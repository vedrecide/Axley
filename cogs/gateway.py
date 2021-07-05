from discord.ext import commands


class Gateway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        db = self.bot.db()
        self.collection = db["gateway"]


def setup(bot):
    bot.add_cog(Gateway(bot))
