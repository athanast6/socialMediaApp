# utils.py

from django.conf import settings
from joblib import load
import os

# Load the model during application initialization
# Construct the path to the model file
legend_model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'my_nba_legend_model.pkl')
legend_model = load(legend_model_path)