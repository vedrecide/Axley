import discord
import os
import logging
import json

from discord.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient as MotorClient
from motor.motor_asyncio import AsyncIOMotorDatabase as BotDatabase
from typing import List


class Axley(commands.AutoShardedBot):
    def __init__(self):
        self.cool_emojis = {
            "tick": "<a:whitetick:849331491699556412>",
            "cross": "<a:redcross:849331580300165140>",
        }
        self.initiate = {
            'command_prefix': self.get_guild_prefixes,
            'intents': discord.Intents.all(),
            'owner_id': self.config['owner'],
            'case_insensitive': True,
            'allowed_mentions': discord.AllowedMentions(
                roles=False,
                everyone=False,
                users=True
            ),
            'description': 'A multi-purpose, open source Bot for your Discord server',
            'help_command': None
        }
        self.github_repo = "https://github.com/1olipop/Axley"
        super().__init__(**self.initiate)
        self._load_cogs()

    def _load_cogs(self):
        for file in self._cogs:
            if file.endswith(".py"):
                try:
                    self.load_extension(f"axley.cogs.{file[:-3]}")
                except Exception as exc:
                    print(exc)

    def db(self) -> BotDatabase:
        cluster = MotorClient(self.config['mongo_url'])
        db = cluster["database"]

        return db

    @property
    def logger(self) -> logging.Logger:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            fmt='%(asctime)s:%(name)s: [%(levelname)s] => %(message)s',
            datefmt='%m/%d/%y %H:%M:%S'
        )
        file_handler = logging.FileHandler('start.log')
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        return logger

    @property
    def _cogs(self) -> List[str]:
        return os.listdir('./axley/cogs')

    @property
    def config(self):
        with open('./axley/config/config.json', 'r') as file:
            config = json.load(file)

        return config

    def run(self):
        super().run(self.config['token'], reconnect=False)

    async def on_connect(self):
        self.logger.info("Bot connected to Discord")

    async def on_disconnect(self):
        try:
            self.logger.info("Bot disconnected from Discord")
        except Exception as e:
            self.logger.error(e)

    async def shutdown(self):
        self.logger.info("Closing connection to Discord")
        await super().close()

    async def get_guild_prefixes(
        self, bot: commands.Bot, msg: discord.Message
    ) -> str or List[str]:
        db = self.db()
        collection = db["prefix"]
        prefixes = []

        data = await collection.find_one({"_id": msg.guild.id})

        if not data:
            prefixes = "+"
        else:
            for _prefixes in data['prefix']:
                prefixes.append(_prefixes)

        return prefixes

    async def on_ready(self):
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"+help in {len(self.guilds)} guilds",
            )
        )

        self.logger.info("Logged in as {}".format(self.user))
