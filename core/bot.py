import discord, os, dotenv

from discord.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient
from cogs.help import AxleyHelpCommand

dotenv.load_dotenv()

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


    def load_cogs(self):
        for file in self.bot_cogs:
            if file.endswith('.py'):
                try:
                    self.load_extension(f'cogs.{file[:-3]}')
                    print("  Loaded '{}' cog".format(file[:-3]))
                except Exception as exc:
                    raise exc


    def db(self):
        cluster = AsyncIOMotorClient(os.getenv("MONGO_URL"))
        db = cluster['database']

        return db

    def run(self):
        self.load_cogs()

        super().run(os.getenv("TOKEN"), reconnect=True)

    async def prefix(self, bot, msg):
        db = self.db()
        collection = db['prefix']

        data = await collection.find_one({'_id': msg.guild.id})

        if not data:
            prefix = '+'
        else:
            prefix = data['prefix']

        return commands.when_mentioned_or(prefix)(bot, msg)

    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'+help in {len(self.guilds)} guilds'))
        print('Logged in as {}'.format(self.user))