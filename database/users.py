from database.connection import get_pool


async def add_user(user_id, first_name, username):
    pool = await get_pool()

    async with pool.acquire() as conn:

        result = await conn.fetchrow("""
            INSERT INTO users (user_id, first_name, username)
            VALUES ($1, $2, $3)
            ON CONFLICT (user_id) DO NOTHING
            RETURNING user_id
        """, user_id, first_name, username)

        # If inserted → new user
        if result:
            return True

        # If already exists → update info
        await conn.execute("""
            UPDATE users
            SET first_name = $2,
                username = $3
            WHERE user_id = $1
        """, user_id, first_name, username)

        return False


async def total_users():
    pool = await get_pool()

    async with pool.acquire() as conn:
        return await conn.fetchval(
            "SELECT COUNT(*) FROM users"
        )