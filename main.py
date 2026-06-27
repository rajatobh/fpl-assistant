import requests

url = "https://fantasy.premierleague.com/api/bootstrap-static/"

response = requests.get(url)

data = response.json()

players = data['elements']

element_types = data['element_types']

positions = {t['id']: t['singular_name_short'] for t in element_types}

print("-" * 70)
print(f"| {'Name':<30} | {'Pos':<5} | {'Price':<10} | {'Points':<10} |")
print("-" * 70)

for player in players[:10]:
    name = f"{player['first_name']} {player['second_name']}"
    price = f"£{player['now_cost']/10}m"
    points = player['total_points']
    position = positions[player['element_type']]
    print(f"| {name:<30} | {position:<5} | {price:<10} | {points:<10} |")