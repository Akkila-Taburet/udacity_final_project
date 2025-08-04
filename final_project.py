from datetime import datetime, timedelta
import pendulum
import os
from airflow.decorators import dag
from airflow.operators.dummy_operator import DummyOperator
from final_project_operators.stage_redshift import StageToRedshiftOperator
from final_project_operators.load_fact import LoadFactOperator
from final_project_operators.load_dimension import LoadDimensionOperator
from final_project_operators.data_quality import DataQualityOperator
from airflow.operators.postgres_operator import PostgresOperator
from udacity.common import final_project_sql_statements,final_project_sql_create


default_args = {
    'owner': 'Akkila',
    'start_date': pendulum.now(),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_retry': False,
    'max_active_runs': 3

}

@dag(
    default_args=default_args,
    description='Load and transform data in Redshift with Airflow',
    schedule_interval='@hourly',
    'catchup':False
)
def final_project():

    start_operator = PostgresOperator(
        task_id="Begin_execution",
        postgres_conn_id="redshift",
        sql=final_project_sql_create.create_table_queries
        #[]   
    )

    stage_events_to_redshift = StageToRedshiftOperator(
        task_id="Stage_events",
        aws_credentials_id="aws_credentials",
        redshift_conn_id="redshift",
        table="staging_events",
        s3_bucket="akkila-air",
        s3_key="log-data/",
        json="s3://akkila-air/log_json_path.json",
        skip = "false"
    )


    stage_songs_to_redshift = StageToRedshiftOperator(
        task_id='Stage_songs',
        aws_credentials_id="aws_credentials",
        redshift_conn_id="redshift",
        table="staging_songs",
        s3_bucket="akkila-air",
        s3_key="song-data/",
        json="auto",
        skip= "false"
    )

    load_songplays_table = LoadFactOperator(
        task_id='Load_songplays_fact_table',
        redshift_conn_id="redshift",
        sql=final_project_sql_statements.SqlQueries.songplay_table_insert
        

    )

    load_user_dimension_table = LoadDimensionOperator(
        task_id='Load_user_dim_table',
        redshift_conn_id="redshift",
        sql=final_project_sql_statements.SqlQueries.user_table_insert,
        table="users",
        append="false"
    )

    load_song_dimension_table = LoadDimensionOperator(
        task_id='Load_song_dim_table',
        redshift_conn_id="redshift",
        sql=final_project_sql_statements.SqlQueries.song_table_insert,
        table="song",
        append="false"
    )

    load_artist_dimension_table = LoadDimensionOperator(
        task_id='Load_artist_dim_table',
        redshift_conn_id="redshift",
        sql=final_project_sql_statements.SqlQueries.artist_table_insert,
        table="artist",
        append="false"
    )

    load_time_dimension_table = LoadDimensionOperator(
        task_id='Load_time_dim_table',
        redshift_conn_id="redshift",
        sql=final_project_sql_statements.SqlQueries.time_table_insert,
        table="time",
        append="false"
    )

    run_quality_checks = DataQualityOperator(
        task_id='Run_data_quality_checks',
        redshift_conn_id="redshift",
        tables = ["time","artist","song","users","songplay"]

    )

    end_operator = DummyOperator(task_id='End_execution')

    start_operator >> [stage_songs_to_redshift,stage_events_to_redshift]     
    [stage_events_to_redshift, stage_songs_to_redshift] >> load_songplays_table
    load_songplays_table >> [load_user_dimension_table,load_song_dimension_table,load_artist_dimension_table,load_time_dimension_table]
    [load_user_dimension_table,load_song_dimension_table,load_artist_dimension_table,load_time_dimension_table] >>  run_quality_checks
    run_quality_checks >> end_operator
final_project_dag = final_project()
