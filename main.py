import requests
from database import create_tables, add_to_watchlist, get_watchlist, remove_from_watchlist
create_tables()

url = "https://fantasy.premierleague.com/api/bootstrap-static/"
response = requests.get(url)
data = response.json()

players = data['elements']
positions = {t['id']: t['singular_name_short'] for t in data['element_types']}
teams = {t['id']: t['name'] for t in data['teams']}

divider = "-" * 110

def print_players(filtered_players):
    print(divider)
    print(f"| {'Name':<30} | {'Team':<25} | {'Pos':<5} | {'Price':<10} | {'Points':<10} | {'Value':<8} |")
    print(divider)
    for player in filtered_players:
        name = f"{player['first_name']} {player['second_name']}"
        position = positions[player['element_type']]
        price_value = player['now_cost'] / 10
        team = teams[player['team']]
        price = f"£{price_value}m"
        points = player['total_points']
        value = round(points / price_value, 1) if price_value > 0 else 0
        print(f"| {name:<30} | {team:<25} | {position:<5} | {price:<10} | {points:<10} | {value:<8} |")
    print(divider)

def search_players():
    search = input("Search for a player (or press Enter to skip): ").lower()
    pos_filter = input("Filter by position (GKP/DEF/MID/FWD or press Enter to skip): ").upper()
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
    global players
    pos_filter = input("Position (GKP/DEF/MID/FWD): ").upper()
    filtered = [p for p in players if positions[p['element_type']] == pos_filter]
    filtered.sort(key=lambda x:x['total_points'], reverse=True)
    print_players(filtered[:10])

def save_to_watchlist():
    search = input("Enter player name to add to watchlist: ").lower()

    matches = []
    for player in players:
        name = f"{player['first_name']} {player['second_name']}"
        if search in name.lower():
            matches.append(player)

    if len(matches) == 0:
        print("No players found!")
    elif len(matches) == 1:
        p = matches[0]
        name = f"{p['first_name']} {p['second_name']}"
        team = teams[p['team']]
        position = positions[p['element_type']]
        price = p['now_cost'] / 10
        points = p['total_points']
        add_to_watchlist(p['id'], name, team, position, price, points)
    else:
        print("\nMultiple players found:")
        for i, p in enumerate(matches):
            name = f"{p['first_name']} {p['second_name']}"
            print(f"{i + 1}. {name} - {teams[p['team']]}")
        choice = int(input("Choose a player: ")) - 1
        p = matches[choice]
        name = f"{p['first_name']} {p['second_name']}"
        team = teams[p['team']]
        position = positions[p['element_type']]
        price = p['now_cost'] / 10
        points = p['total_points']
        add_to_watchlist(p['id'], name, team, position, price, points)

def view_watchlist():
    players = get_watchlist()

    if len(players) == 0:
        print("Your watchlist is empty!")
        return
    
    print(divider)
    print(f"| {'Name':<30} | {'Team':<25} | {'Pos':<5} | {'Price':<10} | {'Points':<10} |")
    print(divider)

    for player in players:
        _, player_id, name, team, position, price, points = player
        print(f"| {name:<30} | {team:<25} | {position:<5} | £{price:<9} | {points:<10} |")

    print(divider)

def delete_from_watchlist():
    players = get_watchlist()

    if len(players) == 0:
        print("Your watchlist is empty!")
        return
    
    print("\nYour watchlist:")
    for i, player in enumerate(players):
        _, player_id, name, team, position, price, points = player
        print(f"{i + 1}. {name} - {team}")

    choice = int(input("\nChoose a player to remove: ")) - 1
    selected = players[choice]
    remove_from_watchlist(selected[1])


while True:
    print("\n--- FPL Assistant ---")
    print("1. Search players")
    print("2. Top picks by position")
    print("3. Add player to watchlist")
    print("4. View watchlist")
    print("5. Remove from watchlist")
    print("6. Exit")

    choice = input("\nChoose an option: ")

    if choice == "1":
        search_players()
    elif choice == "2":
        top_picks()
    elif choice =="3":
        save_to_watchlist()
    elif choice == "4":
        view_watchlist()
    elif choice == "5":
        delete_from_watchlist()
    elif choice == "6":
        print("Goodbye!")
        break
    else:
        print("Invalid option, pick 1-4")
