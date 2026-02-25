from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

# Track active tagging sessions per chat
active_sessions = {}


def set_active(chat_id: int, active: bool):
    active_sessions[chat_id] = active


def is_active(chat_id: int) -> bool:
    return active_sessions.get(chat_id, False)


async def cancel_command(client: Client, message: Message):
    chat_id = message.chat.id
    if is_active(chat_id):
        set_active(chat_id, False)
        await message.reply_text("**Tagging cancelled!**")
    else:
        await message.reply_text("No active tagging session to cancel.")


cancel_handler = MessageHandler(cancel_command, filters.command("cancel") & filters.group)
