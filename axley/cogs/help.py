import discord
import typing
import datetime

from discord.ext import commands
from axley.utils.buttons import ButtonPaginator
from discord.ext.commands import DefaultHelpCommand

class AxleyHelpCommand(DefaultHelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(
        self, mapping: typing.Dict[commands.Cog, typing.List[commands.Command]]
    ):
            ctx: commands.Context = self.context
            self.help = ButtonPaginator(ctx.bot)
            z = discord.Embed(
                color=0xD9E6D1,
                description=f"""
                For more info regarding a category, Send `{ctx.prefix}help [category]`
                """,
                timestamp=ctx.message.created_at
            )
            z.set_author(
                name='Help - Axley',
                icon_url='{}'.format(ctx.bot.user.avatar_url)
            )
            z.add_field(
                name=':straight_ruler: Moderation',
                value='`{}help Moderation`'.format(ctx.prefix)
            )
            z.add_field(
                name=':cloud: General',
                value='`{}help General`'.format(ctx.prefix)
            )
            z.add_field(
                name=':grey_exclamation: Prefix',
                value='`{}help Prefix`'.format(ctx.prefix)
            )
            z.add_field(
                name='Misc',
                value='{}help Misc'.format(ctx.prefix)
            )
            z.add_field(
                name='Images',
                value='{}help Images'.format(ctx.prefix)
            )
            z.add_field(
                name='\0',
                value="[**Invite**](https://discord.com/api/oauth2/authorize?client_id=768380239255568414&permissions=8&scope=bot) **|** [**Community**](https://discord.gg/XJcThGs4Pu) **|** [**Github**](https://github.com/1olipop/Axley)",
                inline=False
            )
            z.set_footer(
                text="Requested by {}".format(ctx.author),
                icon_url=f"{ctx.author.avatar_url}"
            )

            a = discord.Embed(
                color=0xD9E6D1,
                title="Moderation",
                description=' '.join(
                    map(
                        lambda command: '`' + command.name + '`',
                        ctx.bot.get_cog('Moderation').get_commands()
                    )
                ), 
                timestamp=ctx.message.created_at
            )
            a.set_author(
                name='Help - Axley',
                icon_url='{}'.format(ctx.bot.user.avatar_url)
            )
            a.add_field(
                name='\0',
                value="[**Invite**](https://discord.com/api/oauth2/authorize?client_id=768380239255568414&permissions=8&scope=bot) **|** [**Community**](https://discord.gg/XJcThGs4Pu) **|** [**Github**](https://github.com/1olipop/Axley)"
            )
            a.set_footer(
                text="Requested by {}".format(ctx.author),
                icon_url=f"{ctx.author.avatar_url}"
            )
            b = discord.Embed(
                title="General",
                color=0xD9E6D1,
                description=' '.join(
                    map(
                        lambda command: '`' + command.name + '`',
                        ctx.bot.get_cog('General').get_commands()
                    )
                ),
                timestamp=ctx.message.created_at
            )
            b.set_author(
                name='Help - Axley',
                icon_url='{}'.format(ctx.bot.user.avatar_url)
            )
            b.add_field(
                name='\0',
                value="[**Invite**](https://discord.com/api/oauth2/authorize?client_id=768380239255568414&permissions=8&scope=bot) **|** [**Community**](https://discord.gg/XJcThGs4Pu) **|** [**Github**](https://github.com/1olipop/Axley)"
            )
            b.set_footer(text="Requested by {}".format(ctx.author), icon_url=f"{ctx.author.avatar_url}")
            c = discord.Embed(
                title="Fun",
                color=0xD9E6D1,
                description=' '.join(
                    map(
                        lambda command: '`' + command.name + '`',
                        ctx.bot.get_cog('Fun').get_commands()
                    )
                ),
                timestamp=ctx.message.created_at
            )
            c.set_author(
                name='Help - Axley',
                icon_url='{}'.format(ctx.bot.user.avatar_url)
            )
            c.add_field(
                name='\0',
                value="[**Invite**](https://discord.com/api/oauth2/authorize?client_id=768380239255568414&permissions=8&scope=bot) **|** [**Community**](https://discord.gg/XJcThGs4Pu) **|** [**Github**](https://github.com/1olipop/Axley)"
            )
            c.set_footer(text="Requested by {}".format(ctx.author), icon_url=f"{ctx.author.avatar_url}")

            await self.help.run(ctx, [z, a, b, c], 60, True, True)

    async def send_cog_help(self, cog):
        ctx: commands.Context = self.context
        
        embed = discord.Embed(
            color=0xD9E6D1, title="Help", timestamp=datetime.datetime.utcnow()
        )

        embed.set_author(
            name="Help",
            icon_url="""
            https://cdn.discordapp.com/avatars/768380239255568414/343bbefbd8d9b7166c9b1a0f6b7ccf80.png?size=1024
            """,
        )

        embed.add_field(
            name=cog.qualified_name + " " + f"""
            ({len([command for command in cog.get_commands()])} commands in total)
            """,
            value="`" + "` `".join(a.name for a in cog.get_commands()) + "`",
        )
        embed.set_footer(text="Requested by {}".format(ctx.author), icon_url="{}".format(ctx.author.avatar_url))

        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(color=0xD9E6D1)
        embed.set_author(name="{}{}".format(self.clean_prefix, command.name))
        embed.add_field(
            name="Usage",
            value="```yaml\n" + self.get_command_signature(command) + "```",
        )
        embed.add_field(name="Description", value=command.description, inline=False)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)


class Help(commands.Cog):
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = AxleyHelpCommand()
        bot.help_command.cog = self

def setup(bot):
    bot.add_cog(Help(bot))
