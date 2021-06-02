import discord, asyncio

from discord.ext import commands

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='Purge', description='Purges a given amount of messages mentioned, also works with mentioning members at the end')
    @commands.guild_only()
    @commands.bot_has_guild_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int, member: discord.Member = None):
        if member == None:
            try:
                if amount <= -1:
                    await ctx.message.reply('The amount must not be negative..', mention_author=False)
                else:
                    await ctx.channel.purge(limit=amount+1)
                    embed = discord.Embed(
                        color=discord.Color.dark_red(),
                        description='{} Purged `{}` messages'.format(self.bot.emojis['tick'], amount)
                    )
                    await ctx.send(embed=embed)
            except ValueError:
                await ctx.message.reply('The amount must be an natural number', mention_author=False)
        else:
            try:
                if amount <= -1:
                    await ctx.message.reply('The amount must not be negative..', mention_author=False)
                else:
                    def check(m):
                        return m.author == member

                    await ctx.channel.purge(limit=amount, check=check)
                    embed = discord.Embed(
                        color=discord.Color.dark_red(),
                        description='{} Purged `{}` messages from **{}**'.format(self.bot.emojis['tick'], amount, member)
                    )
                    await ctx.send(embed=embed)
            except ValueError:
                await ctx.message.reply('The amount must be an natural number', mention_author=False)

def setup(bot):
    bot.add_cog(Moderation(bot))