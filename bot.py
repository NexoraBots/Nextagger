from pyrogram import Client
from pyrogram.enums import ParseMode

from config import API_ID, API_HASH, BOT_TOKEN
from database.connection import connect_db
from database.init import init_db


class NexTagger(Client):

    def __init__(self):
        super().__init__(
            "nex_tagger_bot",
            bot_token=BOT_TOKEN,
            api_id=API_ID,
            api_hash=API_HASH,
            workers=50,
            parse_mode=ParseMode.MARKDOWN,
            plugins=dict(root="plugins")
        )

    async def start(self):
        await super().start()

        await connect_db()
        await init_db()

        me = await self.get_me()

        print()
        print("🏏 Nex Tagger Bot Started")
        print(f"🤖 Name: {me.first_name}")
        print(f"🔗 Username: @{me.username}")
        print()

    async def stop(self, *args):
        print("🛑 Shutting down Nex Tagger Bot...")
        await super().stop()


bot = NexTagger()


if __name__ == "__main__":
    print("⚡ Booting Nex Tagger Bot...")
    bot.run()