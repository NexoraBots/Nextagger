from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType
import os


HELP_IMAGE = "Assets/start.jpeg"


@Client.on_message(filters.command("help"))
async def help_handler(client, message):

    text = (
        "📖 **Nex Tagger Bot Help Menu**\n\n"
        "🏏 **Tagging Commands**\n"
        "`/tagall` - Tag all members\n"
        "`/tagall message` - Tag with custom message\n"
        "`@all` - Quick tag trigger\n"
        "`/cancel` - Stop ongoing tagging\n\n"
        "⚙️ Admin Only: Tagging commands work only for group admins.\n\n"
        "⚡ Fast • Clean • Optimized"
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
                    url="https://t.me/YourSupportUsername"
                ),
                InlineKeyboardButton(
                    "👑 Owner",
                    url="https://t.me/YourOwnerUsername"
                )
            ]
        ]
    )

    if os.path.exists(HELP_IMAGE):
        await message.reply_photo(
            photo=HELP_IMAGE,
            caption=text,
            reply_markup=buttons
        )
    else:
        await message.reply_text(
            text,
            reply_markup=buttons
        )