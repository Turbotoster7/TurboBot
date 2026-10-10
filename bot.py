import logging
import os
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("PREFIX", "!")
# Opcjonalne: ID serwera testowego - komendy slash pojawiają się tam od razu,
# a globalne mogą potrzebować chwili, zanim Discord je pokaże.
GUILD_ID = os.getenv("GUILD_ID")

COGS_DIR = Path(__file__).parent / "cogs"

log = logging.getLogger("turbobot")


class TurboBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        # Te dwa intenty trzeba włączyć w Developer Portal -> Bot -> Privileged Gateway Intents
        intents.message_content = True  # komendy z prefiksem (np. !ping)
        intents.members = True  # zdarzenia typu dołączenie użytkownika

        super().__init__(command_prefix=commands.when_mentioned_or(PREFIX), intents=intents)

    async def setup_hook(self) -> None:
        # Ładuje każdy plik .py z folderu cogs/ jako osobny moduł z komendami
        for file in sorted(COGS_DIR.glob("*.py")):
            if file.stem.startswith("_"):
                continue
            await self.load_extension(f"cogs.{file.stem}")
            log.info("Załadowano cog: %s", file.stem)

        if GUILD_ID:
            guild = discord.Object(id=int(GUILD_ID))
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
        else:
            synced = await self.tree.sync()
        log.info("Zsynchronizowano %d komend slash", len(synced))

    async def on_ready(self) -> None:
        log.info("Zalogowano jako %s (ID: %s)", self.user, self.user.id)
        await self.change_presence(activity=discord.Game(name=f"{PREFIX}help | /ping"))


def main() -> None:
    if not TOKEN:
        raise SystemExit("Brak DISCORD_TOKEN - skopiuj .env.example do .env i wklej token bota.")

    discord.utils.setup_logging(level=logging.INFO)
    bot = TurboBot()
    try:
        bot.run(TOKEN, log_handler=None)
    except discord.PrivilegedIntentsRequired:
        raise SystemExit(
            "Włącz 'MESSAGE CONTENT INTENT' i 'SERVER MEMBERS INTENT' w Developer Portal "
            "(zakładka Bot -> Privileged Gateway Intents)."
        )
    except discord.LoginFailure:
        raise SystemExit("Nieprawidłowy token - sprawdź DISCORD_TOKEN w pliku .env.")


if __name__ == "__main__":
    main()
