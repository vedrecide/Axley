import discord

from discord.ext import commands


class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        db = self.bot.db()
        self.collection = db["prefix"]
        self.emojis = self.bot.cool_emojis

    @commands.command(
        name="SetPrefix",
        aliases=[
            "ChangePrefix",
            "AddPrefix"
        ],
        description="Set's the custom prefix of the guild",
    )
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def prefix(self, ctx: commands.Context, pre: str):

        data = await self.collection.find_one({"_id": ctx.guild.id})

        if not data:
            await self.collection.insert_one(
                {"_id": ctx.guild.id, "prefix": [pre]}
            )
            embed = discord.Embed(
                color=discord.Color.magenta(),
                description="{} Successfully added the custom prefix of this server as `{}`".format(
                    self.emojis["tick"], pre
                ),
            )
            await ctx.message.reply(embed=embed)
        else:
            '''
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
            '''
            data['prefix'].append(pre)
            await self.collection.update_one({"_id": ctx.guild.id}, {"$set": {"prefix": data['prefix']}})

            embed = discord.Embed(
                color=discord.Color.magenta(),
                description="""
                {} Successfully added the custom prefix of this server to `{}`
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
    async def delprefix(self, ctx: commands.Context, index_num: int):

        data = await self.collection.find_one(
            {
                "_id": ctx.guild.id
            }
        )

        if not data:
            embed = discord.Embed(
                color=discord.Color.magenta(),
                description="{} **{}** doesn't have any custom prefix".format(
                    self.emojis["cross"], ctx.guild
                ),
            )
            await ctx.send(embed=embed)
        else:
            try:
                if len(data['prefix']) == 1:
                    await self.collection.delete_one(
                        {'_id': ctx.guild.id}
                    )

                    embed = discord.Embed(
                        color=discord.Color.magenta(),
                        description="""
                        {} **{}'s** custom prefixes have been deleted
                        """.format(
                            self.emojis["tick"],
                            ctx.guild
                        ),
                    )
                    await ctx.send(embed=embed)
                else:

                    data['prefix'].pop(index_num-1)
                    await self.collection.update_one(
                        {'_id': ctx.guild.id},
                        {'$set': {'prefix': data['prefix']}}
                    )
                    embed = discord.Embed(
                        color=discord.Color.magenta(),
                        description="""
                        {} Successfully deleted the prefix!
                        """.format(
                            self.emojis["tick"]
                        ),
                    )
                    await ctx.send(embed=embed)
            except IndexError:
                embed = discord.Embed(
                    color=discord.Color.magenta(),
                    description="{} That prefix index doesn't exist".format(self.em)
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
                timestamp=ctx.message.created_at
            )
            embed.set_footer(
                text="Requested by {}".format(ctx.author),
                icon_url='{}'.format(ctx.author.avatar_url)
            )

            await ctx.message.reply(embed=embed, mention_author=False)

        else:
            
            embed = discord.Embed(
                color=discord.Color.magenta(),
                description="{} **{}'s** prefixes".format(
                    self.emojis["tick"],
                    ctx.guild,
                    data["prefix"]
                ),
                timestamp=ctx.message.created_at
            )
            for i in range(len(data['prefix'])):
                prefixes = data['prefix'][i]
                embed.add_field(
                    name="Prefix #{}".format(i+1),
                    value='`{}`'.format(prefixes),
                    inline=False
                )
            embed.set_footer(
                text="Requested by {}".format(ctx.author),
                icon_url='{}'.format(ctx.author.avatar_url)
            )
            await ctx.message.reply(embed=embed, mention_author=False)


def setup(bot):
    bot.add_cog(Prefix(bot))
