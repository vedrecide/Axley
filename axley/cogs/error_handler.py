import discord

from discord.ext import commands


class ErrorHandler(commands.Cog):
    """
    Don't complain I have a error handler for almost every moderation command
    This one is for everything is common
    """

    def __init__(self, bot):
        self.bot = bot
        self.emojis = self.bot.cool_emojis

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(
                color=discord.Color.dark_red(),
                description="{} Mentioned member is not in the guild".format(
                    self.emojis["cross"]
                ),
            )

            await ctx.send(embed=embed)

        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                color=discord.Color.dark_red(),
                description="{} **Owner only command >:(**".format(
                    self.emojis["cross"]
                ),
            )

            await ctx.send(embed=embed)

        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                color=discord.Color.dark_red(),
                title="{} **Invalid Arguments Provided!**".format(
                    self.emojis["cross"]
                ),
                description="Make sure you follow the pattern of arguments given below or the command won't just work"
            )
            embed.add_field(
                name="Command Format",
                value="```yaml\n{}{} {}```".format(
                    ctx.prefix, ctx.command, ctx.command.signature
                ),
            )
            await ctx.send(embed=embed)

        elif isinstance(error, commands.CommandOnCooldown):
            amount_left_in_seconds = (str(error.retry_after))
            final_time = amount_left_in_seconds.partition('.')
            embed = discord.Embed(
                title="{} Woah, Take a rest".format(self.emojis['cross']),
                description="Kindly wait for {} to use the command again".format(final_time)
            )

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                color=discord.Color.dark_red(),
                title="{} **Invalid Arguments Provided!**".format(
                    self.emojis["cross"]
                ),
                description="Make sure you follow the pattern of arguments given below or the command won't just work"
            )
            embed.add_field(
                name="Command Format",
                value="```yaml\n{}{} {}```".format(
                    ctx.prefix, ctx.command, ctx.command.signature
                ),
            )
            embed.set_footer(
                text="Requested by {}".format(ctx.author),
                icon_url="{}".format(ctx.author.avatar_url)
            )
            await ctx.send(embed=embed)

        else:
            raise error


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
