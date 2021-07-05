import discord
import asyncio
import datetime

from discord.ext import commands
from utils.converters import TimeConverter, MemberID


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emojis = self.bot.cool_emojis
        self.multiplier = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
        db = self.bot.db()
        self.warn_collection = db["warnings"]
        self.muterole_collection = db["muteroles"]

    @commands.command(
        name="Purge",
        description="Purges a given amount of messages mentioned, also works with mentioning members at the end",
    )
    @commands.guild_only()
    @commands.bot_has_guild_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    async def purge(
        self, ctx: commands.Context, amount: int, member: discord.Member = None
    ):
        if member is None:
            try:
                if amount <= -1:
                    embed = discord.Embed(
                        color=discord.Color.dark_orange(),
                        description="{} The amount must not be negative".format(
                            self.emojis["cross"]
                        ),
                    )
                    await ctx.message.reply(embed=embed, mention_author=False)
                elif amount >= 100:
                    embed = discord.Embed(
                        color=discord.Color.dark_orange(),
                        description="{} The amount must not exceed 100 or equal to it".format(
                            self.emojis["cross"]
                        ),
                    )
                    await ctx.message.reply(embed=embed, mention_author=False)
                else:
                    await ctx.channel.purge(limit=amount + 1)
                    embed = discord.Embed(
                        color=discord.Color.dark_red(),
                        description="{} Purged `{}` messages".format(
                            self.emojis["tick"], amount
                        ),
                    )
                    await ctx.send(embed=embed)
            except ValueError:
                embed = discord.Embed(
                    color=discord.Color.dark_orange(),
                    description="{} The amount must be an natural number".format(
                        self.emojis["cross"]
                    ),
                )
                await ctx.message.reply(embed=embed, mention_author=False)
        else:
            try:
                if amount <= -1:
                    embed = discord.Embed(
                        color=discord.Color.dark_orange(),
                        description="{} The amount must not be negative".format(
                            self.emojis["cross"]
                        ),
                    )
                    await ctx.message.reply(embed=embed, mention_author=False)
                else:

                    def check(m):
                        return m.author == member

                    await ctx.channel.purge(limit=amount, check=check)
                    embed = discord.Embed(
                        color=discord.Color.dark_red(),
                        description="{} Purged `{}` messages from **{}**".format(
                            self.bot.emojis["tick"], amount, member
                        ),
                    )
                    await ctx.send(embed=embed)
            except ValueError:
                embed = discord.Embed(
                    color=discord.Color.dark_orange(),
                    description="{} The amount must be an natural number".format(
                        self.emojis["cross"]
                    ),
                )
                await ctx.message.reply(embed=embed, mention_author=False)

    @purge.error
    async def purge_error(self, ctx, error):
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
        name="Kick", description="Kick's the mentioned user out of the server"
    )
    @commands.guild_only()
    @commands.bot_has_permissions(kick_members=True)
    @commands.has_permissions(kick_members=True)
    async def kick(
        self,
        ctx: commands.Context,
        member: discord.Member,
        *,
        reason="No reason provided",
    ):
        if ctx.author.top_role.position < member.top_role.position:
            embed = discord.Embed(
                color=discord.Color.dark_purple(),
                description="{} Can't kick **{}** due to role heirarchy".format(
                    self.emojis["cross"], member
                ),
            )
            return await ctx.send(embed=embed)

        embed = discord.Embed(
            color=discord.Color.dark_purple(),
            description="{} **{}** has been kicked `|` **Reason:** {}".format(
                self.emojis["tick"], member, reason
            ),
        )
        await ctx.send(embed=embed)
        await member.kick(reason=reason)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                color=discord.Color.dark_orange(),
                description="""
                {} You are missing `Kick Members` Permission(s) to run this command
                """.format(
                    self.emojis["cross"]
                ),
            )
            await ctx.send(embed=embed)

    @commands.command(
        name="Softban", description="Softban's the mentioned user out of the server"
    )
    @commands.guild_only()
    @commands.bot_has_permissions(kick_members=True)
    @commands.has_permissions(kick_members=True)
    async def softban(
        self,
        ctx: commands.Context,
        member: discord.Member,
        *,
        reason="No reason provided",
    ):
        if ctx.author.top_role.position < member.top_role.position:
            embed = discord.Embed(
                color=discord.Color.dark_purple(),
                description="{} Can't kick **{}** due to role heirarchy".format(
                    self.emojis["cross"], member
                ),
            )
            return await ctx.send(embed=embed)

        embed = discord.Embed(
            color=discord.Color.dark_purple(),
            description="{} **{}** has been softbanned `|` **Reason:** {}".format(
                self.emojis["tick"], member, reason
            ),
        )
        await ctx.send(embed=embed)
        await ctx.guild.ban(member)
        await asyncio.sleep(1)
        await ctx.guild.unban(member)

    @softban.error
    async def softban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                color=discord.Color.dark_orange(),
                description="{} You are missing `Ban Members` Permission(s) to run this command".format(
                    self.emojis["cross"]
                ),
            )
            await ctx.send(embed=embed)

    @commands.command(
        name="Ban",
        aliases=["Hackban"],
        description="Ban's the mentioned user out of the server",
    )
    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def ban(
        self,
        ctx: commands.Context,
        member: discord.User,
        *,
        reason="No reason provided",
    ):
        if ctx.author.top_role.position < member.top_role.position:
            embed = discord.Embed(
                color=discord.Color.dark_purple(),
                description="{} Can't ban **{}** due to role heirarchy".format(
                    self.emojis["cross"], member
                ),
            )
            return await ctx.send(embed=embed)

        try:
            embed = discord.Embed(
                color=discord.Color.dark_purple(),
                description="{} **{}** has been banned `|` **Reason:** {}".format(
                    self.emojis["tick"], member, reason
                ),
            )
            await ctx.send(embed=embed)
            await member.ban(reason=reason)
        except Exception as exc:
            embed = discord.Embed(
                color=discord.Color.dark_purple(),
                description="{} Looks like **{}** isn't found (Not in the bot's reach sadly)".format(
                    self.emojis["cross"],
                    member
                ),
            )
            await ctx.send(embed=embed)
            raise exc

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                color=discord.Color.dark_orange(),
                description="{} You are missing `Ban Members` Permission(s) to run this command".format(
                    self.emojis["cross"]
                ),
            )
            await ctx.send(embed=embed)

    @commands.command(
        name="Unban", description="Unban's the mentioned user if in Guild ban lists"
    )
    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx: commands.Context, member: MemberID):
        await ctx.guild.unban(discord.Object(member))

        embed = discord.Embed(
            color=discord.Color.blue(),
            description="{} **{}** has been unbanned".format(
                self.emojis["tick"], member
            ),
        )
        await ctx.send(embed=embed)

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                color=discord.Color.dark_orange(),
                description="{} You are missing `Ban Members` Permission(s) to run this command".format(
                    self.emojis["cross"]
                ),
            )
            await ctx.send(embed=embed)

    @commands.command(
        name="Tempban", description="Temporary ban somebody if the duration is correct"
    )
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def tempban(
        self,
        ctx: commands.Context,
        member: discord.User,
        duration: TimeConverter,
        *,
        reason="No reason provided",
    ):
        if ctx.author.top_role.position < member.top_role.position:
            embed = discord.Embed(
                color=discord.Color.dark_purple(),
                description="{} Can't tempban **{}** due to role heirarchy".format(
                    self.emojis["cross"], member
                ),
            )
            return await ctx.send(embed=embed)

        amount, unit = duration
        await ctx.guild.ban(member)
        embed = discord.Embed(
            color=discord.Color.purple(),
            description="{} **{}** has been tempbanned for `{}` `|` **Reason:** {}".format(
                self.emojis["tick"], member, duration, reason
            ),
        )
        await ctx.send(embed=embed)
        await asyncio.sleep(amount * self.multiplier[unit])
        await ctx.guild.unban(member)

    @tempban.error
    async def tempban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                color=discord.Color.dark_orange(),
                description="{} You are missing `Ban Members` Permission(s) to run this command".format(
                    self.emojis["cross"]
                ),
            )
            await ctx.send(embed=embed)

    @commands.command(
        name="Warn", aliases=["Punish", "W"], description="Adds a warning to the member"
    )
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def warn(
        self,
        ctx: commands.Context,
        member: discord.Member,
        *,
        reason="No reason provided",
    ):
        if ctx.author.top_role.position < member.top_role.position:
            embed = discord.Embed(
                color=discord.Color.dark_purple(),
                description="{} Can't warn **{}** due to role heirarchy".format(
                    self.emojis["cross"], member
                ),
            )
            return await ctx.send(embed=embed)

        if member == ctx.author:
            embed = discord.Embed(
                color=discord.Color.dark_purple(),
                description="{} You can't warn yourself".format(
                    self.emojis["cross"], member
                ),
            )
            return await ctx.send(embed=embed)

        user_id = {"user": member.id, "guild": ctx.guild.id}

        warns = await self.warn_collection.find_one(user_id)

        if not warns:
            await self.warn_collection.insert_one(
                {"user": member.id, "guild": ctx.guild.id, "warnings": []}
            )
            warns = await self.warn_collection.find_one(user_id)
            warns["warnings"].append(
                {
                    "warned_at": datetime.datetime.utcnow().strftime(
                        "%d/%m/%Y - %I:%M %p"
                    ),
                    "responsible_moderator": f"{ctx.author}",
                    "moderator_id": f"{ctx.author.id}",
                    "reason": str(reason),
                }
            )

            await self.warn_collection.update_one(
                {"user": member.id, "guild": ctx.guild.id},
                {"$set": {"warnings": warns["warnings"]}},
            )

            embed = discord.Embed(
                color=discord.Color.light_grey(),
                description="{} **{}** has been warned `|` **Reason:** {}".format(
                    self.emojis["tick"], member, reason
                ),
            )
            await ctx.send(embed=embed)

        else:

            warns["warnings"].append(
                {
                    "warned_at": datetime.datetime.utcnow().strftime(
                        "%d/%m/%Y - %I:%M %p"
                    ),
                    "responsible_moderator": f"{ctx.author}",
                    "moderator_id": f"{ctx.author.id}",
                    "reason": str(reason),
                }
            )

            await self.warn_collection.update_one(
                {"user": member.id, "guild": ctx.guild.id},
                {"$set": {"warnings": warns["warnings"]}},
            )

            embed = discord.Embed(
                color=discord.Color.light_grey(),
                description="{} **{}** has been warned `|` **Reason:** {}".format(
                    self.emojis["tick"], member, reason
                ),
            )
            await ctx.send(embed=embed)

    @warn.error
    async def warn_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                color=discord.Color.dark_orange(),
                description="{} You are missing `Manage Messages` Permission(s) to run this command".format(
                    self.emojis["cross"]
                ),
            )
            await ctx.send(embed=embed)

    @commands.command(
        name="Warnings",
        aliases=["Warns"],
        description="View the warnings of other members using this command",
    )
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def warnings(self, ctx: commands.Context, member: discord.Member):

        warns = await self.warn_collection.find_one(
            {"user": member.id, "guild": ctx.guild.id}
        )

        if not warns:
            embed = discord.Embed(
                color=discord.Color.light_grey(),
                description="{} **{}** doesn't have any warnings".format(
                    self.emojis["cross"], member
                ),
            )

            await ctx.send(embed=embed)

        else:
            number_of_warns = len(warns["warnings"])
            embed = discord.Embed(
                color=discord.Color.light_grey(), timestamp=ctx.message.created_at
            )
            embed.set_author(
                name="{}".format(member), icon_url="{}".format(member.avatar_url)
            )
            embed.set_footer(
                text="Requested by {}".format(ctx.author),
                icon_url="{}".format(ctx.author.avatar_url),
            )
            for i in range(number_of_warns):
                reason = warns["warnings"][i]["reason"]
                mod = warns["warnings"][i]["responsible_moderator"]
                time = warns["warnings"][i]["warned_at"]
                mod_id = warns["warnings"][i]["moderator_id"]

                embed.add_field(
                    name="#{} | {}".format(i + 1, time),
                    value="🔖 **Reason:** {}\n🧑‍🦱 **Mod:** {}\n🔩 **Mod ID:** {}".format(
                        reason, mod, mod_id
                    ),
                )

            await ctx.send(
                "📖 **{}** has `{}` warnings in total".format(member, number_of_warns),
                embed=embed,
            )

    @warnings.error
    async def warnings_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                color=discord.Color.dark_orange(),
                description="{} You are missing `Manage Messages` Permission(s) to run this command".format(
                    self.emojis["cross"]
                ),
            )
            await ctx.send(embed=embed)

    @commands.command(
        name="ClearWarn",
        aliases=["DeleteWarn", "Delwarn", "Dw"],
        description="Clear's the warning of the member mentioned if the Warn ID is correct",
    )
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def delwarn(self, ctx: commands.Context, member: discord.Member, num: str):
        if ctx.author.top_role.position < member.top_role.position:
            embed = discord.Embed(
                color=discord.Color.dark_purple(),
                description="""
                {} Can't delete the warning of **{}** due to role heirarchy
                """.format(
                    self.emojis["cross"], member
                ),
            )
            return await ctx.send(embed=embed)

        if member == ctx.author:
            embed = discord.Embed(
                color=discord.Color.dark_purple(),
                description="{} You can't delete your warning".format(
                    self.emojis["cross"], member
                ),
            )
            return await ctx.send(embed=embed)

        try:
            warn = int(num)
        except ValueError:
            embed = discord.Embed(
                color=discord.Color.light_grey(),
                description="""
                {} Number must be a natural number and not any other value
                """.format(
                    self.emojis["cross"]
                ),
            )
            return await ctx.send(embed=embed)

        warns = await self.warn_collection.find_one(
            {"user": member.id, "guild": ctx.guild.id}
        )

        if not warns:
            embed = discord.Embed(
                color=discord.Color.light_grey(),
                description="{} **{}** doesn't have any warnings".format(
                    self.emojis["cross"]
                ),
            )
            return await ctx.send(f"**{member}** doesn't have any warnings..")

        try:
            warns["warnings"].pop(warn - 1)
        except IndexError:
            embed = discord.Embed(
                color=discord.Color.light_grey(),
                description="{} **Invalid Warn ID provided**".format(
                    self.emojis["cross"]
                ),
            )
            return await ctx.send(embed=embed)

        if len(warns["warnings"]) == 0:
            await self.warn_collection.delete_one(
                {"user": member.id, "guild": ctx.guild.id}
            )
        else:
            await self.warn_collection.update_one(
                {"user": member.id, "guild": ctx.guild.id},
                {"$set": {"warnings": warns["warnings"]}},
            )

        embed = discord.Embed(
            color=discord.Color.light_grey(),
            description="{} Successfully deleted Warning **#{}** of **{}**".format(
                self.emojis["tick"], num, member
            ),
        )

        await ctx.message.reply(embed=embed, mention_author=False)

    @delwarn.error
    async def delwarn_error(self, ctx, error):
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

    @commands.group(
        name="Muterole",
        aliases=["Mr", "Mrole", "Muter"],
        description="Muterole grouped command consisting of other sub commands <3",
    )
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def muterole(self, ctx: commands.Context):
        if ctx.invoke.command is None:
            pass

    @muterole.command(
        name="Set", aliases=["Add"], description="Set's the muterole of the guild"
    )
    @commands.guild_only()
    async def set(self, ctx: commands.Context, role: discord.Role):
        data = await self.muterole_collection.find_one({"_id": ctx.guild.id})

        if not data:
            await self.muterole_collection.insert_one(
                {"_id": ctx.guild.id, "muterole": role.id}
            )

        else:
            await self.muterole_collection.update_one(
                {"_id": ctx.guild.id}, {"$set": {"muterole": role.id}}
            )


def setup(bot):
    bot.add_cog(Moderation(bot))
