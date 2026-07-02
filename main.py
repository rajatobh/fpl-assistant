import requests
from database import create_tables
create_tables()

url = "https://fantasy.premierleague.com/api/bootstrap-static/"
response = requests.get(url)
data = response.json()

players = data['elements']
positions = {t['id']: t['singular_name_short'] for t in data['element_types']}
teams = {t['id']: t['name'] for t in data['teams']}

divider = "-" * 97

def print_players(filtered_players):
    print(divider)
    print(f"| {'Name':<30} | {'Team':<25} | {'Pos':<5} | {'Price':<10} | {'Points':<10} |")
    print(divider)
    for player in filtered_players:
        name = f"{player['first_name']} {player['second_name']}"
        position = positions[player['element_type']]
        price_value = player['now_cost'] / 10
        team = teams[player['team']]
        price = f"£{price_value}m"
        points = player['total_points']
        print(f"| {name:<30} | {team:<25} | {position:<5} | {price:<10} | {points:<10} |")
    print("-" * 97)

def search_players():
    search = input("Search for a player (or press Enter to skip): ").lower()
    pos_filter = input("Filter by position (GK/DEF/MID/FWD or press Enter to skip): ").upper()
    budget = input("Max price (eg. 7.0 or press Enter to skip): ")
    sort_by = input("Sort by (points/price or press Enter to skip): ").lower()

    filtered_players = []

    for player in players:
        name = f"{player['first_name']} {player['second_name']}"
        position = positions[player['element_type']]
        price_value = player['now_cost'] / 10

        if search in name.lower():
            if pos_filter == "" or position == pos_filter:
                if budget == "" or price_value <= float(budget):
                    filtered_players.append(player)

    if sort_by == "points":
        filtered_players.sort(key=lambda x: x['total_points'], reverse=True)
    elif sort_by == "price":
        filtered_players.sort(key=lambda x: x['now_cost'], reverse=True)

    print_players(filtered_players)

def top_picks():
    pos_filter = input("Position (GK/DEF/MID/FWD): ").upper()
    filtered = [p for p in players if positions[p['element_type']] == pos_filter]
    filtered.sort(key=lambda x:x['total_points'], reverse=True)
    print_players(filtered[:10])

while True:
    print("\n--- FPL Assistant ---")
    print("1. Search players")
    print("2. Top picks by position")
    print("3. Exit")

    choice = input("\nChoose an option: ")

    if choice == "1":
        search_players()
    elif choice == "2":
        top_picks()
    elif choice == "3":
        print("Goodbye!")
        break
    else:
        print("Invalid option, pick 1-3")