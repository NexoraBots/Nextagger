from pyrogram import Client, filters
from utils.tag_state import stop_tag, is_tag_running
from utils.mentions import make_mention
from utils.admin import is_admin
from config import ADMIN_ONLY_TAG


@Client.on_message(filters.command("cancel") & filters.group)
async def cancel_handler(client, message):

    chat_id = message.chat.id
    user = message.from_user

    if ADMIN_ONLY_TAG:
        if not await is_admin(client, chat_id, user.id):
            return await message.reply_text(
                "Only group administrators can cancel an active tagging process."
            )

    if not is_tag_running(chat_id):
        return await message.reply_text(
            "There is no active tagging process running in this group."
        )

    stop_tag(chat_id)

    admin_mention = make_mention(user)

    await message.reply_text(
        f"The tagging process has been stopped by {admin_mention}.\n\n"
        "You may start a new tagging session whenever needed."
    )