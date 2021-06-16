import discord

from discord.ext import commands

class Misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.message.reply('**Pong!** `{}ms`'.format(round(self.bot.latency * 1000)), mention_author=False)

def setup(bot):
    bot.add_cog(Misc(bot))