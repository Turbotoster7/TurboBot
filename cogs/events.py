import logging

import discord
from discord.ext import commands

log = logging.getLogger("turbobot")


class Events(commands.Cog):
    """Zdarzenia serwera i obsługa błędów komend."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f"Witaj na serwerze, {member.mention}! 🎉")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.MissingPermissions):
            msg = "Nie masz uprawnień do tej komendy."
        elif isinstance(error, commands.BotMissingPermissions):
            msg = "Bot nie ma wymaganych uprawnień na tym kanale."
        elif isinstance(error, commands.NoPrivateMessage):
            msg = "Tej komendy można używać tylko na serwerze."
        elif isinstance(error, (commands.MissingRequiredArgument, commands.BadArgument)):
            msg = f"Złe argumenty. Użycie: `{ctx.clean_prefix}{ctx.command} {ctx.command.signature}`"
        else:
            log.exception("Błąd w komendzie %s", ctx.command, exc_info=error)
            msg = "Coś poszło nie tak. 😕"
        await ctx.send(msg, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Events(bot))
