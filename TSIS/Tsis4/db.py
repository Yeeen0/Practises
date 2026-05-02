import psycopg2
from config import DB_PARAMS

def get_connection():
    try:
        return psycopg2.connect(**DB_PARAMS)
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL
        );
        CREATE TABLE IF NOT EXISTS game_sessions (
            id SERIAL PRIMARY KEY,
            player_id INTEGER REFERENCES players(id),
            score INTEGER NOT NULL,
            level_reached INTEGER NOT NULL,
            played_at TIMESTAMP DEFAULT NOW()
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def save_score(username, score, level):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING RETURNING id;", (username,))
    res = cur.fetchone()
    if res:
        player_id = res[0]
    else:
        cur.execute("SELECT id FROM players WHERE username = %s;", (username,))
        player_id = cur.fetchone()[0]

    cur.execute("INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s);",
                (player_id, score, level))
    conn.commit()
    cur.close()
    conn.close()

def get_top_10():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.username, s.score, s.level_reached, TO_CHAR(s.played_at, 'YYYY-MM-DD HH24:MI')
        FROM game_sessions s
        JOIN players p ON s.player_id = p.id
        ORDER BY s.score DESC
        LIMIT 10;
    """)
    top10 = cur.fetchall()
    cur.close()
    conn.close()
    return top10

def get_personal_best(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT MAX(s.score)
        FROM game_sessions s
        JOIN players p ON s.player_id = p.id
        WHERE p.username = %s;
    """, (username,))
    res = cur.fetchone()
    cur.close()
    conn.close()
    return res[0] if res and res[0] is not None else 0