# user_profiles.py
import json
import os

USER_PROFILES_FILE = 'user_profiles.json'

def load_user_profiles():
    if os.path.exists(USER_PROFILES_FILE):
        with open(USER_PROFILES_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_user_profiles(profiles):
    with open(USER_PROFILES_FILE, 'w') as f:
        json.dump(profiles, f)

def update_user_profile(user_id, preferences):
    profiles = load_user_profiles()
    profiles[user_id] = preferences
    save_user_profiles(profiles)

def get_user_profile(user_id):
    profiles = load_user_profiles()
    return profiles.get(user_id, {})