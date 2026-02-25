from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message


async def start_command(client: Client, message: Message):
    await message.reply_text(
        "**Welcome to NexTagger Bot!**\n\n"
        "I can help you tag all members in a group.\n\n"
        "Use /help to see available commands."
    )


start_handler = MessageHandler(start_command, filters.command("start") & filters.group)
