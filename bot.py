import logging
import os
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("PREFIX", "!")
# Optional: ID of a test server - slash commands show up there instantly,
# while global ones can take a while before Discord displays them.
GUILD_ID = os.getenv("GUILD_ID")

COGS_DIR = Path(__file__).parent / "cogs"

log = logging.getLogger("turbobot")


class TurboBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        # These two must be enabled in Developer Portal -> Bot -> Privileged Gateway Intents
        intents.message_content = True  # prefix commands (e.g. !ping)
        intents.members = True  # events like a member joining

        super().__init__(command_prefix=commands.when_mentioned_or(PREFIX), intents=intents)

    async def setup_hook(self) -> None:
        # Load every .py file in cogs/ as a separate command module
        for file in sorted(COGS_DIR.glob("*.py")):
            if file.stem.startswith("_"):
                continue
            await self.load_extension(f"cogs.{file.stem}")
            log.info("Loaded cog: %s", file.stem)

        if GUILD_ID:
            guild = discord.Object(id=int(GUILD_ID))
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
        else:
            synced = await self.tree.sync()
        log.info("Synced %d slash commands", len(synced))

    async def on_ready(self) -> None:
        log.info("Logged in as %s (ID: %s)", self.user, self.user.id)
        await self.change_presence(activity=discord.Game(name=f"{PREFIX}help | /ping"))


def main() -> None:
    if not TOKEN:
        raise SystemExit("DISCORD_TOKEN is missing - copy .env.example to .env and paste your bot token.")

    discord.utils.setup_logging(level=logging.INFO)
    bot = TurboBot()
    try:
        bot.run(TOKEN, log_handler=None)
    except discord.PrivilegedIntentsRequired:
        raise SystemExit(
            "Enable 'MESSAGE CONTENT INTENT' and 'SERVER MEMBERS INTENT' in the Developer Portal "
            "(Bot tab -> Privileged Gateway Intents)."
        )
    except discord.LoginFailure:
        raise SystemExit("Invalid token - check DISCORD_TOKEN in your .env file.")


if __name__ == "__main__":
    main()
