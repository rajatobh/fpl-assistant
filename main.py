from api import get_bootstrap_data
from database import create_tables
from actions import (
    search_players,
    top_picks,
    save_to_watchlist,
    view_watchlist,
    delete_from_watchlist,
    player_history
)

# Load data
data = get_bootstrap_data()
players = data['elements']
positions = {t['id']: t['singular_name_short'] for t in data['element_types']}
teams = {t['id']: t['name'] for t in data['teams']}

# Setup database
create_tables()

# Menu
while True:
    print("\n--- FPL Assistant ---")
    print("1. Search players")
    print("2. Top picks by position")
    print("3. Add player to watchlist")
    print("4. View watchlist")
    print("5. Remove from watchlist")
    print("6. Player gameweek history")
    print("7. Exit")

    choice = input("\nChoose an option: ")

    if choice == "1":
        search_players(players, positions, teams)
    elif choice == "2":
        top_picks(players, positions, teams)
    elif choice == "3":
        save_to_watchlist(players, positions, teams)
    elif choice == "4":
        view_watchlist()
    elif choice == "5":
        delete_from_watchlist()
    elif choice == "6":
        player_history(players, positions, teams)
    elif choice == "7":
        print("Goodbye!")
        break
    else:
        print("Invalid option, try again.")