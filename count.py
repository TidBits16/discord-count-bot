def check_count(current, last_user_id, user_id, text):
    digits = "".join(ch for ch in text if ch in "0123456789")
    if digits == "":
        return "ignore", None, None
    number = int(digits)
    expected = 1 if current is None else current + 1
    if number != expected or user_id == last_user_id:
        return "fail", None, None
    return "ok", number, user_id
