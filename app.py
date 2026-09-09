from fastapi import FastAPI
from api import get_bootstrap_data
from database import create_tables, add_to_watchlist, get_watchlist, remove_from_watchlist
from pydantic import BaseModel

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

@app.get("/players/top")
def get_top_players(position: str, limit: int = 10):
    filtered = []

    for player in players:
        position_name = positions[player['element_type']]
        if position_name != position.upper():
            continue

        name = f"{player['first_name']} {player['second_name']}"
        price_value = player['now_cost'] / 10
        team = teams[player['team']]
        points = player['total_points']
        value = round(points / price_value, 1) if price_value > 0 else 0

        filtered.append({
            "name": name,
            "team": team,
            "position": position_name,
            "price": price_value,
            "points": points,
            "value": value
        })

    filtered.sort(key=lambda x: x['points'], reverse=True)

    return {"position": position.upper(), "players": filtered[:limit]}

class WatchlistPlayer (BaseModel):
    player_id: int
    name: str
    team: str
    position: str
    price: float
    points: int

@app.get("/watchlist")
def view_watchlist():
    players = get_watchlist()
    result = []
    for player in players:
        _, player_id, name, team, position, price, points = player
        result.append({
            "player_id": player_id,
            "name": name,
            "team": team,
            "position": position,
            "price": price,
            "points": points
        })
    return {"count": len(result), "players": result}

@app.post("/watchlist")
def add_player_to_watchlist(player: WatchlistPlayer):
    add_to_watchlist(player.player_id, player.name, player.team, player.position, player.price, player.points)
    return {"message": f"{player.name} added to watchlist!"}

@app.delete("/watchlist/{player_id}")
def remove_player_from_watchlist(player_id: int, player_name: str):
    remove_from_watchlist(player_id)
    return {"message": f"{player_name} removed from watchlist!"}

@app.get("/players/search")
def search_players(name: str):
    results = []

    for player in players:
        full_name = f"{player['first_name']} {player['second_name']}"
        if name.lower() in full_name.lower():
            position_name = positions[player['element_type']]
            price_value = player['now_cost'] / 10
            team = teams[player['team']]
            points = player['total_points']
            value = round(points / price_value, 1) if price_value > 0 else 0

            results.append({
                "name": full_name,
                "team": team,
                "position": position_name,
                "price": price_value,
                "points": points,
                "value": value
            })

    return {"count": len(results), "players": results}
