from database.connection import get_pool

async def add_group(chat_id, title):
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO groups (chat_id, title)
            VALUES ($1, $2)
            ON CONFLICT (chat_id)
            DO UPDATE SET title = EXCLUDED.title
        """, chat_id, title)

async def total_groups():
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.fetchval("SELECT COUNT(*) FROM groups")