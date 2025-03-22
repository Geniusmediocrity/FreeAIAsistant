def split_message(message: str, limit=4096):
    """Разбивает текст на части, не превышающие limit."""
    return [message[i: i+limit] for i in range(0, len(message), limit)]