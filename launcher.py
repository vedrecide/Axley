import json
from bot import Axley

def run():
    bot = Axley()
    
    with open('./config/config.json', 'r') as file:
        config = json.load(file)
        token = config['token']

    bot.run(token)

if __name__ == '__main__':
    run()