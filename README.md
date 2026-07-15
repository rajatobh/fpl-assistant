# FPL Assistant

A command-line tool to explore Fantasy Premier League player data.

## Features
- Search players by name
- Filter by position and budget
- Sort by points or price
- View top 10 picks by position

## Setup
```bash
git clone https://github.com/rajatobh/fpl-assistant.git
cd fpl-assistant
python -m venv venv
source venv/bin/activate
pip install requests
python main.py
```

## Data
Live data pulled from the official FPL API — no authentication required.

## Project Structure
- `main.py` — menu and startup
- `api.py` — FPL API calls
- `display.py` — table formatting
- `actions.py` — user interactions
- `database.py` — watchlist persistence