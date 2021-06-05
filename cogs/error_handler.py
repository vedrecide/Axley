import discord

from discord.ext import commands
from discord.ext.commands import bot

class ErrorHandler(commands.Cog):
    '''
    Don't complain I have a error handler for almost every moderation command
    This one is for everything is common
    '''

    def __init__(self, bot):
        self.bot = bot
        self.emojis = self.bot.cool_emojis

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(
                color=discord.Color.dark_red(),
                description='{} Mentioned member is not in the guild'.format(self.emojis['cross'])
            )

            await ctx.send(embed=embed)

        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                color=discord.Color.dark_red(),
                description='{} **Owner only command >:(**'.format(self.emojis['cross'])
            )

            await ctx.send(embed=embed)
            
        else:
            pass


def setup(bot):
    bot.add_cog(ErrorHandler(bot))