from discord import app_commands
from discord.ext import commands


class Moderation(commands.Cog):
    """Commands for moderators."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(description="Delete recent messages in this channel")
    @app_commands.describe(amount="How many messages to delete (1-100)")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self, ctx: commands.Context, amount: commands.Range[int, 1, 100]) -> None:
        await ctx.defer(ephemeral=True)
        if ctx.interaction is None:
            await ctx.message.delete()  # for !clear, also delete the command message itself
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(f"🧹 Deleted {len(deleted)} messages.", ephemeral=True, delete_after=5)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Moderation(bot))
