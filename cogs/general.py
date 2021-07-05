import discord
import json

from discord.ext import commands
from utils.paginator import clean_code


class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='Avatar',
        aliases=['Av'],
        description="""
        Sends the avatar / profile picture of the member mentioned, if not mentioned,
        it will send your avatar..
        """
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
        embed.add_field(name='Original URL',
                        value='[Click]({})'.format(member.avatar_url))

        await ctx.send(embed=embed)

    @commands.command(
        name='Userinfo',
        aliases=[
            'MemberInfo',
            'Whois'
        ],
        description="Send's the mentioned user information"
    )
    @commands.guild_only()
    async def userinfo(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author

        roles = [role for role in member.roles[1:]]

        if len(roles) == 0:
            role = "Member has no role in the server"
        elif len(roles) > 1024:
            role = f'Displaying Top 15 roles : {roles[:15]}'
        else:
            roles.reverse()
            role = ' , '.join([role.mention for role in roles])

        embed = discord.Embed(color=member.color,
                              timestamp=ctx.message.created_at)
        embed.set_author(
            name=f"User Info - {member}", icon_url="{}".format(member.avatar_url))
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        embed.add_field(name="Full name:", value=member, inline=False)
        embed.add_field(name="Guild name:",
                        value=member.display_name, inline=False)
        embed.add_field(name="ID:", value=member.id, inline=False)
        embed.add_field(name="Created at:", value=member.created_at.strftime(
            "%a, %d %B %Y, %I:%M %p UTC "), inline=False)
        embed.add_field(name="Joined at:", value=member.joined_at.strftime(
            "%a, %d %B %Y, %I:%M %p UTC "), inline=False)
        embed.add_field(name=f"Roles ({len(roles)})", value=" ".join(
            [role.mention for role in roles]), inline=False)
        embed.add_field(name="Top role:",
                        value=member.top_role.mention, inline=False)

        await ctx.message.reply(embed=embed, mention_author=False)

    @commands.command(
        name='EmbedBuilder',
        aliases=[
            'Embed'
        ],
        description='Embed Builder using JSON'
    )
    async def embed(self, ctx, *, data):
        try:
            try:
                data = clean_code(data)
                data = res = json.loads(data)

                if isinstance(data, dict):
                    embed = discord.Embed.from_dict(data)
                    await ctx.send(embed=embed)
            except Exception as exc:
                await ctx.send(exc)
        except:
            embed = discord.Embed(color=0x2f3136, description=data)
            await ctx.send(embed=embed)

    @commands.command(
        name='ServerInfo',
        aliases=[
            'Si',
            'GuildInfo',
            'Gi'
        ],
        description="Show's the respective guild's server info"
    )
    @commands.guild_only()
    async def serverinfo(self, ctx):
        embed = discord.Embed(color=0xd9e6d1, timestamp=ctx.message.created_at)

        embed.set_author(icon_url=f"{ctx.guild.icon_url}",
                         name=f"Guild Info - {ctx.guild.name}")
        embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
        embed.add_field(name="Owner", value=ctx.guild.owner)
        embed.add_field(name="Guild ID", value=str(ctx.guild.id))
        embed.add_field(name="Verification Level", value=str(
            ctx.guild.verification_level).title())
        embed.add_field(name="Total Count", value=ctx.guild.member_count)
        embed.add_field(
            name="Roles", value=f"`{len(ctx.guild.roles)}` roles in total")
        embed.add_field(name="Guild Region",
                        value=str(ctx.guild.region).title())
        embed.add_field(name="Created at", value=ctx.guild.created_at.__format__(
            '%A, %d. %B %Y %H:%M:%S'))
        embed.add_field(name="Channels", value="`{}` in total\n`{}` voice channels\n`{}` text channels".format(
            len(ctx.guild.channels),
            len(ctx.guild.voice_channels),
            len(ctx.guild.text_channels)
        )
        )
        embed.add_field(name="Categories", value="`{}` in total".format(
            len(ctx.guild.categories)))
        embed.add_field(name="Features", value="`" +
                        "` `".join(a for a in ctx.guild.features) + '` ', inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
