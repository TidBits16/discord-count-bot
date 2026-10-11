import sqlite3

# create database (if not already existing)
conn = sqlite3.connect("counts.db")
conn.row_factory = sqlite3.Row
def create_database():
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS servers (
            server_id INTEGER PRIMARY KEY,
            count_channel_id INTEGER,
            max_count INTEGER NOT NULL DEFAULT 0,
            max_count_user_id INTEGER,
            last_count_user_id INTEGER,
            current_count_number INTEGER
        )
        """
    )
    conn.commit()

# start count
def set_count_channel(server_id, channel_id):
    row = conn.execute(
        "SELECT count_channel_id FROM servers WHERE server_id = ?",
        (server_id,),
    ).fetchone()
    old = row[0] if row else None

    conn.execute(
        """
        INSERT INTO servers (server_id, count_channel_id)
        VALUES (?, ?)
        ON CONFLICT(server_id) DO UPDATE SET
            count_channel_id = excluded.count_channel_id
        """,
        (server_id, channel_id),
    )
    conn.commit()
    return old

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

# read count
def get_count(server_id):
    row = conn.execute(
        """
        SELECT count_channel_id, current_count_number, last_count_user_id
        FROM servers
        WHERE server_id = ?
        """,
        (server_id,),
    ).fetchone()
    return row

# write numbers to database
def save_success(server_id, number, user_id):
    conn.execute(
        """
        UPDATE servers
        SET current_count_number = ?, last_count_user_id = ?
        WHERE server_id = ?
        """,
        (number, user_id, server_id),
    )
    conn.commit()

# reset current number on fail
def fail_count(server_id):
    row = conn.execute(
        """
        SELECT current_count_number, last_count_user_id, max_count
        FROM servers WHERE server_id = ?
        """,
        (server_id,),
    ).fetchone()
    reached = row["current_count_number"] or 0
    record = row["max_count"]
    record_user = row["last_count_user_id"]

    if reached > record:
        record = reached
    else:
        record_user = None

    conn.execute(
        """
        UPDATE servers
        SET max_count = ?,
            max_count_user_id = COALESCE(?, max_count_user_id),
            current_count_number = NULL,
            last_count_user_id = NULL
        WHERE server_id = ?
        """,
        (record, record_user, server_id),
    )
    conn.commit()
    return record