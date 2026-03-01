active_tags = {}

def start_tag(chat_id: int):
    active_tags[chat_id] = True

def stop_tag(chat_id: int):
    active_tags.pop(chat_id, None)

def is_tag_running(chat_id: int) -> bool:
    return active_tags.get(chat_id, False)