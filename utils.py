"""
Weather Analytics Dashboard - Utility Functions
Provides helper functions for model loading, data preprocessing, and visualization
"""

import os
import pickle
import pandas as pd
import numpy as np
from datetime import datetime

def load_model(filepath):
    """Load a pickle model file safely"""
    try:
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        return None, str(e)

def get_all_cities(model_dir):
    """Extract unique city names from model directory"""
    if not os.path.exists(model_dir):
        return []
    
    files = os.listdir(model_dir)
    cities = set()
    
    for f in files:
        parts = f.replace('.pkl', '').split('_')
        if len(parts) > 0:
            cities.add(parts[0])
    
    return sorted(list(cities))

def get_available_targets(city, model_dir):
    """Get available target variables for a city"""
    if not os.path.exists(model_dir):
        return []
    
    files = os.listdir(model_dir)
    targets = set()
    
    for f in files:
        if f.startswith(city + '_'):
            parts = f.replace('.pkl', '').split('_')
            if len(parts) > 1:
                target = '_'.join(parts[1:])
                targets.add(target)
    
    return sorted(list(targets))

def format_city_name(city_str):
    """Format city name for display"""
    return city_str.replace('_', ' ').title()

def format_target_name(target_str):
    """Format target variable name for display"""
    return target_str.replace('_', ' ').title()

def get_model_stats():
    """Get statistics about available models"""
    base_path = "/home/admin123/DIV Academy/PYTHON/"
    
    stats = {
        'total_models': 0,
        'time_series': 0,
        'regression': 0,
        'classification': 0,
        'clustering': 0,
        'cities': 0
    }
    
    try:
        # Count models
        dirs = {
            'time_series': os.path.join(base_path, 'saved_models1'),
            'regression': os.path.join(base_path, 'saved_models_reg'),
            'classification': os.path.join(base_path, 'saved_models_clasf'),
            'clustering': os.path.join(base_path, 'saved_models_clustering')
        }
        
        for key, dir_path in dirs.items():
            if os.path.exists(dir_path):
                files = [f for f in os.listdir(dir_path) if f.endswith('.pkl')]
                stats[key] = len(files)
                stats['total_models'] += len(files)
        
        # Count cities
        if os.path.exists(dirs['classification']):
            cities = get_all_cities(dirs['classification'])
            stats['cities'] = len(cities)
    
    except Exception as e:
        print(f"Error calculating stats: {e}")
    
    return stats

def validate_input_data(input_dict, expected_features):
    """Validate that input data has all expected features"""
    missing = set(expected_features) - set(input_dict.keys())
    return len(missing) == 0, missing

def prepare_forecast_dataframe(forecast_mean, forecast_ci, forecast_steps):
    """Prepare forecast data for display"""
    dates = pd.date_range(start=datetime.now(), periods=forecast_steps, freq='D')
    
    return pd.DataFrame({
        'Date': dates,
        'Predicted Temp (°C)': forecast_mean.values,
        'Lower 95% CI': forecast_ci.iloc[:, 0].values,
        'Upper 95% CI': forecast_ci.iloc[:, 1].values
    })

def get_model_accuracy_info():
    """Return general accuracy information for models"""
    return {
        'time_series': 'MAPE < 15% for most cities',
        'regression': 'R² > 0.7 for most targets',
        'classification': 'Accuracy > 80% for most tasks',
        'clustering': 'High silhouette scores'
    }

class ModelCache:
    """Cache loaded models to improve performance"""
    
    def __init__(self):
        self.cache = {}
    
    def get(self, key):
        return self.cache.get(key)
    
    def set(self, key, value):
        self.cache[key] = value
    
    def clear(self):
        self.cache.clear()
    
    def has(self, key):
        return key in self.cache

# Global cache instance
model_cache = ModelCache()
