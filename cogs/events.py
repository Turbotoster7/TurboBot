import logging

import discord
from discord.ext import commands

log = logging.getLogger("turbobot")


class Events(commands.Cog):
    """Server events and command error handling."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f"Welcome to the server, {member.mention}! 🎉")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.MissingPermissions):
            msg = "You don't have permission to use this command."
        elif isinstance(error, commands.BotMissingPermissions):
            msg = "The bot is missing the required permissions in this channel."
        elif isinstance(error, commands.NoPrivateMessage):
            msg = "This command can only be used in a server."
        elif isinstance(error, commands.CheckFailure):  # e.g. is_owner()
            msg = "You can't use this command."
        elif isinstance(error, commands.CommandOnCooldown):
            msg = f"Slow down! Try again in {error.retry_after:.0f} s."
        elif isinstance(error, (commands.MissingRequiredArgument, commands.BadArgument)):
            msg = f"Invalid arguments. Usage: `{ctx.clean_prefix}{ctx.command} {ctx.command.signature}`"
        else:
            log.exception("Error in command %s", ctx.command, exc_info=error)
            msg = "Something went wrong. 😕"
        await ctx.send(msg, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Events(bot))
