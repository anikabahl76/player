import sqlite3
from sqlite3 import Error
import pandas as pd

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
    except Error as err:
        print(f"Failed to make database because '{err}'")
    return connection

def get_cursor():
    connection = create_connection("E:\\sm_app.sqlite")
    cursor = connection.cursor()
    return connection, cursor

connection, cursor = get_cursor()

def clean_name(df, column_name):
    df[column_name] = list(df[column_name].str.split(" "))
    df[column_name] = df[column_name].str[0].str[0] + " " + df[column_name].str[1]
    return df[column_name]
    
player_data = pd.read_csv("data/Players.csv")
player_data = player_data[["Player_Id", "Player_Name"]]
player_data["Player_Name"] = clean_name(player_data, "Player_Name")
player_data = player_data.dropna()

ball_data = pd.read_csv("data/Balls.csv")
ball_data["4"] = ball_data["batsman_runs"] == 4
ball_data["6"] = ball_data["batsman_runs"] == 6
ball_data["boundary"] = ball_data["4"] | ball_data["6"]
ball_data = ball_data[["inning","over","ball","batsman","non_striker","bowler", "total_runs", "boundary"]]
ball_data["batsman"] = clean_name(ball_data, "batsman")
ball_data["non_striker"] = clean_name(ball_data, "non_striker")
ball_data["bowler"] = clean_name(ball_data, "bowler")
ball_data = ball_data.dropna()

cursor.execute('CREATE TABLE IF NOT EXISTS players (player_id int, player_name nvarchar(50))')
cursor.execute('CREATE TABLE IF NOT EXISTS balls (inning int, over int, ball int, batsman nvarchar(50), non_striker nvarchar(50), bowler nvarchar(50), total_runs int, boundary boolean)')

for player in player_data.itertuples():
    cursor.execute('''INSERT INTO players (player_id, player_name) VALUES (?,?)''',
                (player.Player_Id, 
                player.Player_Name))

connection.commit()

for ball in ball_data.itertuples():
    cursor.execute('INSERT INTO balls (inning, over, ball, batsman, non_striker, bowler, total_runs, boundary) VALUES (?,?,?,?,?,?,?,?)',
                (ball.inning, 
                ball.over,
                ball.ball,
                ball.batsman,
                ball.non_striker,
                ball.bowler,
                ball.total_runs,
                ball.boundary))
connection.commit()


