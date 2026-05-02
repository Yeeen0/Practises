import json
import os

def load_json(filename, default_data):
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except:
            pass
    return default_data

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def load_settings():
    default = {"sound": True, "car_color": "Blue", "difficulty": "Normal"}
    return load_json("settings.json", default)

def save_settings(settings):
    save_json("settings.json", settings)

def load_leaderboard():
    return load_json("leaderboard.json", [])

def save_leaderboard(leaderboard):
    leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)[:10]
    save_json("leaderboard.json", leaderboard)