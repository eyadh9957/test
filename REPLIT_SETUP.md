# Replit Setup Guide

## 🚀 Host Your Discord Bot on Replit (Free!)

Replit is perfect for hosting Discord bots. It's free and easy!

### Step 1: Create Replit Account

1. Go to [Replit.com](https://replit.com)
2. Sign up (free account)
3. Verify email

### Step 2: Import Your Repository

1. Click "Create" → "Import from GitHub"
2. Paste: `https://github.com/siddhartrathi/quest-completer-bot`
3. Choose language: **Python**
4. Click "Import from GitHub"

### Step 3: Create .env File on Replit

1. In Replit file explorer, click **"+ Add File"**
2. Name it: `.env`
3. Paste this (with your values):
```env
DISCORD_TOKEN=your_bot_token_here
DISCORD_USER_TOKEN=your_user_token_here
COMMAND_PREFIX=!
DATABASE_URL=sqlite:///./quest_bot.db
ENCRYPTION_KEY=your_encryption_key_here
BOT_OWNER_ID=your_discord_user_id
LOG_LEVEL=INFO
REQUEST_TIMEOUT=30
MAX_RETRIES=3
```

### Step 4: Get Your Discord Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create New Application (or select existing)
3. Go to "Bot" section
4. Click "Add Bot"
5. Under TOKEN, click "Copy"
6. Paste in `.env` as `DISCORD_TOKEN`

### Step 5: Get Encryption Key

1. Click "Run" button at top
2. Wait for terminal to open
3. In terminal, run:
```bash
python -c "from utils.encryption import TokenEncryption; print(TokenEncryption.generate_key())"
```
4. Copy the output
5. Paste in `.env` as `ENCRYPTION_KEY`

### Step 6: Complete .env File

Edit `.env` with:
- `DISCORD_TOKEN` - Your bot token (from step 4)
- `DISCORD_USER_TOKEN` - Can be anything for now (e.g., "bot")
- `ENCRYPTION_KEY` - From step 5
- `BOT_OWNER_ID` - Your Discord user ID

### Step 7: Run the Bot

1. In Replit terminal, run:
```bash
python bot/main.py
```

2. You should see:
```
✅ Configuration loaded successfully
✅ Database initialized successfully
✅ Loaded cog: quest_commands
✅ BotName#1234 has connected to Discord!
```

### Step 8: Invite Bot to Your Server

1. [OAuth2 URL Generator](https://discord.com/developers/applications)
2. Select your bot application
3. Go to "OAuth2" → "URL Generator"
4. **Scopes**: Select `bot`
5. **Permissions**: Select:
   - ✅ Send Messages
   - ✅ Embed Links
   - ✅ Read Message History
6. Copy generated URL
7. Open URL in browser
8. Select your server and click "Authorize"

### Step 9: Keep Bot Running 24/7

**Option 1: Replit's Always On (Paid)**
- Go to Replit dashboard
- Click your repl
- Go to Settings → Autostop → Disable
- Need Replit premium (~$7/month)

**Option 2: Use UptimeRobot (Free!)**

This keeps your bot alive for free:

1. Get your Replit URL:
   - In Replit, click "Run"
   - Copy the URL from browser address bar
   - It looks like: `https://your-username-replit.repl.co`

2. Go to [UptimeRobot.com](https://uptimerobot.com)
3. Sign up (free)
4. Click "Create Monitor"
5. Set:
   - **Type**: HTTP(s)
   - **Friendly Name**: Quest Bot
   - **URL**: Your Replit URL
   - **Interval**: 5 minutes
6. Click "Create Monitor"

This will ping your Replit app every 5 minutes, keeping it alive!

### Step 10: Test Commands

In your Discord server, type:
```
/link
/info
/start
/progress
```

## 📋 Checklist

- ✅ Replit account created
- ✅ Repository imported
- ✅ `.env` file created with tokens
- ✅ Bot running (test with `/info`)
- ✅ Bot invited to server
- ✅ UptimeRobot configured (for 24/7)

## 🆘 Troubleshooting

**Bot doesn't respond**
- Click "Run" again
- Check `.env` has correct tokens
- Make sure bot has permissions in server

**"Token required" error**
- Check all tokens in `.env`
- Make sure no quotes unless needed

**Bot stops after a while**
- Replit spins down inactive repls
- Use UptimeRobot to keep it alive

**Can't see database**
- Click "Files" icon (left sidebar)
- Look for `quest_bot.db`
- It's created automatically when bot runs

## 📁 File Structure on Replit

```
quest-completer-bot/
├── .env              ← Your secrets (not visible in GitHub)
├── bot/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   └── cogs/
├── utils/
├── requirements.txt
├── .gitignore
└── quest_bot.db      ← Created automatically
```

## 💡 Tips

1. **Monitor logs**: Click "Run" and watch terminal for errors
2. **Check database**: `quest_bot.db` appears in Files after first run
3. **Restart bot**: Click "Stop" then "Run" again
4. **Update code**: Just edit files and restart
5. **Database backup**: Download `quest_bot.db` from Files periodically

## 🔗 Useful Links

- [Replit Discord Docs](https://docs.replit.com/tutorials/06-discord-bot)
- [Discord.py Docs](https://discordpy.readthedocs.io/)
- [UptimeRobot](https://uptimerobot.com)

---

**Your bot is now hosted on Replit!** 🎉

Share the Discord invite link with your server members so they can use the bot! 🚀
