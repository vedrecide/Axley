from axley.core.bot import Axley
from discord_slash import SlashCommand


def main() -> None:
    
    try:
        import uvloop
        uvloop.install()
    except:
        pass
    
    bot = Axley()
    SlashCommand(bot, sync_commands = True)
    bot.run()


if __name__ == "__main__":
    main()
