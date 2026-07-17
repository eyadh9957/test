# Quick Start - Multi-User Server Bot

## 🚀 Setup (10 minutes)

### Step 1: Get Discord Bot Token
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Go to "Bot" → "Add Bot"
4. Under TOKEN, click "Copy"
5. Keep this safe! (It's your `DISCORD_TOKEN`)

### Step 2: Clone & Install
```bash
git clone https://github.com/siddhartrathi/quest-completer-bot.git
cd quest-completer-bot
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### Step 3: Configure Bot
```bash
cp .env.example .env
```

Edit `.env`:
```env
DISCORD_TOKEN=paste_your_bot_token_here
DISCORD_USER_TOKEN=anything  # This is for bot, not users
BOT_OWNER_ID=your_discord_id
ENCRYPTION_KEY=generate_below
```

**Generate Encryption Key:**
```bash
python -c "from utils.encryption import TokenEncryption; print(TokenEncryption.generate_key())"
```

Copy output and paste as `ENCRYPTION_KEY` in `.env`

### Step 4: Run Bot
```bash
python bot/main.py
```

You should see:
```
✅ Loaded cog: quest_commands
✅ BotName#1234 has connected to Discord!
✅ Synced X command(s)
```

### Step 5: Invite Bot to Server
1. [OAuth2 Generator](https://discord.com/developers/applications)
2. Select your bot
3. Go to "OAuth2" → "URL Generator"
4. Scopes: `bot`
5. Permissions: 
   - ✅ Send Messages
   - ✅ Embed Links
   - ✅ Read Message History
6. Copy URL and open in browser
7. Select your server and invite

### Step 6: Test Commands

In your Discord server, type:
```
/link
/info
/start
```

## 📖 User Guide

### For Your Server Members:

**1. Link Their Account:**
```
/link
```
Response: ✅ Token Linked

**2. Start Auto-Completing:**
```
/start
```
Response: ✅ Quest Completion Started
- Quests will be completed every 5 minutes
- They can leave it running

**3. Check Progress:**
```
/progress
```
Shows:
- Quests completed
- Rewards earned
- Session duration

**4. View Global Dashboard:**
```
/info
```
Shows:
- Bot status & uptime
- All active users
- Total quests completed by everyone
- Their personal status

**5. Stop Completing:**
```
/stop
```

## 🔑 Getting User Token (For Members)

⚠️ **Tell your members:**

1. Open Discord in **web browser** (not app)
2. Press `F12` or `Ctrl+Shift+I` → Open DevTools
3. Go to **Application** tab
4. Left sidebar: **Local Storage** → select any discord.com URL
5. Look for `token` key
6. Copy the long value (without quotes)
7. When running `/link`, paste it

## 📊 How It Works

```
Your Server
├─ User1: Links token → Starts auto-complete → 50 quests/day
├─ User2: Links token → Starts auto-complete → 35 quests/day
├─ User3: Links token → Starts auto-complete → 42 quests/day
└─ Admin: Uses /info to see everyone's progress
```

## 🗄️ Database

- SQLite by default (`quest_bot.db`)
- Stores each user's token (encrypted)
- Tracks quest completion per user
- Logs all completed quests

## 🛡️ Security Notes

✅ Each user's token is encrypted before storage  
✅ Only stored in local database, never sent anywhere  
✅ Keep `.env` file secret  
✅ Never commit `.env` to GitHub  
✅ Users should not share their tokens  

## ❓ FAQs

**Q: Can multiple users use this bot?**
A: Yes! Everyone can link their token and complete their own quests.

**Q: Are tokens safe?**
A: Yes, they're encrypted in the database.

**Q: How often are quests completed?**
A: Every 5 minutes for each user.

**Q: Can I change the interval?**
A: Yes, edit line in `utils/quest_completer.py` → change `interval=300` to different value (in seconds)

**Q: What if bot crashes?**
A: Add restart script (see SETUP_LOCAL.md)

## 🚨 Troubleshooting

**Bot doesn't show up in server:**
- Check bot has permissions
- Reinvite with correct scopes

**Commands don't work:**
- Restart bot
- Check bot has "Use Slash Commands" permission

**Token errors:**
- Get fresh token from Discord DevTools
- Make sure it's copied completely

**Quests not completing:**
- Verify user token is correct
- Check logs in `bot.log`
- Run `/complete_now` to test

## 📈 Monitoring

Check `bot.log` for:
- User logins
- Quest completions
- Errors

```bash
tail -f bot.log  # macOS/Linux
type bot.log    # Windows
```

## 🔧 Keep Bot Running 24/7

See `SETUP_LOCAL.md` for scripts to auto-restart if it crashes.

---

**Ready to go!** Your server can now start using the bot! 🎉
