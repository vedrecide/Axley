import discord

from discord.ext import commands
from discord.ext.commands import bot

class ErrorHandler(commands.Cog):

    def __init__(self):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(
                color=discord.Color.dark_red(),
                description='{} Mentioned member is not in the guild'.format(self.bot.emojis['tick'])
            )

            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))