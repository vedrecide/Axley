import discord, os, json, pymongo, io, re, zlib, aiohttp

from discord.ext import commands

class AxleyHelpCommand(commands.HelpCommand):

    def __init__(self):
        super().__init__()

    def get_something(self, command):
        return '%s' % (command.qualified_name)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help", color=discord.Color.blurple())
        for cog, commands in mapping.items():
           filtered = await self.filter_commands(commands, sort=True)
           command_signatures = [self.get_something(c) for c in filtered]
           if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value='`' + '` `'.join(a for a in command_signatures) + '`', inline=False)
        '''
        embed = discord.Embed(
            color=discord.Color.blue()
        )
        embed.set_author(name='Help')
        for cog in mapping:
            embed.add_field(name=f'{cog.qualified_name}', value=f"`{[command.name for command in mapping[cog]]}`", inline=False)

        #embed.add_field(name='Prompt `{}help <command>` for more information'.format(self.clean_prefix), value='**[Github](https://github.com/1olipop/Axley)** `|` **[Community](http://localhost:5000)**', inline=False)
        
        #'{cog.qualified_name}: {[command.name for command in mapping[cog]]}'
        '''
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        return await super().send_cog_help(cog)

    async def send_group_help(self, group):
        return await super().send_group_help(group)
    
    async def send_command_help(self, command):
        embed = discord.Embed(
            color=discord.Color.dark_green()
        )
        embed.set_author(name='{}{}'.format(self.clean_prefix, command.name))
        embed.add_field(name="Usage", value='```yaml\n' + self.get_command_signature(command) + '```')
        embed.add_field(name="Description", value=command.description, inline=False)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

class Axley(commands.AutoShardedBot):

    def __init__(self):
        self.bot_cogs = os.listdir('./cogs')
        self.cool_emojis = {
            'tick': '<a:whitetick:849331491699556412>',
            'cross': '<a:redcross:849331580300165140>'
        }
        self.owner = 709613711475605544
        super().__init__(
            command_prefix=self.prefix,
            intents=discord.Intents.all(),
            owner_id=self.owner,
            case_insensitive=True,
            help_command=AxleyHelpCommand()
        )

        for file in self.bot_cogs:
            if file.endswith('.py'):
                try:
                    self.load_extension(f'cogs.{file[:-3]}')
                except Exception as exc:
                    raise exc

    def db(self):
        with open('./config/config.json', 'r') as file:
            config = json.load(file)
            mongo_url = config['mongo_url']

        cluster = pymongo.MongoClient(mongo_url)
        db = cluster['database']

        return db

    def prefix(self, bot, msg):
        db = self.db()
        collection = db['prefix']

        data = collection.find_one({'_id': msg.guild.id})

        if not data:
            prefix = '+'
        else:
            prefix = data['prefix']

        return commands.when_mentioned_or(prefix)(bot, msg)

    async def on_ready(self):
        print('[*] Ready')