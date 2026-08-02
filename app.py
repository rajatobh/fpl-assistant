from fastapi import FastAPI
from api import get_bootstrap_data
from database import create_tables

app = FastAPI(title="FPL Assistant API")

# Load data on startup
data = get_bootstrap_data()
players = data['elements']
positions = {t['id']: t['singular_name_short'] for t in data['element_types']}
teams = {t['id']: t['name'] for t in data['teams']}

# Setup database
create_tables()

@app.get("/")
def root():
    return {"message": "Welcome to FPL Assistant API"}

@app.get("/players")
def get_players(position: str = None, max_price: float = None, sort_by: str = None):
    filtered = []

    for player in players:
        name = f"{player['first_name']} {player['second_name']}"
        position_name = positions[player['element_type']]
        price_value = player['now_cost'] / 10
        team = teams[player['team']]
        points = player['total_points']
        value = round(points / price_value, 1) if price_value > 0 else 0

        if position and position_name != position.upper():
            continue
        if max_price and price_value > max_price:
            continue

        filtered.append({
            "name": name,
            "team": team,
            "position": position_name,
            "price": price_value,
            "points": points,
            "value": value
        })

    if sort_by == "points":
        filtered.sort(key=lambda x: x['points'], reverse=True)
    elif sort_by == "price":
        filtered.sort(key=lambda x: x['price'], reverse=True)
    elif sort_by == "value":
        filtered.sort(key=lambda x: x['value'], reverse=True)

    return {"count": len(filtered), "players": filtered}