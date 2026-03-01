import asyncio
from pyrogram.errors import FloodWait

async def safe_send(client, chat_id, text):
    try:
        return await client.send_message(chat_id, text)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await client.send_message(chat_id, text)