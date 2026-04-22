# connect.py

import psycopg2
import config

def connect():
    """Open and return a connection to PostgreSQL."""
    conn = psycopg2.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASS
    )
    return conn
