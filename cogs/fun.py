import discord, random

from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.emojis = self.bot.cool_emojis

    @commands.command(
        name='Reverse',
        aliases=['Rev'],
        description="Reverse's a word given by you if the argument is correct"
    )
    @commands.guild_only()
    async def reverse(self, ctx: commands.Context, *, text: str):
        a = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        embed = discord.Embed(
            color=discord.Color.dark_blue(),
            description="🔁  {}".format(a)
        )
        await ctx.message.reply(embed=embed, mention_author=False)

    @commands.command(
        name='F',
        aliases=['Respect', 'Res'],
        description="Pay Respect by just prompting this command, simple"
    )
    @commands.guild_only()
    async def f(self, ctx: commands.Context, *, text: str = None):
        emojis = [
            '💛',
            '💚',
            '💙',
            '💜'
        ]

        if not text:
            await ctx.message.reply('{} **{}** has paid their respect'.format(random.choice(emojis), ctx.author))
        else:
            await ctx.message.reply('{} **{}** has paid their respect for **{}**'.format(random.choice(emojis), ctx.author, text))


def setup(bot):
    bot.add_cog(Fun(bot))