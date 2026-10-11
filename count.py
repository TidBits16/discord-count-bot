
'''
conn.execute(
    """
    INSERT INTO servers (server_id, max_count, user_id)
    VALUES (?, ?, ?)
    ON CONFLICT(server_id) DO UPDATE SET
        max_count = excluded.max_count,
        user_id = excluded.user_id
    WHERE excluded.max_count > servers.max_count
    """,
    (server_id, new_count, user_id),
)
conn.commit()
'''