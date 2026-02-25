from database.connection import get_pool

async def increment_tag_count(chat_id):
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO tag_stats (chat_id, total_tags)
            VALUES ($1, 1)
            ON CONFLICT (chat_id)
            DO UPDATE SET total_tags = tag_stats.total_tags + 1
        """, chat_id)

async def get_tag_count(chat_id):
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.fetchval("""
            SELECT total_tags FROM tag_stats
            WHERE chat_id = $1
        """, chat_id)