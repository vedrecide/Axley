import discord, random, asyncio, http

from discord.ext import commands
from aiohttp import ClientSession

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.emojis = self.bot.cool_emojis
        self.session = ClientSession()

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
        await ctx.trigger_typing()
        await asyncio.sleep(1)
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
            await ctx.message.reply('{} **{}** has paid their respect'.format(random.choice(emojis), ctx.author), mention_author = False)
        else:
            await ctx.message.reply('{} **{}** has paid their respect for **{}**'.format(random.choice(emojis), ctx.author, text), mention_author = False)

    @commands.command(
        name="Meme",
        aliases = ["meemee", "memes"],
        description="Send's a random meme from reddit :3"
    )
    @commands.guild_only()
    async def meme(self, ctx: commands.Context):
        embed = discord.Embed(color=discord.Color.dark_blue())
        embed.set_footer(text='Requested by {}'.format(ctx.author), icon_url='{}'.format(ctx.author.avatar_url))

        async with self.session.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)

    @commands.command(
        name="Eighball",
        aliases=[
            '8ball',
            'Eb',
            '8b'
        ],
        description="Send's an 8ball answer to your random question"
    )
    @commands.guild_only()
    async def eightball(self, ctx: commands.Context, *, question: str):
        res = [
            "It is Certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."
        ]

        answer = random.choice(res)

        embed = discord.Embed(
            color=discord.Color.dark_purple(),
            description="**Question:** {}\n**Answer:** {}".format(question, answer),
            timestamp=ctx.message.created_at
        )
        embed.set_author(
            name="8ball - {}".format(ctx.author),
            icon_url='{}'.format(ctx.author.avatar_url)
        )

        await ctx.message.reply(embed=embed, mention_author=False)


def setup(bot):
    bot.add_cog(Fun(bot))