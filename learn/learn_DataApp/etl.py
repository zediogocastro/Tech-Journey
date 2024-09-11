"""Module providing an etl process for tenis data"""

import pandas as pd
import psycopg2
from psycopg2.extensions import cursor
from db_values import HOST, DBNAME, USER, PASSWORD
from sql_queries import PLAYER_INSERT, TOURNAMENT_INSERT, MATCH_INSERT, PLAYER_RANKING_INSERT, MATCH_SCORES_INSERT, BETTING_ODDS_INSERT

def extrcat_data_from_excel(url: str) -> pd.DataFrame:
    """Extract a pandas data frame from a url"""
    return pd.read_excel(url)

def transform_and_insert_data(df: pd.DataFrame, cur: cursor) -> None:
    """Function to transform raw tennis data and insert it into the database."""
    # Process Players
    players = pd.concat([df['Winner'], df['Loser']]).unique()
    for player in players:
        cur.execute(PLAYER_INSERT, (player,))

    # Process Tournaments
    tournamemts = df[["Tournament", "Location", "Surface", "Series", "Court"]].drop_duplicates()
    for _, row in tournamemts.iterrows():
        cur.execute(TOURNAMENT_INSERT, (row["Tournament"], 
                                            row["Location"], 
                                            row["Surface"], 
                                            row["Series"], 
                                            row["Court"])
                                        )
    
    # Process matches and player rankings
    for _, row in df.iterrows():
        # Get player IDs for winner and loser
        cur.execute("SELECT player_id FROM players WHERE name = %s", (row['Winner'],))
        winner_id = cur.fetchone()[0]

        cur.execute("SELECT player_id FROM players WHERE name = %s", (row['Loser'],))
        loser_id = cur.fetchone()[0]

        # Get tournament ID
        cur.execute("SELECT tournament_id FROM tournaments WHERE name = %s", (row['Tournament'],))
        tournament_id = cur.fetchone()[0]

        # Insert match
        match_data = (
            tournament_id, row['Date'], row['Round'], row['Best of'],
            winner_id, loser_id, row['WRank'], row['LRank'], 
            row['WPts'], row['LPts'], row['Wsets'], row['Lsets'], row['Comment']
        )
        cur.execute(MATCH_INSERT, match_data)
        match_id = cur.fetchone()[0] # Get the match_id of the inserted match

        # Insert Match Scores
        for set_number in range(1, 6):  # Loop through 5 possible sets
            winner_score = row.get(f'W{set_number}')
            loser_score = row.get(f'L{set_number}')
            
            # Only insert scores where there is data (i.e., not NaN)
            if pd.notna(winner_score) and pd.notna(loser_score):
                cur.execute(MATCH_SCORES_INSERT, (match_id, set_number, winner_score, loser_score))

        # Insert Betting Odds for each bookmaker
        bookmakers = {
            "Bet365": (row['B365W'], row['B365L']),
            "Pinnacle": (row['PSW'], row['PSL']),
            "Max": (row['MaxW'], row['MaxL']),
            "Avg": (row['AvgW'], row['AvgL'])
        }
        
        for bookmaker, odds in bookmakers.items():
            winner_odds, loser_odds = odds
            cur.execute(BETTING_ODDS_INSERT, (match_id, bookmaker, winner_odds, loser_odds))
        

        # Insert player rankings
        cur.execute(PLAYER_RANKING_INSERT, (winner_id, row['Date'], row['WRank'], row['WPts']))
        cur.execute(PLAYER_RANKING_INSERT, (loser_id, row['Date'], row['LRank'], row['LPts']))


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