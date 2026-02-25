from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message


async def help_command(client: Client, message: Message):
    await message.reply_text(
        "**NexTagger Bot - Help**\n\n"
        "**Commands:**\n"
        "/tagall - Tag all members in the group\n"
        "/atall - Tag all members with @mention\n"
        "/cancel - Cancel ongoing tagging\n"
        "/help - Show this help message\n\n"
        "**Note:** Admin permission required to use tag commands."
    )


help_handler = MessageHandler(help_command, filters.command("help") & filters.group)
