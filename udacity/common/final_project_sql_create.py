#copied from course 3 project

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS soundplay"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS song"
artist_table_drop = "DROP TABLE IF EXISTS artist"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

# staging
staging_events_table_create= ("""
    
    Create TABLE IF NOT EXISTS staging_events ( 
                                                event_id INTEGER IDENTITY(0,1) NOT NULL,
                                                artist VARCHAR(512) NULL,
                                                auth VARCHAR(512) NULL,
                                                firstName VARCHAR(512) NULL,
                                                gender VARCHAR(512) NULL,
                                                itemInSession INTEGER NULL,
                                                lastName VARCHAR(512) NULL,
                                                length VARCHAR(512) NULL,
                                                level VARCHAR(512) NULL,
                                                location VARCHAR(512) NULL,
                                                method VARCHAR(512) NULL,
                                                page VARCHAR(512) NULL,
                                                regeistration VARCHAR(512) NULL,
                                                sessionID INTEGER NOT NULL,
                                                song VARCHAR(512) NULL,
                                                status INTEGER NULL,
                                                ts BIGINT NOT NULL,
                                                userAgent VARCHAR(512) NULL,
                                                userID INTEGER NULL
                                               );
""")

staging_songs_table_create = ("""

    Create TABLE IF NOT EXISTS staging_songs (
                                                num_songs INTEGER NULL,
                                                artist_id VARCHAR NOT NULL,
                                                artist_latitude VARCHAR(512) NULL,
                                                artist_longitude VARCHAR(512) NULL,
                                                artist_location VARCHAR(512) NULL,
                                                artist_name VARCHAR(512) NULL,
                                                song_id VARCHAR(512) NOT NULL,
                                                title VARCHAR(512) NULL,
                                                duration DECIMAL NULL,
                                                year INTEGER NULL
                                              );
                                                
""")

#Analysis

#Fact
songplay_table_create = ("""

    Create TABLE IF NOT EXISTS songplay (
                                            songplay_id VARCHAR(512)  NOT NULL,
                                            start_time TIMESTAMP NOT NULL, 
                                            user_id VARCHAR(512) NOT NULL,
                                            level VARCHAR(512) NOT NULL,
                                            song_id VARCHAR(512),
                                            artist_id VARCHAR(512),
                                            session_id VARCHAR(512),
                                            location VARCHAR(512) NULL,
                                            user_agent VARCHAR(512) NULL
                                         );
    
    
""")

#Dimension
user_table_create = ("""

    Create TABLE IF NOT EXISTS users (
                                        user_id INTEGER NOT NULL, 
                                        first_name VARCHAR(512) NULL, 
                                        last_name VARCHAR(512) NULL, 
                                        gender VARCHAR(512) NULL, 
                                        level VARCHAR(512) NULL
                                     );

""")

song_table_create = ("""

    Create TABLE IF NOT EXISTS song (
                                        song_id VARCHAR(512) NOT NULL, 
                                        title VARCHAR(512) NOT NULL, 
                                        artist_id VARCHAR(512) NOT NULL, 
                                        year INTEGER NOT NULL, 
                                        duration DECIMAL NOT NULL
                                     );
""")

artist_table_create = ("""

    Create TABLE IF NOT EXISTS artist (
                                        artist_id VARCHAR(512) NOT NULL, 
                                        name VARCHAR(512) NULL, 
                                        location VARCHAR(512) NULL, 
                                        latitude VARCHAR(512) NULL, 
                                        longitude VARCHAR(512) NULL
                                       );
""")

time_table_create = ("""

    Create TABLE IF NOT EXISTS time ( 
                                        start_time TIMESTAMP NOT NULL, 
                                        hour INTEGER NULL, 
                                        day INTEGER NULL, 
                                        week INTEGER NULL, 
                                        month INTEGER NULL, 
                                        year INTEGER NULL, 
                                        weekday INTEGER NULL
                                     );
    
    
""")







drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
