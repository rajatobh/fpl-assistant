import requests

url = "https://fantasy.premierleague.com/api/bootstrap-static/"

response = requests.get(url)

data = response.json()

players = data['elements']

element_types = data['element_types']

positions = {t['id']: t['singular_name_short'] for t in element_types}

teams = {t['id']: t['name'] for t in data['teams']}

print("-" * 97)
print(f"| {'Name':<30} | {'Team':<25} | {'Pos':<5} | {'Price':<10} | {'Points':<10} |")
print("-" * 97)

for player in players[:10]:
    name = f"{player['first_name']} {player['second_name']}"
    price = f"£{player['now_cost']/10}m"
    points = player['total_points']
    position = positions[player['element_type']]
    team = teams[player['team']]
    print(f"| {name:<30} | {team:<25} | {position:<5} | {price:<10} | {points:<10} |")

search = input("\nSearch for a player: ").lower()
pos_filter = input("Filter by position (GK/DEF/MID/FWD or press Enter to skip): ").upper()
budget = input("Max price (eg. 7.0 or press Enter to skip): ")

for player in players:
    name = f"{player['first_name']} {player['second_name']}"
    position = positions[player['element_type']
                         ]
    if search in name.lower():
        if pos_filter == "" or position == pos_filter:
            price_value = player['now_cost']/10
            if budget == "" or price_value <= float(budget):
                team = teams[player['team']]
                price = f"£{player['now_cost']/10}m"
                points = player['total_points']
                print(f"| {name:<30} | {team:<25} | {position:<5} | {price:<10} | {points:<10} |")
