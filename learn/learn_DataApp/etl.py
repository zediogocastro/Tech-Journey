"""Module providing an etl process for tenis data"""

import pandas as pd
import psycopg2
from psycopg2.extensions import cursor
from db_values import HOST, DBNAME, USER, PASSWORD
from sql_queries import PLAYER_INSERT

def extrcat_data_from_excel(url: str) -> pd.DataFrame:
    """Extract a pandas data frame from a url"""
    return pd.read_excel(url)

def transform_and_insert_data(df: pd.DataFrame, cur: cursor) -> None:
    """Function to transform raw tennis data and insert it into the database."""
    # Process Players
    row_example = df.iloc[-2:]
    players = pd.concat([row_example['Winner'], row_example['Loser']]).unique()
    for player in players:
        print(player)
        cur.execute(PLAYER_INSERT, (player,))

def load_data_to_db(url: str):
    """Function to extract, transform and load data from the URL into the database"""
    conn = psycopg2.connect(host=HOST, dbname=DBNAME, user=USER, password=PASSWORD)
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    df = extrcat_data_from_excel(url)
    print("DF loaded!")
    transform_and_insert_data(df, cur)
    print("Data inserted!")

def main():
    URL = "http://tennis-data.co.uk/2024/20234.xlsx"
    load_data_to_db(URL)

if __name__ == "__main__":
    main()