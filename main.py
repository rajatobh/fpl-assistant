import requests

url = "https://fantasy.premierleague.com/api/bootstrap-static/"

response = requests.get(url)

data = response.json()

players = data['elements']

for player in players[:10]:
    print(f"{player['first_name']} {player['second_name']} | £{player['now_cost']/10}m | {player['total_points']}")