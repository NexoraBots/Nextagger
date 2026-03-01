import os

API_ID = int(os.getenv("API_ID", "35064036"))
API_HASH = os.getenv("API_HASH", "c9a901b08789b91eae4097ba2dcc086c")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8401717875:AAGG7jbYldioblzUkcLUBa3ct9rzSyWHXeQ")


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://neondb_owner:npg_yNzl0oqVOw4M@ep-billowing-frost-a186v8hy.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)


LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", "-1003692127639"))


TAGS_PER_MESSAGE = 5
TAG_DELAY = 2  # seconds between batches
DEFAULT_EMOJI = "🏏"

OWNER_ID = 8294062042
ADMIN_ONLY_TAG = True  # Only admins can use /tagall
