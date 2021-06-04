import discord, os, json, pymongo

from discord.ext import commands

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
            case_insensitive=True
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