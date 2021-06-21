import discord, datetime

from discord.ext import commands
from discord.ext.commands.core import command

class AxleyHelpCommand(commands.HelpCommand):

    def __init__(self):
        super().__init__(
            command_attrs={
                'verify_checks': False
            }
        )

    def get_something(self, command):
        return command.qualified_name

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help", color=0xd9e6d1, timestamp=datetime.datetime.utcnow())

        for cog, commands in mapping.items():
           command_signatures = [self.get_something(c) for c in commands]
           if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value='`' + '` `'.join(a for a in command_signatures) + '`', inline=False)

        embed.add_field(name='\0', value='[**Invite**](https://discord.com/api/oauth2/authorize?client_id=768380239255568414&permissions=8&scope=bot) **|** [**Community**](https://discord.gg/XJcThGs4Pu) **|** [**Github**](https://github.com/1olipop/Axley)')

        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):

        embed = discord.Embed(
            color=0xd9e6d1,
            title='Help',
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_author(
            name='Help',
            icon_url='https://cdn.discordapp.com/avatars/768380239255568414/343bbefbd8d9b7166c9b1a0f6b7ccf80.png?size=1024'
        )
        embed.add_field(
            name=cog.qualified_name + ' ' + f'({len([command for command in cog.get_commands()])} commands in total)',
            value='`' + '` `'.join(a.name for a in cog.get_commands()) + '`'
        )
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        return await super().send_group_help(group)
    
    async def send_command_help(self, command):
        embed = discord.Embed(
            color=0xd9e6d1
        )
        embed.set_author(name='{}{}'.format(self.clean_prefix, command.name))
        embed.add_field(name="Usage", value='```yaml\n' + self.get_command_signature(command) + '```')
        embed.add_field(name="Description", value=command.description, inline=False)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Help(bot))