import discord, asyncio

from discord.ext import commands
from .utils.converters import TimeConverter

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.emojis = self.bot.cool_emojis
        self.multiplier = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400, 'w': 604800}

    @commands.command(name='Purge', description='Purges a given amount of messages mentioned, also works with mentioning members at the end')
    @commands.guild_only()
    @commands.bot_has_guild_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context, amount: int, member: discord.Member = None):
        if member == None:
            try:
                if amount <= -1:
                    await ctx.message.reply('The amount must not be negative..', mention_author=False)
                elif amount > 100:
                    await ctx.message.reply('The amount must not exceed 100', mention_author=False)
                else:
                    await ctx.channel.purge(limit=amount+1)
                    embed = discord.Embed(
                        color=discord.Color.dark_red(),
                        description='{} Purged `{}` messages'.format(self.emojis['tick'], amount)
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

    @commands.command(name='Kick', description="Kick's the mentioned user out of the server")
    @commands.guild_only()
    @commands.bot_has_permissions(kick_members=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason = "No reason provided"):
        if ctx.author.top_role.position < member.top_role.position:
            embed = discord.Embed(
                color=discord.Color.dark_purple(),
                description="{} Can't kick **{}** due to role heirarchy".format(self.emojis['cross'], member)
            )
            return await ctx.send(embed=embed)

        embed = discord.Embed(
            color=discord.Color.dark_purple(),
            description="{} **{}** has been kicked `|` **Reason:** {}".format(self.emojis['tick'], member, reason)
        )
        await ctx.send(embed=embed)
        await member.kick(reason=reason)

    @commands.command(
        name='Ban',
        aliases=['Hackban'],
        description="Ban's the mentioned user out of the server"
    )
    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: discord.User, *, reason = "No reason provided"):
        if ctx.author.top_role.position < member.top_role.position:
            embed = discord.Embed(
                color=discord.Color.dark_purple(),
                description="{} Can't ban **{}** due to role heirarchy".format(self.emojis['cross'], member)
            )
            return await ctx.send(embed=embed)

        try:
            embed = discord.Embed(
                color=discord.Color.dark_purple(),
                description="{} **{}** has been banned `|` **Reason:** {}".format(self.emojis['tick'], member, reason)
            )
            await ctx.send(embed=embed)
            await member.ban(reason=reason)
        except Exception as exc:
            embed = discord.Embed(
                color=discord.Color.dark_purple(),
                description="{} Looks like **{}** isn't found (Not in the bot's reach sadly)".format(self.emojis['cross'], member)
            )
            await ctx.send(embed=embed)


    @commands.command(name='Unban', description="Unban's the mentioned user if in Guild ban lists")
    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx: commands.Context, member: int):
        # Not the best Unban command but meh..
        try:
            #try:
                await ctx.guild.unban(discord.Object(member))

                embed = discord.Embed(
                    color=discord.Color.blue(),
                    description="{} **{}** has been unbanned".format(self.emojis['tick'], member)
                )
                await ctx.send(embed=embed)
            #except Exception as exc:
                #embed = discord.Embed(
                    #color=discord.Color.blue(),
                    #description="{} **{}** isn't banned and isn't in the guild ban list\nOr there is an exception that has occured, Reported to the Support server!".format(self.emojis['cross'], member)
                #)

                #await ctx.send(embed=embed)

        except ValueError:
            embed = discord.Embed(
                color=discord.Color.blue(),
                description="{} Unban command includes only the `ID` of the User\n[Learn More Here!]".format(self.emojis['cross'])
            )

            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))