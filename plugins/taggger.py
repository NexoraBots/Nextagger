import asyncio
import time
from pyrogram import Client, filters
from pyrogram.errors import FloodWait

from config import TAGS_PER_MESSAGE, TAG_DELAY, ADMIN_ONLY_TAG
from utils.admin import is_admin
from utils.mentions import make_mention
from utils.tag_state import start_tag, stop_tag, is_tag_running
from utils.sender import safe_send
from database.stats import increment_tag_count


# Cooldown storage (per group)
tag_cooldowns = {}


def is_on_cooldown(chat_id, seconds=30):
    now = time.time()
    if chat_id in tag_cooldowns:
        if tag_cooldowns[chat_id] > now:
            return True
    return False


def set_cooldown(chat_id, seconds=30):
    tag_cooldowns[chat_id] = time.time() + seconds


async def process_tagging(client, message, custom_text=None):

    chat_id = message.chat.id
    user = message.from_user

    # 🚫 Block if already running
    if is_tag_running(chat_id):
        return await message.reply_text(
            "A tagging process is already running in this group. Please wait until it finishes."
        )

    # 🚫 Block if cooldown active
    if is_on_cooldown(chat_id, 30):
        return await message.reply_text(
            "Please wait 30 seconds before starting tagging again."
        )

    # Admin check
    if ADMIN_ONLY_TAG:
        if not await is_admin(client, chat_id, user.id):
            return await message.reply_text(
                "Only group administrators can use this command."
            )

    # Start tagging
    start_tag(chat_id)

    admin_mention = make_mention(user)

    await message.reply_text(
        f"Tagging process started by {admin_mention}.\n\n"
        "Members are being mentioned..."
    )

    total_tagged = 0
    batch = []

    try:
        async for member in client.get_chat_members(chat_id):

            if not is_tag_running(chat_id):
                break

            if member.user.is_bot:
                continue

            mention = make_mention(member.user)
            batch.append(mention)
            total_tagged += 1

            if len(batch) == TAGS_PER_MESSAGE:

                text = " ".join(batch)

                if custom_text:
                    text = f"{custom_text}\n\n{text}"

                try:
                    await safe_send(client, chat_id, text)
                    await increment_tag_count(chat_id)

                except FloodWait as e:
                    await asyncio.sleep(e.value)

                batch.clear()
                await asyncio.sleep(TAG_DELAY)

        # Send remaining users
        if batch and is_tag_running(chat_id):

            text = " ".join(batch)

            if custom_text:
                text = f"{custom_text}\n\n{text}"

            await safe_send(client, chat_id, text)

    finally:
        # Always stop safely
        stop_tag(chat_id)

        # ⏳ Start 30 sec cooldown AFTER completion
        set_cooldown(chat_id, 30)

        await message.reply_text(
            f"Tagging completed successfully.\n\n"
            f"Started by {admin_mention}\n"
            f"Total users tagged: {total_tagged}\n\n"
            f"Next tagging available after 30 seconds."
        )


@Client.on_message(filters.command("tagall") & filters.group)
async def tagall_handler(client, message):

    custom_text = None

    if len(message.command) > 1:
        custom_text = message.text.split(None, 1)[1]

    await process_tagging(client, message, custom_text)


@Client.on_message(filters.regex(r"^@all$") & filters.group)
async def atall_handler(client, message):
    await process_tagging(client, message)