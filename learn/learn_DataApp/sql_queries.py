"""Module providig sql queries"""

table_names = (
    "players",
    "player_rankings",  
    "matches",
    "tournaments", 
    "match_scores", 
    "betting_odds"
)

# CREATE TABLES

PLAYERS_TABLE_CREATE = """
CREATE TABLE IF NOT EXISTS players (
  player_id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL
);
"""

PLAYER_RANKINGS_TABLE_CREATE= """
CREATE TABLE IF NOT EXISTS player_rankings (
  ranking_id SERIAL PRIMARY KEY,
  player_id INT REFERENCES players(player_id),
  ranking_date DATE NOT NULL,
  rank INT NOT NULL,
  points INT,
  UNIQUE(player_id, ranking_date),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
"""

MATCHES_TABLE_CREATE = """
CREATE TABLE IF NOT EXISTS matches (
  match_id SERIAL PRIMARY KEY,
  tournament_id INT REFERENCES tournaments(tournament_id) ON DELETE CASCADE,
  date DATE NOT NULL,
  round VARCHAR(50),
  best_of INT,
  winner_id INT REFERENCES players(player_id) ON DELETE CASCADE,
  loser_id INT REFERENCES players(player_id) ON DELETE CASCADE,
  winner_rank INT,
  loser_rank INT,
  winner_pts INT,
  loser_pts INT,
  winner_sets INT CHECK (winner_sets >= 0),
  loser_sets INT CHECK (loser_sets >= 0),
  comments TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
"""

TOURNAMENTS_TABLE_CREATE= """
CREATE TABLE IF NOT EXISTS tournaments (
  tournament_id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  location VARCHAR(100),
  surface VARCHAR(50),
  series VARCHAR(50),
  court VARCHAR(50)
);
"""

MATCH_SCORES_TABLE_CREATE = """
CREATE TABLE IF NOT EXISTS match_scores (
  score_id SERIAL PRIMARY KEY,
  match_id INT REFERENCES matches(match_id) ON DELETE CASCADE,
  set_number INT CHECK (set_number > 0),
  winner_score INT,
  loser_score INT
);
"""

BETTING_ODDS_TABLE_CREATE = """
CREATE TABLE IF NOT EXISTS betting_odds (
  odds_id SERIAL PRIMARY KEY,
  match_id INT REFERENCES matches(match_id) ON DELETE CASCADE,
  bookmaker VARCHAR(50),
  winner_odds DECIMAL(5, 2),
  loser_odds DECIMAL(5, 2)
);
"""

# QUERY LISTS
CREATE_TABLE_QUERIES = [
    PLAYERS_TABLE_CREATE,
    PLAYER_RANKINGS_TABLE_CREATE,
    MATCHES_TABLE_CREATE,
    TOURNAMENTS_TABLE_CREATE,
    MATCH_SCORES_TABLE_CREATE,
    BETTING_ODDS_TABLE_CREATE
]

DROP_TABLE_QUERIES = [f"DROP TABLE IF EXISTS {table}" for table in table_names]
