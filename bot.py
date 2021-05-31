import discord, os, json

from discord.ext import commands

class Axley(commands.AutoShardedBot):

    def __init__(self):
        self.cogs = os.listdir('./cogs')
        self.owner = 709613711475605544
        super().__init__(
            command_prefix='!',
            intents=discord.Intents.all(),
            owner_id=self.owner
        )

        for file in self.cogs:
            try:
                self.load_extension(f'cogs.{file[:-3]}')
            except Exception as exc:
                raise exc

        def login(self):
            with open('./config/config.json', 'r') as file:
                config = json.load(file)
                token = config['token']

            super().run(token, reconnect=True)