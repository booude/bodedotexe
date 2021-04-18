import os
import json
import unidecode

from pathlib import Path
from dotenv import load_dotenv
from os.path import join, dirname
from twitchio.ext import commands
from twitchio.client import Client

dir_path = os.path.dirname(os.path.realpath(__file__))
dotenv_path = join(dir_path, '.env')
load_dotenv(dotenv_path)

TMI_TOKEN = os.environ.get('TMI_TOKEN')
CLIENT_ID = os.environ.get('CLIENT_ID')
BOT_NICK = os.environ.get('BOT_NICK')
BOT_PREFIX = os.environ.get('BOT_PREFIX')
CHANNEL = os.environ.get('CHANNEL')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

JSON_FILE = str(os.path.dirname(os.path.realpath(__file__))) + '/data.json'
COMMAND_FILE = str(os.path.dirname(
    os.path.realpath(__file__))) + '/commands.json'

bot = commands.Bot(
    irc_token=TMI_TOKEN,
    client_id=CLIENT_ID,
    nick=BOT_NICK,
    prefix=BOT_PREFIX,
    initial_channels=[CHANNEL]
)

client = Client(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)


@bot.event
async def event_ready():
    print(f"{BOT_NICK} ta online!")

@bot.event
async def event_message(ctx):
    if ctx.author.name.lower() == BOT_NICK.lower():
        return
    await bot.handle_commands(ctx)

@bot.event
async def event_message(ctx):

    if ctx.author.name.lower() == BOT_NICK.lower():
        return

    message = ctx.content
    if message[0] == BOT_PREFIX:
        cmd = message.split(' ')[0][1:]
        if cmd == 'comando':
            if(ctx.author.is_mod) or (ctx.author == CHANNEL):
                message = message.replace('!comando', '').strip()
                new = message.split()[0]
                if new == 'novo':
                    cmd = message.split()[1]
                    cmd2 = unidecode.unidecode(cmd.lower())
                    dsc = message.replace(f'novo {cmd}','').strip()
                    data={cmd2: dsc}
                    add_command(data)
                    await ctx.channel.send_me(f'{ctx.author.name} -> Comando criado/editado com sucesso :D')
                    return
        else:
            msg = get_command(cmd.lower())
            await ctx.channel.send_me(f"{ctx.author.name} -> {msg}")
        return

def get_command(cmd):
    with open(COMMAND_FILE) as json_file:
        command = json.load(json_file)
        return command[unidecode.unidecode(cmd)]

def add_command(data):
    with open(COMMAND_FILE) as json_file:
        command = json.load(json_file)
        command.update(data)
    with open(COMMAND_FILE, 'w', encoding='utf-8') as json_file:
        json.dump(command, json_file,ensure_ascii=False,indent=4,sort_keys=True)

if __name__ == "__main__":
    bot.run()
