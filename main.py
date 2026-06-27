import requests

url = "https://fantasy.premierleague.com/api/bootstrap-static/"

response = requests.get(url)

data = response.json()

players = data['elements']

print("-" * 60)
print(f"| {'Name':<30} | {'Price':<10} | {'Points':<10} |")
print("-" * 60)

for player in players[:10]:
    name = f"{player['first_name']} {player['second_name']}"
    price = f"£{player['now_cost']/10}m"
    points = player['total_points']
    print(f"| {name:<30} | {price:<10} | {points:<10} |")