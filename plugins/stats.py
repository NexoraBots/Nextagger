from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import OWNER_ID
from database.users import total_users
from database.groups import total_groups
from database.stats import total_tags


@Client.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats_handler(client, message):

    users = await total_users()
    groups = await total_groups()
    tags = await total_tags()

    bot = await client.get_me()

    text = (
        f"Bot Statistics\n\n"
        f"Bot Name : {bot.first_name}\n"
        f"Username : @{bot.username}\n"
        f"Bot ID : `{bot.id}`\n\n"
        f"Users : {users}\n"
        f"Groups : {groups}\n"
        f"Total Tag Processes : {tags}\n\n"
        f"System Status : Running\n"
    )

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Add Bot To Group",
                    url=f"https://t.me/{bot.username}?startgroup=true"
                )
            ]
        ]
    )

    await message.reply_text(
        text,
        reply_markup=buttons,
        disable_web_page_preview=True
    )