import asyncio
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from config import TAGS_PER_MESSAGE, TAG_DELAY, DEFAULT_EMOJI, ADMIN_ONLY_TAG
from handlers.cancel import set_active, is_active


async def is_admin(client: Client, chat_id: int, user_id: int) -> bool:
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status.value in ("administrator", "owner", "creator")
    except Exception:
        return False


async def tagall_command(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if ADMIN_ONLY_TAG and not await is_admin(client, chat_id, user_id):
        await message.reply_text("**Only admins can use this command.**")
        return

    if is_active(chat_id):
        await message.reply_text("**A tagging session is already active. Use /cancel to stop it.**")
        return

    set_active(chat_id, True)
    await message.reply_text("**Starting to tag all members...**")

    members = []
    try:
        async for member in client.get_chat_members(chat_id):
            if not member.user.is_bot and not member.user.is_deleted:
                members.append(member.user)
    except Exception as e:
        set_active(chat_id, False)
        await message.reply_text(f"**Error fetching members:** {e}")
        return

    batch = []
    for i, user in enumerate(members):
        if not is_active(chat_id):
            break

        mention = f"[{DEFAULT_EMOJI}](tg://user?id={user.id})"
        batch.append(mention)

        if len(batch) >= TAGS_PER_MESSAGE:
            try:
                await message.reply_text(" ".join(batch))
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await message.reply_text(" ".join(batch))
            except Exception:
                pass
            batch = []
            await asyncio.sleep(TAG_DELAY)

    if batch and is_active(chat_id):
        try:
            await message.reply_text(" ".join(batch))
        except Exception:
            pass

    set_active(chat_id, False)
    await message.reply_text("**Done! All members tagged.**")


async def atall_command(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if ADMIN_ONLY_TAG and not await is_admin(client, chat_id, user_id):
        await message.reply_text("**Only admins can use this command.**")
        return

    if is_active(chat_id):
        await message.reply_text("**A tagging session is already active. Use /cancel to stop it.**")
        return

    set_active(chat_id, True)
    await message.reply_text("**Starting to tag all members with @mentions...**")

    members = []
    try:
        async for member in client.get_chat_members(chat_id):
            if not member.user.is_bot and not member.user.is_deleted:
                members.append(member.user)
    except Exception as e:
        set_active(chat_id, False)
        await message.reply_text(f"**Error fetching members:** {e}")
        return

    batch = []
    for user in members:
        if not is_active(chat_id):
            break

        if user.username:
            mention = f"@{user.username}"
        else:
            mention = f"[{user.first_name}](tg://user?id={user.id})"
        batch.append(mention)

        if len(batch) >= TAGS_PER_MESSAGE:
            try:
                await message.reply_text(" ".join(batch))
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await message.reply_text(" ".join(batch))
            except Exception:
                pass
            batch = []
            await asyncio.sleep(TAG_DELAY)

    if batch and is_active(chat_id):
        try:
            await message.reply_text(" ".join(batch))
        except Exception:
            pass

    set_active(chat_id, False)
    await message.reply_text("**Done! All members tagged.**")


tagall_handler = MessageHandler(tagall_command, filters.command("tagall") & filters.group)
atall_handler = MessageHandler(atall_command, filters.command("atall") & filters.group)
