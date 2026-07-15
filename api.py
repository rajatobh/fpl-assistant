import requests

BASE_URL = "https://fantasy.premierleague.com/api"

def get_bootstrap_data():
    url = f"{BASE_URL}/bootstrap-static/"
    response = requests.get(url)
    return response.json()

def get_player_history(player_id):
    url = f"{BASE_URL}/element-summary/{player_id}/"
    response = requests.get(url)
    return response.json()['history']
