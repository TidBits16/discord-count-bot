def check_count(current, last_user_id, user_id, text):
    expected = 1 if current is None else current + 1
    try:
        number = int(text.strip())
    except ValueError:
        return "fail", None, None
    if number != expected or user_id == last_user_id:
        return "fail", None, None
    return "ok", number, user_id