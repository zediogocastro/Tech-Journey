table_names = ('songs', 'artists', 'time', 'users', 'songplays')

# CREATE TABLES

song_table_create = """
CREATE TABLE IF NOT EXISTS songs (
  song_id VARCHAR(64) PRIMARY KEY,
  title VARCHAR,
  artist_id VARCHAR,
  year SMALLINT,
  duration DOUBLE PRECISION
);
"""



# QUERY LISTS

CREATE_TABLE_QUERIES = [song_table_create]
DROP_TABLE_QUERIES = [f'DROP TABLE IF EXISTS {table}' for table in table_names]