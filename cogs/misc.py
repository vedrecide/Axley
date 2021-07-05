import discord
import psutil
import os

from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process(os.getpid())

    @commands.command(name="Ping", description="Ping of the bot")
    @commands.guild_only()
    async def ping(self, ctx: commands.Context):
        await ctx.message.reply(
            "**Pong!** `{}ms`".format(round(self.bot.latency * 1000)),
            mention_author=False,
        )

    @commands.command(name="Source", description="Source code of Axley <3")
    @commands.guild_only()
    async def source(self, ctx: commands.Context):
        embed = discord.Embed(
            color=0xD9E6D1, description=f"[Click]({self.bot.github_repo})"
        )

        await ctx.message.reply(embed=embed, mention_author=False)

    @commands.command(
        name="Stats",
        aliases=["Botstats", "Botinfo"],
        description="You can check bot statistics using this command",
    )
    @commands.guild_only()
    async def stats(self, ctx: commands.Context):
        ram_usage = self.process.memory_full_info().rss / 1024 ** 2

        embed = discord.Embed(
            color=0xD9E6D1,
            description="> **RAM:** {:.2f} MB\n> **Commands:** {}\n".format(
                ram_usage, len([a.name for a in self.bot.commands])
            ),
        )

        await ctx.message.reply(embed=embed, mention_author=False)


def setup(bot):
    bot.add_cog(Misc(bot))
