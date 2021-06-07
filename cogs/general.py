import discord

from discord.ext import commands

class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='Avatar',
        aliases=['Av'],
        description='Sends the avatar / profile picture of the member mentioned, if not mentioned, it will send your avatar'
    )
    @commands.guild_only()
    async def avatar(self, ctx: commands.Context, member: discord.Member = None):
        if member == None:
            member = ctx.author

        embed = discord.Embed(
            color=0xd9e6d1
        )
        embed.set_author(name='Avatar - {}'.format(member))
        embed.set_image(url='{}'.format(member.avatar_url))
        embed.add_field(name='URL', value='[Click]({})'.format(member.avatar_url))

        await ctx.send(embed=embed)
    

def setup(bot):
    bot.add_cog(General(bot))