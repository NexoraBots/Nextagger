from database.connection import get_pool


async def add_user(user_id, first_name, username):
    pool = await get_pool()

    async with pool.acquire() as conn:
        result = await conn.fetchrow(
            """
            INSERT INTO users (user_id, first_name, username)
            VALUES ($1, $2, $3)
            ON CONFLICT (user_id)
            DO UPDATE SET
                first_name = EXCLUDED.first_name,
                username = EXCLUDED.username
            RETURNING (xmax = 0) AS inserted
            """,
            user_id,
            first_name,
            username
        )

        return result["inserted"]


async def total_users():
    pool = await get_pool()

    async with pool.acquire() as conn:
        count = await conn.fetchval(
            "SELECT COUNT(*) FROM users"
        )

        return count or 0
