import random

import discord
from discord import app_commands
from discord.ext import commands


class General(commands.Cog):
    """Podstawowe komendy."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # hybrid_command = działa jednocześnie jako /ping i !ping
    @commands.hybrid_command(description="Sprawdza opóźnienie bota")
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.send(f"🏓 Pong! {round(self.bot.latency * 1000)} ms")

    @commands.hybrid_command(description="Bot się przywita")
    async def hello(self, ctx: commands.Context) -> None:
        await ctx.send(f"Cześć, {ctx.author.mention}! 👋")

    @commands.hybrid_command(description="Rzut kostką")
    @app_commands.describe(sides="Liczba ścianek (domyślnie 6)")
    async def roll(self, ctx: commands.Context, sides: commands.Range[int, 2, 1000] = 6) -> None:
        await ctx.send(f"🎲 Wypadło: **{random.randint(1, sides)}** (k{sides})")

    @commands.hybrid_command(description="Informacje o użytkowniku")
    @app_commands.describe(member="Użytkownik (domyślnie ty)")
    @commands.guild_only()
    async def userinfo(self, ctx: commands.Context, member: discord.Member | None = None) -> None:
        member = member or ctx.author
        embed = discord.Embed(title=member.display_name, color=member.color)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Nazwa", value=str(member))
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Konto założone", value=discord.utils.format_dt(member.created_at, "D"))
        if member.joined_at:
            embed.add_field(name="Dołączył(a)", value=discord.utils.format_dt(member.joined_at, "R"))
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(General(bot))
