# utils.py
import os
import io

from django.conf import settings
from joblib import load

import pandas as pd

rosters_file_path = os.path.join(settings.STATIC_ROOT, 'hooptoday/ncaa_ratings_2024.csv')
ncaa_team_names_path = os.path.join(settings.STATIC_ROOT, 'hooptoday/ncaa_team_abbreviations.csv')

# Load the model during application initialization
# Construct the path to the model file
legend_model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'my_nba_legend_model.pkl')
legend_model = load(legend_model_path)



nba_player_model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'which_nba_player_model.pkl')
nba_player_model = load(nba_player_model_path)



def get_rosters():
    rosters = pd.read_csv(rosters_file_path)
    return(rosters)


