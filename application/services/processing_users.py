from application.services.generate_users import generate_users


def format_users(amount: int = 100) -> list:
    users = generate_users(amount)
    list_of_users = []
    for user in users:
        username = user.username
        email = user.email
        list_of_users.append(f"<li><b>{username}</b> - <span>{email}</span></li>")
    return list_of_users


def output_user_info(users_dict: list) -> str:
    return "\n".join(users_dict)
