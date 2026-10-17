import random

import discord
from discord import app_commands
from discord.ext import commands


class General(commands.Cog):
    """Basic commands."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # hybrid_command = works as both /ping and !ping
    @commands.hybrid_command(description="Check the bot's latency")
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.send(f"🏓 Pong! {round(self.bot.latency * 1000)} ms")

    @commands.hybrid_command(description="Say hello to the bot")
    async def hello(self, ctx: commands.Context) -> None:
        await ctx.send(f"Hi, {ctx.author.mention}! 👋")

    @commands.hybrid_command(description="Roll a die")
    @app_commands.describe(sides="Number of sides (default 6)")
    async def roll(self, ctx: commands.Context, sides: commands.Range[int, 2, 1000] = 6) -> None:
        await ctx.send(f"🎲 You rolled **{random.randint(1, sides)}** (d{sides})")

    @commands.hybrid_command(description="Show information about a member")
    @app_commands.describe(member="Member to look up (defaults to you)")
    @commands.guild_only()
    async def userinfo(self, ctx: commands.Context, member: discord.Member | None = None) -> None:
        member = member or ctx.author
        embed = discord.Embed(title=member.display_name, color=member.color)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Username", value=str(member))
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Account created", value=discord.utils.format_dt(member.created_at, "D"))
        if member.joined_at:
            embed.add_field(name="Joined", value=discord.utils.format_dt(member.joined_at, "R"))
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(General(bot))
