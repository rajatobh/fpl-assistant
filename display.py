DIVIDER = "-" * 110

def print_players(filtered_players, positions, teams):
    print(DIVIDER)
    print(f"| {'Name':<30} | {'Team':<25} | {'Pos':<5} | {'Price':<10} | {'Points':<10} | {'Value':<8} |")
    print(DIVIDER)
    for player in filtered_players:
        name = f"{player['first_name']} {player['second_name']}"
        position = positions[player['element_type']]
        price_value = player['now_cost'] / 10
        team = teams[player['team']]
        price = f"£{price_value}m"
        points = player['total_points']
        value = round(points / price_value, 1) if price_value > 0 else 0
        print(f"| {name:<30} | {team:<25} | {position:<5} | {price:<10} | {points:<10} | {value:<8} |")
    print(DIVIDER)

def print_history(history, name):
    print(f"\n--- Gameweek History: {name} ---")
    print("-" * 60)
    print(f"| {'GW':<5} | {'Points':<10} | {'Price':<10} | {'Goals':<8} | {'Assists':<8} |")
    print("-" * 60)

    total_points = 0
    for gw in history:
        print(f"| {gw['round']:<5} | {gw['total_points']:<10} | £{gw['value']/10:<9} | {gw['goals_scored']:<8} | {gw['assists']:<8} |")
        total_points += gw['total_points']

    print("-" * 60)
    print(f"Total Points: {total_points}")
