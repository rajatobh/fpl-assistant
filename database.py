import sqlite3

def get_connection():
    conn = sqlite3.connect('fpl.db')
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER UNIQUE,
            name TEXT,
            team TEXT,
            position TEXT,
            price REAL,
            points INTEGER
        )
    ''')

    conn.commit()
    conn.close()

