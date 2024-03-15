# utils.py
import os
import io

from django.conf import settings
from joblib import load

import pandas as pd
import redis
import csv

rosters_file_path = os.path.join(settings.BASE_DIR, 'static', 'NBARatingsMar2024.csv')

# Load the model during application initialization
# Construct the path to the model file
legend_model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'my_nba_legend_model.pkl')
legend_model = load(legend_model_path)



nba_player_model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'which_nba_player_model.pkl')
nba_player_model = load(nba_player_model_path)



def get_rosters():
    rosters = pd.read_csv(rosters_file_path)
    return(rosters)




# Connect to Redis
def get_roster_data():
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
    # Check if data exists in cache
    csv_data = redis_client.get('csv_data')
    if csv_data:
        return csv_data.decode('utf-8')  # Decode bytes to string
    else:
        # Fetch CSV data from source (e.g., file system, database)
        rosters = get_rosters()
        # Store CSV data in cache with expiry time
        redis_client.setex(rosters, 3600, csv_data)  # Expires in 1 hour
        return csv_data


