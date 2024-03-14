# utils.py
import os
import io

from django.conf import settings
from joblib import load

import pandas as pd

from .cloudstorage import download_blob_file, get_blob_service_client_account_key

rosters_file_name = "NBARatingsMar2024.csv"

# Load the model during application initialization
# Construct the path to the model file
legend_model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'my_nba_legend_model.pkl')
legend_model = load(legend_model_path)



nba_player_model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'which_nba_player_model.pkl')
nba_player_model = load(nba_player_model_path)



def get_rosters():
    container_name = 'hoop-today-blob'
    #container_client = blob_service_client.get_container_client(container_name)
    #blob_client = container_client.get_blob_client(file_name)

    blob_service_client = get_blob_service_client_account_key()

    print(blob_service_client.account_name)

    file_name = rosters_file_name
    
    file = download_blob_file(blob_service_client=blob_service_client,filename=file_name,container_name=container_name)

    print(container_name)

    nba_ratings = file.readall()


    df = pd.read_csv(io.BytesIO(nba_ratings))

    # Now you can work with the DataFrame 'df' containing the CSV data
    print(df.head())

    return df


rosters = get_rosters()