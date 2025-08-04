from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.secrets.metastore import MetastoreBackend
from airflow.exceptions import AirflowSkipException



class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'
    copy_sql = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        JSON '{}'
        BLANKSASNULL 
        EMPTYASNULL

    """

    @apply_defaults
    def __init__(
                self,
                redshift_conn_id="",
                aws_credentials_id="",
                table="",
                s3_bucket="",
                s3_key="",
                json="auto",
                skip="false",
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.aws_credentials_id = aws_credentials_id
        self.json = json
        self.skip = skip

    def execute(self, context):
        metastoreBackend = MetastoreBackend()
        aws_connection=metastoreBackend.get_connection(self.aws_credentials_id)
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)


        
        key = self.s3_key.format(**context)
        s3_path = "s3://{}/{}".format(self.s3_bucket, key)

        copy_sql = StageToRedshiftOperator.copy_sql.format(
            self.table,
            s3_path,
            aws_connection.login,
            aws_connection.password,
            self.json
        )
        if self.skip.lower() == "false":
            self.log.info("Deleting data from {self.table}")
            redshift.run("DELETE FROM {}".format(self.table))

            self.log.info("Copy data from s3 to {self.table}")
            redshift.run(copy_sql)
        else:
            self.log.info(f"Skipping staging to Redshift for table {self.table}")
            #raise AirflowSkipException("StageToRedshiftOperator was skipped as per configuration.")
