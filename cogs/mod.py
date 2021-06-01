import discord, asyncio

from discord.ext import commands

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='Purge', description='Purges a given amount of messages mentioned, also works with mentioning members at the end')
    @commands.guild_only()
    @commands.bot_has_guild_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, amount: int, member: discord.Member = None):
        if member == None:
            pass # will work on this
        else:
            pass

def setup(bot):
    bot.add_cog(Moderation(bot))