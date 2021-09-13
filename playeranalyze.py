from database import get_cursor
from mlmodel import get_knn_model_accuracy
import pandas as pd


connection, cursor = get_cursor()
id_cache = {}

def get_player_data(player_name):
    query = "SELECT * FROM balls WHERE batsman = \'" + player_name + "\'"
    df = pd.read_sql_query(query, connection)
    batsman_id = get_player_id(player_name, id_cache)
    #df["non_striker_id"] = df.apply(lambda row: get_player_id(row["non_striker"], id_cache), axis=1)
    #df["bowler_id"] = df.apply(lambda row: get_player_id(row["bowler"], id_cache), axis=1)
    df["non_striker_id"] = map(lambda s: get_player_id(s, id_cache), df["non_striker"])
    df["bowler_id"] = map(lambda s: get_player_id(s, id_cache), df["bowler"])
    df["batsman_id"] = batsman_id
    df = df[["inning", "over", "ball", "total_runs", "boundary", "non_striker_id", "bowler_id", "batsman_id"]]
    df = df.dropna()
    return df

def get_player_id(player_name, cache):
    query = "SELECT player_id FROM players WHERE player_name = \'" + player_name + "\'"
    df = pd.read_sql_query(query, connection)
    try:
        id = cache[player_name]
    except:
        try:  
            id = df['player_id'].iloc[0]
            cache["player_name"] = id
        except:
            id = None
    return id

def get_run_prediction_model(player_name):
    data = get_player_data("V Kohli")
    model, accuracy = get_knn_model_accuracy(data, 25)
    return model