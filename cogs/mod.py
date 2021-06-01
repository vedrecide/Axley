import discord, asyncio

from discord.ext import commands

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='Purge', description='Deletes a given amount of messages sent in the chat or by a specific user')
    @commands.guild_only()
    @commands.bot_has_guild_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context, amount: int = 1, member: discord.Member = None):
        is_negative: bool = amount <= -1

        if not member:
            if is_negative:
                return await ctx.message.reply(
                    'The amount must not be negative..', 
                    mention_author=False
                )
            
            return await ctx.channel.purge(limit=amount+1)

        if is_negative:
            return await ctx.message.reply(
                'The amount must not be negative..', 
                mention_author=False
            )

        await ctx.channel.purge(
            limit=amount+1, 
            check=lambda m: m.author == member
        )

def setup(bot):
    bot.add_cog(Moderation(bot))