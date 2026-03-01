from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType
from database.users import add_user, total_users
from database.groups import add_group, total_groups
from config import LOG_CHANNEL_ID
import os

START_IMAGE = "Assets/start.jpeg"


@Client.on_message(filters.command("start"))
async def start_handler(client, message):

    user = message.from_user
    new_user = False

    # Save user
    if user:
        new_user = await add_user(user.id, user.first_name, user.username)

    # Save group if not private
    if message.chat.type != ChatType.PRIVATE:
        await add_group(message.chat.id, message.chat.title)

    text = (
        "🏏 **Welcome to Nex Tagger Bot**\n\n"
        "⚡ Fast • Clean • Powerful Group Tagging\n\n"
        "✨ Features:\n"
        "• Instant member tagging\n"
        "• Clean formatting\n"
        "• Safe & optimized\n\n"
        "📌 Commands:\n"
        "`/tagall` - Tag everyone\n"
        "`@all` - Quick tag\n"
        "/help - View help menu\n\n"
        "Add me to your group and start tagging 🚀"
    )

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "➕ Add Me To Group",
                    url=f"https://t.me/{client.me.username}?startgroup=true"
                )
            ],
            [
                InlineKeyboardButton(
                    "📞 Support",
                    url="https://t.me/nexorabotschat"
                ),
                InlineKeyboardButton(
                    "👑 Owner",
                    url="https://t.me/drekk_so"
                )
            ]
        ]
    )

    # Send start message
    if os.path.exists(START_IMAGE):
        await message.reply_photo(
            photo=START_IMAGE,
            caption=text,
            reply_markup=buttons
        )
    else:
        await message.reply_text(
            text,
            reply_markup=buttons
        )

    # ✅ Log ONLY if user is NEW
    if message.chat.type == ChatType.PRIVATE and new_user:
        try:
            users = await total_users()
            groups = await total_groups()

            await client.send_message(
                LOG_CHANNEL_ID,
                f"📥 **New User Started Bot**\n\n"
                f"👤 Name: {user.first_name}\n"
                f"🆔 ID: `{user.id}`\n"
                f"🔗 Username: @{user.username if user.username else 'None'}\n\n"
                f"📊 Total Users: {users}\n"
                f"👥 Total Groups: {groups}"
            )
        except Exception as e:
            print("Log Error:", e)

    # Group logging
    if message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        try:
            users = await total_users()
            groups = await total_groups()

            await client.send_message(
                LOG_CHANNEL_ID,
                f"📥 **Bot Added To Group**\n\n"
                f"🏷 Group: {message.chat.title}\n"
                f"🆔 Group ID: `{message.chat.id}`\n\n"
                f"📊 Total Users: {users}\n"
                f"👥 Total Groups: {groups}"
            )
        except Exception as e:
            print("Log Error:", e)