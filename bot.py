import asyncio
from pyrogram import Client
from pyrogram.enums import ParseMode
from config import API_ID, API_HASH, BOT_TOKEN

# Import handlers (we will create these next)
from handlers.start import start_handler
from handlers.help import help_handler
from handlers.tagger import tagall_handler, atall_handler
from handlers.cancel import cancel_handler

# ==============================
# 🚀 INITIALIZE BOT
# ==============================

class NexTagger(Client):

    def __init__(self):
        super().__init__(
            "nex_tagger_bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=10,
            parse_mode=ParseMode.MARKDOWN
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        print("\n==============================")
        print(f"🏏 Nex Tagger Bot Started!")
        print(f"🤖 Bot Name: {me.first_name}")
        print(f"🔗 Username: @{me.username}")
        print("==============================\n")

    async def stop(self, *args):
        print("\n🛑 Stopping Nex Tagger Bot...")
        await super().stop()


# ==============================
# 🔥 RUN BOT
# ==============================

app = NexTagger()

# Register Handlers
app.add_handler(start_handler)
app.add_handler(help_handler)
app.add_handler(tagall_handler)
app.add_handler(atall_handler)
app.add_handler(cancel_handler)

if __name__ == "__main__":
    print("⚡ Booting Nex Tagger Bot...")
    app.run()
