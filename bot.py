import os
import json

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

@bot.command(name='elo')
async def count_command(ctx):
    count = get_count()
    await ctx.send_me(f'Elo: Diamante 4 ({count} LP )')


@bot.command(name='add')
async def command_add(ctx):
    if(ctx.author.is_mod) or (ctx.author == CHANNEL):

        command_string = ctx.content
        command_string = command_string.replace('!add', '').strip()
        value = 0
        try:
            value = int(command_string)
        except ValueError:
            value = 0
        count = get_count()
        count = count + value
        update_count(count)
        await ctx.send(f'Doritos mudou pra {count}')
'''
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
                    dsc = message.replace(f'novo {cmd}','').strip()
                    data={cmd: dsc}
                    add_command(data)
                    await ctx.channel.send_me(f'{ctx.author.name} -> Comando criado/editado com sucesso :D')
                    return
        else:
            msg = get_command(cmd)
            await ctx.channel.send_me(f"{ctx.author.name} -> {msg}")
        return


 @bot.command(name='chat')
 async def get_chatters(ctx):
     chatters = await client.get_chatters(CHANNEL)
     all_chatters = ' '.join(chatters.all)
     await ctx.send_me(f"{ctx.author.name} -> no chat: {all_chatters}")'''


def get_count():
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
        return data['elo']


def update_count(count):
    data = None
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
    if data is not None:
        data['elo'] = count
    with open(JSON_FILE, 'w') as json_file:
        json.dump(data, json_file, sort_keys=True, indent=4)


def get_command(cmd):
    with open(COMMAND_FILE) as json_file:
        command = json.load(json_file)
        return command[cmd]

def add_command(data):
    with open(COMMAND_FILE) as json_file:
        command = json.load(json_file)
        command.update(data)
    with open(COMMAND_FILE, 'w') as json_file:
        json.dump(command, json_file)

if __name__ == "__main__":
    # launch bot
    bot.run()
