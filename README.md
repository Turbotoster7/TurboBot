# TurboBot

A Discord bot written in Python with [discord.py](https://discordpy.readthedocs.io/).

## 1. Create the bot on Discord

1. Go to https://discord.com/developers/applications → **New Application**.
2. **Bot** tab:
   - **Reset Token** → copy the token (never share it!).
   - Under **Privileged Gateway Intents**, enable **SERVER MEMBERS INTENT** and **MESSAGE CONTENT INTENT**.
3. **OAuth2 → URL Generator** tab:
   - Scopes: `bot` and `applications.commands`
   - Bot Permissions: e.g. `Send Messages`, `Embed Links`, `Manage Messages`, `Read Message History`
   - Open the generated link and add the bot to your server.

## 2. Run it (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env   # then paste your token into .env
python bot.py
```

> If `Activate.ps1` is blocked, run this once:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## Commands

Each one works as `/command` and as `!command`.

| Command | Description |
|---|---|
| `ping` | bot latency |
| `hello` | greeting |
| `roll [sides]` | roll a die |
| `userinfo [member]` | info about a member |
| `clear <amount>` | delete messages (requires the *Manage Messages* permission) |
| `help` | list of commands (`!help` only) |

## Structure

```
bot.py            # starts the bot, loads cogs, syncs slash commands
cogs/
  general.py      # basic commands
  moderation.py   # moderation commands
  events.py       # welcome message + error handling
```

To add new commands, create a new file in `cogs/` (use `general.py` as a template) — it will be loaded automatically.

**Tip:** put your server's ID in `GUILD_ID` in `.env` — new slash commands will show up right after restarting the bot.
