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

def add_to_watchlist(player_id, name, team, position, price, points):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO watchlist (player_id, name, team, position, price, points)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (player_id, name, team, position, price, points))
        conn.commit()
        print(f"✅ {name} added to watchlist!")
    except sqlite3.IntegrityError:
        print(f"⚠️  {name} is already in your watchlist!")

def get_watchlist():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM watchlist')
    players = cursor.fetchall()

    conn.close
    return players

def remove_from_watchlist(player_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM watchlist WHERE player_id = ?', (player_id,))
    conn.commit()
    conn.close()
    print("✅ Player removed from watchlist!")