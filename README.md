# FPL Assistant

A Fantasy Premier League tool built in Python with a CLI interface and REST API.

## Features
- Search players by name, position, and budget
- Sort players by points, price, or value
- View top picks by position
- View player gameweek history
- Create personal watchlist (add, view, remove)
- REST API built with FastAPI

## Project Structure
- `main.py` — CLI menu and startup
- `app.py` — FastAPI REST API
- `api.py` — FPL API calls
- `display.py` — table formatting
- `actions.py` — user interactions
- `database.py` — watchlist persistence

## Setup
```bash
git clone https://github.com/rajatobh/fpl-assistant.git
cd fpl-assistant
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
## Run the CLI
```bash
python main.py
```

## Run the API
```bash
uvicorn app:app --reload
```

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /players | Get all players with optional filters |
| GET | /players/top | Top picks by position |
| GET | /players/search | Search players by name |
| GET | /players/{id}/history | Player gameweek history |
| GET | /watchlist | View watchlist |
| POST | /watchlist | Add player to watchlist |
| DELETE | /watchlist/{id} | Remove player from watchlist |

## Data
Live data pulled from the official FPL API — no authentication required.
