# Quest Completer Bot - Multi-User Server Bot

A Discord bot that allows all server members to link their own Discord tokens and auto-complete their quests.

## Features

- 🔐 **Per-User Token Storage** - Each user securely stores their own Discord token
- 🎯 **Individual Quest Completion** - Every user auto-completes their own quests
- 📊 **Shared Dashboard** - View all active sessions and global stats
- 🔄 **Auto-Complete Loop** - Quests completed every 5 minutes per user
- 👥 **Multi-User Support** - Entire server can use the bot
- 🛡️ **Secure Storage** - Tokens encrypted in database
- ⚡ **Fast & Async** - Non-blocking quest completion

## Setup

### Quick Start
```bash
# 1. Clone repo
git clone https://github.com/siddhartrathi/quest-completer-bot.git
cd quest-completer-bot

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup configuration
cp .env.example .env
# Edit .env with your Discord Bot Token

# 5. Run bot
python bot/main.py
```

See [QUICKSTART.md](QUICKSTART.md) for detailed setup.

## Commands (Everyone can use)

| Command | Description |
|---------|-------------|
| `/link` | Link your Discord token to enable quest completion |
| `/start` | Start auto-completing YOUR quests (every 5 min) |
| `/stop` | Stop your quest completion |
| `/complete_now` | Complete all YOUR quests right now |
| `/progress` | View YOUR quest completion stats |
| `/info` | View global server dashboard & all active sessions |

## How It Works

1. **User links token** → `/link`
2. **User starts completer** → `/start`
3. **Bot fetches their quests** → Every 5 minutes
4. **Bot completes them** → All their available quests
5. **User checks progress** → `/progress` or `/info`

## Example Usage

```
User1: /link
✅ Token linked for User1

User1: /start
✅ Started auto-completing for User1

User2: /link
✅ Token linked for User2

User2: /start
✅ Started auto-completing for User2

Anyone: /info
📊 Dashboard shows:
   - User1: 45 quests completed ✅
   - User2: 32 quests completed ✅
   - Bot Status: Online
   - Active Users: 2
```

## Database Schema

### Users Table
- discord_id (unique)
- username
- encrypted_token
- created_at
- is_active

### Sessions Table
- user_id (linked to Users)
- started_at
- ended_at
- quests_completed
- status (active/paused/stopped)

### QuestLog Table
- user_id
- quest_name
- reward
- completed_at

## Security

✅ Tokens encrypted in database  
✅ Each user's data isolated  
✅ Never stored in plain text  
✅ Keep `.env` file secret  
✅ Don't commit `.env` to GitHub  

## Troubleshooting

**"Token not linked" error**
- Use `/link` first before `/start`

**Bot not completing quests**
- Check your user token is correct
- Make sure you ran `/link` and `/start`
- Check bot logs for errors

**"Already running" error**
- Quest completion already active for you
- Use `/stop` first, then `/start` again

## Admin Commands (Optional)

Add these later if needed:
- `/admin stats` - View all users and their stats
- `/admin clear <user>` - Remove user's token
- `/admin broadcast <message>` - Send message to all

## License

MIT
