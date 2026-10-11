import sqlite3

# create database (if not already existing)
conn = sqlite3.connect("counts.db")
def create_database():
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS servers (
            server_id INTEGER PRIMARY KEY,
            max_count INTEGER NOT NULL DEFAULT 0,
            max_count_user_id   INTEGER
        )
        """
    )
    conn.commit()

# adding servers to the server table
def add_server(server_id):
    conn.execute(
        "INSERT OR IGNORE INTO servers (server_id) VALUES (?)",
        (server_id,),
    )
    conn.commit()

# remove servers from the server table
def remove_server(server_id):
    conn.execute(
        "DELETE FROM servers WHERE server_id = ?",
        (server_id,),
    )
    conn.commit()