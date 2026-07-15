from api import get_player_history
from display import print_players, print_history
from database import add_to_watchlist, get_watchlist, remove_from_watchlist


def search_players(players, positions, teams):
    search = input("Search for a player (or press Enter to skip): ").lower()
    pos_filter = input("Filter by position (GKP/DEF/MID/FWD or press Enter to skip): ").upper()
    budget = input("Max price (e.g. 7.0 or press Enter to skip): ")
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

    print_players(filtered_players, positions, teams)


def top_picks(players, positions, teams):
    pos_filter = input("Position (GKP/DEF/MID/FWD): ").upper()
    filtered = [p for p in players if positions[p['element_type']] == pos_filter]
    filtered.sort(key=lambda x: x['total_points'], reverse=True)
    print_players(filtered[:10], positions, teams)


def save_to_watchlist(players, positions, teams):
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

    print("-" * 97)
    print(f"| {'Name':<30} | {'Team':<25} | {'Pos':<5} | {'Price':<10} | {'Points':<10} |")
    print("-" * 97)

    for player in players:
        _, player_id, name, team, position, price, points = player
        print(f"| {name:<30} | {team:<25} | {position:<5} | £{price:<9} | {points:<10} |")

    print("-" * 97)


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


def player_history(players, positions, teams):
    search = input("Enter player name: ").lower()

    matches = []
    for player in players:
        name = f"{player['first_name']} {player['second_name']}"
        if search in name.lower():
            matches.append(player)

    if len(matches) == 0:
        print("No players found!")
        return
    elif len(matches) > 1:
        print("\nMultiple players found:")
        for i, p in enumerate(matches):
            name = f"{p['first_name']} {p['second_name']}"
            print(f"{i + 1}. {name} - {teams[p['team']]}")
        choice = int(input("Choose a player: ")) - 1
        selected = matches[choice]
    else:
        selected = matches[0]

    player_id = selected['id']
    history = get_player_history(player_id)
    name = f"{selected['first_name']} {selected['second_name']}"
    print_history(history, name)