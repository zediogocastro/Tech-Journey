import glob
import os
from typing import List

import psycopg2
import numpy as np
from psycopg2.extensions import cursor

import pandas as pd

from db_values import HOST, DBNAME, USER, PASSWORD
from sql_queries import SONG_TABLE_INSERT, ARTIST_TABLE_INSERT


# To avoid `psycopg2.ProgrammingError: can't adapt type 'numpy.int64'` when
# executing the INSERT command:
psycopg2.extensions.register_adapter(np.int64, psycopg2.extensions.AsIs)
psycopg2.extensions.register_adapter(np.float64, psycopg2.extensions.AsIs)

def process_song_file(cur: cursor,
                      filepath: str,
                      song_table_insert: str = SONG_TABLE_INSERT,
                      artist_table_insert: str = ARTIST_TABLE_INSERT):
    """
    Read JSON file and insert data into songs and artists dimensional tables.

    Parameters
    ----------
    cur : psycopg2.extensions.cursor
        Database cursor.
    filepath : str
        Path of the JSON file.
    song_table_insert : str, optional
        INSERT statement.
    artist_table_insert : str, optional
        INSERT statement.

    Returns
    -------
    None
    """
    # Read song file
    df = pd.read_json(filepath, lines=True)
    df.convert_dtypes()

    # Insert song record
    song_data = (df
                .loc[0, ['song_id', 'title', 'artist_id', 'year', 'duration']]
                .values.tolist())
    cur.execute(SONG_TABLE_INSERT, song_data)

    # Insert artist record
    # LATER Improve with a MERGE INTO
    raw_artist_data = (df
                   .loc[0, ['artist_id', 'artist_name', 'artist_location', 
                            'artist_latitude', 'artist_longitude']])
    
    # TO CHECK IF THERE IS A BETTER WAY TO DEAL WITH THIS
    clean_artist_data = [
        raw_artist_data['artist_id'] if pd.notna(raw_artist_data['artist_id']) else None,
        raw_artist_data['artist_name'] if pd.notna(raw_artist_data['artist_name']) else None,
        raw_artist_data['artist_location'] if pd.notna(raw_artist_data['artist_location']) else None,
        raw_artist_data['artist_latitude'] if pd.notna(raw_artist_data['artist_latitude']) else None,
        raw_artist_data['artist_longitude'] if pd.notna(raw_artist_data['artist_longitude']) else None,
    ]
    print(clean_artist_data)
    cur.execute(ARTIST_TABLE_INSERT, clean_artist_data)


def get_files(filepath: str, pattern: str = '*.json') -> List[str]:
    """
    Get all files matching pattern in directory.

    Parameters
    ----------
    filepath : str
        Path with files possibly under sub-folders.
    pattern : str, optional
        Pattern to search in file names.

    Returns
    -------
    list[str]
        List of full file names.
    """
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, pattern))
        for f in files:
            all_files.append(os.path.abspath(f))

    return all_files

def process_data(cur: cursor, filepath: str, func: callable) -> None:
    """
    Run 'func' on all files under 'filepath'.

    Parameters
    ----------
    cur : psycopg2.extensions.cursor
        Database cursor.
    filepath : str 
        Path with files possibly under sub-folders.
    func : callable
        Function.
    
    Returns
    -------
    None
    """

    # Get all files matching extension in directory
    all_files = get_files(filepath)

    # Get total number of files found
    num_files = len(all_files)
    print(f'{num_files} files found in "{filepath}"')

    # Iterate over files and process
    for i, datafile in enumerate(all_files, start=1):
        func(cur, datafile)
        print(f"{i}/{num_files} files processed")

def main():
    conn = psycopg2.connect(host=HOST, dbname=DBNAME, 
                            user=USER, password=PASSWORD)
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    process_data(cur, filepath='data/song_data', func=process_song_file)

if __name__ == "__main__":
    main()