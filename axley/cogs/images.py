import discord

from discord.ext import commands
from PIL import Image
from io import BytesIO


class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="Walker", aliases=["Aw"], description="Send's you being Alan Walker OwO"
    )
    @commands.guild_only()
    async def walker(self, ctx: commands.Context, user: discord.Member = None):
        if user is None:
            user = ctx.author

        walker = Image.open("./axley/images/walker.jpeg")

        asset = user.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((195, 195))

        walker.paste(pfp, (175, 60))

        walker.save("./axley/images/profile.jpg")

        embed = discord.Embed(
            title="Looking good {}".format(user.display_name),
            color=0xD9E6D1
        )
        file = discord.File("./axley/images/profile.jpg", filename="image.png")
        embed.set_image(url="attachment://image.png")
        await ctx.send(embed=embed, file=file)


def setup(bot):
    bot.add_cog(Images(bot))
