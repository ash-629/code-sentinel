def load_user_orders(connection, user_ids):
    results = []
    for user_id in user_ids:
        user = connection.execute(
            f"SELECT * FROM users WHERE id = {user_id}"
        ).fetchone()
        orders = connection.execute(
            f"SELECT * FROM orders WHERE user_id = {user_id}"
        ).fetchall()
        results.append({"user": user, "orders": orders})
    return results
