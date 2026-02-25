# NexTagger Bot

A Telegram group tagging bot built with Pyrogram. It allows admins to tag all members in a Telegram group.

## Architecture

- **Language**: Python 3.12
- **Framework**: Pyrogram (Telegram MTProto)
- **Database**: PostgreSQL (Neon hosted, via asyncpg)
- **Runtime**: Single-process async bot

## Project Structure

```
bot.py          - Main entry point, bot initialization and handler registration
config.py       - Configuration (API keys, database URL, tag settings)
requirements.txt - Python dependencies
handlers/
  __init__.py   - Package init
  start.py      - /start command handler
  help.py       - /help command handler
  tagger.py     - /tagall and /atall command handlers
  cancel.py     - /cancel command handler + session tracking
database/
  __init__.py   - Database package (placeholder)
```

## Configuration

Environment variables (with defaults in config.py):
- `API_ID` - Telegram API ID
- `API_HASH` - Telegram API Hash
- `BOT_TOKEN` - Bot token from @BotFather
- `DATABASE_URL` - PostgreSQL connection string
- `LOG_CHANNEL_ID` - Telegram channel ID for logs

## Running

The bot runs as a console workflow: `python bot.py`

## Features

- `/tagall` - Tags all group members using inline mentions
- `/atall` - Tags all group members using @username or inline mention
- `/cancel` - Cancels an ongoing tagging session
- `/start` - Welcome message
- `/help` - Help information
- Admin-only restriction configurable via `ADMIN_ONLY_TAG`
- Configurable tags per message, delay, and emoji via config.py
