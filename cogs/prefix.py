import discord
import asyncio

from discord.ext import commands


class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        db = self.bot.db()
        self.collection = db["prefix"]
        self.emojis = self.bot.cool_emojis

    @commands.command(
        name="SetPrefix",
        aliases=["Changeprefix"],
        description="Set's the custom prefix of the guild",
    )
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def prefix(self, ctx: commands.Context, *, pre):

        data = await self.collection.find_one({"_id": ctx.guild.id})

        if not data:
            embed = discord.Embed(
                color=discord.Color.magenta(),
                description="""
                Are you sure you want to set the server prefix to `{}` ?\n
                If not, then you can leave this message as it is..
                """.format(
                    pre
                ),
            )
            message = await ctx.send(embed=embed)
            await message.add_reaction("✅")

            def check(reaction, user):
                return user == ctx.message.author and str(reaction.emoji) == "✅"

            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", timeout=60.0, check=check
                )
            except asyncio.TimeoutError:
                await ctx.message.add_reaction("❎")
                await message.remove_reaction("✅")
            else:
                await self.collection.insert_one(
                    {"_id": ctx.guild.id, "prefix": str(pre)}
                )
                embed = discord.Embed(
                    color=discord.Color.magenta(),
                    description="{} Successfully changed the custom prefix of this server to `{}`".format(
                        self.emojis["tick"], pre
                    ),
                )
                await ctx.message.reply(embed=embed)
        else:
            embed = discord.Embed(
                color=discord.Color.magenta(),
                description="Are you sure you want to update the server prefix to `{}` ?".format(
                    pre
                ),
            )
            message = await ctx.send(embed=embed)
            await message.add_reaction("✅")

            def check(reaction, user):
                return user == ctx.message.author and str(reaction.emoji) == "✅"

            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", timeout=60.0, check=check
                )
            except asyncio.TimeoutError:
                await ctx.message.add_reaction("❎")
            else:
                await self.collection.update_one(
                    {
                        "_id": ctx.guild.id
                    },
                    {
                        "$set": {
                            "prefix": str(pre)
                        }
                    }
                )

                embed = discord.Embed(
                    color=discord.Color.magenta(),
                    description="""
                    {} Successfully changed the custom prefix of this server to `{}`
                    """.format(
                        self.emojis["tick"],
                        pre
                    ),
                )
                await ctx.send(embed=embed)

    @prefix.error
    async def prefix_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                color=discord.Color.dark_orange(),
                description="""
                {} You are missing `Manage Messages` Permission(s) to run this command
                """.format(
                    self.emojis["cross"]
                ),
            )
            await ctx.send(embed=embed)

    @commands.command(
        name="DeletePrefix",
        aliases=[
            "Delprefix",
            "Dp",
            "Delpre"
        ],
        description="""
        Delete's the custom prefix of the bot,
        leaving it to the default prefix which is `+`
        """,
    )
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def delprefix(self, ctx: commands.Context):

        data = await self.collection.find_one(
            {
                "_id": ctx.guild.id
            }
        )

        if not data:
            embed = discord.Embed(
                color=discord.Color.magenta(),
                description="{} **{}** doesn't have any custom prefix".format(
                    self.cross["cross"], ctx.guild
                ),
            )
            await ctx.send(embed=embed)
        else:
            await self.collection.delete_one({"_id": ctx.guild.id})
            embed = discord.Embed(
                color=discord.Color.magenta(),
                description="""
                {} **{}'s** custom prefix has been deleted
                """.format(
                    self.cross["tick"],
                    ctx.guild
                ),
            )
            await ctx.send(embed=embed)

    @commands.command(
        name="ViewPrefix",
        description="View the guild's prefix"
    )
    @commands.guild_only()
    async def viewprefix(self, ctx):
        data = await self.collection.find_one(
            {
                "_id": ctx.guild.id
            }
        )

        if not data:
            embed = discord.Embed(
                color=discord.Color.magenta(),
                description="{} **{}'s** prefix is `+`".format(
                    self.emojis["tick"],
                    ctx.guild
                ),
            )
            await ctx.message.reply(embed=embed, mention_author=False)

        else:
            embed = discord.Embed(
                color=discord.Color.magenta(),
                description="{} **{}'s** prefix is `{}`".format(
                    self.emojis["tick"],
                    ctx.guild,
                    data["prefix"]
                ),
            )
            await ctx.message.reply(embed=embed, mention_author=False)


def setup(bot):
    bot.add_cog(Prefix(bot))
