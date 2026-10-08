def attach_orders_to_users(users: list[dict], orders: list[dict]) -> list[dict]:
    result = []
    for user in users:
        user_orders = []
        for order in orders:
            if order["user_id"] == user["id"]:
                user_orders.append(order)
        result.append({"user": user, "orders": user_orders})
    return result
