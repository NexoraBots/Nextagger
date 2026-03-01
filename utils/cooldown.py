import time

cooldowns = {}

def check_cooldown(chat_id: int, seconds: int) -> bool:
    now = time.time()
    last = cooldowns.get(chat_id)

    if last and now - last < seconds:
        return False

    cooldowns[chat_id] = now
    return True