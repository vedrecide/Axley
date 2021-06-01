import discord, os, json

from discord.ext import commands

class Axley(commands.AutoShardedBot):

    def __init__(self):
        super().__init__(
            command_prefix=self.prefix,
            intents=discord.Intents.all(),
            owner_id=709613711475605544
        )

        for file in os.listdir('./cogs'):
            if file.endswith('.py'):
                try:
                    self.load_extension(f'cogs.{file[:-3]}')
                except Exception as exc:
                    raise exc

    def prefix(self, bot, msg):
        return commands.when_mentioned_or('+')(bot, msg)

    def login(self):
        with open('./config/config.json', 'r') as file:
            config = json.load(file)
            token = config['token']

        super().run(token, reconnect=True)