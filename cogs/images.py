import discord

from discord.ext import commands
from PIL import Image
from io import BytesIO

class Images(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="Walker",
        aliases=[
            'Aw'
        ],
        description="Send's you being Alan Walker OwO"
    )
    @commands.guild_only()
    async def walker(self, ctx: commands.Context, user: discord.Member = None):
        if user == None:
            user = ctx.author

        walker = Image.open("./images/walker.jpeg")

        asset = user.avatar_url_as(size = 128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((195,195))

        walker.paste(pfp, (175, 60))

        walker.save("./images/profile.jpg")

        await ctx.send(file=discord.File("./images/profile.jpg"))

def setup(bot):
    bot.add_cog(Images(bot))