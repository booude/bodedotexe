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

    message = ctx.content
    if message[0] == BOT_PREFIX:
        cmd = message.split(' ')[0][1:]
        if cmd == 'comando' or cmd == 'command' or cmd == 'cmd':
            if(ctx.author.is_mod) or (ctx.author == CHANNEL):
                message = message.replace(f'!{cmd}', '').strip()
                new = message.split()[0]
                if new == 'novo' or new == 'new' or new == 'add' or new == 'edit' or new == 'editar':
                    cmd = message.split()[1]
                    cmd2 = unidecode.unidecode(cmd.lower())
                    dsc = message.replace(f'{new} {cmd}', '').strip()
                    data = {cmd2: dsc}
                    add_command(data)
                    await ctx.channel.send_me(f'{ctx.author.name} -> Comando criado/editado com sucesso :D')
                    return
                elif new == 'delete' or new == 'apaga' or new == 'del':
                    cmd = message.split()[1]
                    cmd2 = unidecode.unidecode(cmd.lower())
                    if del_command(cmd2) != None:
                        await ctx.channel.send_me(f'{ctx.author.name} -> Comando deletado :|')
                        return
                    else:
                        await ctx.channel.send_me(f'{ctx.author.name} -> Comando "{cmd2}" não foi encontrado :\ ')
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
        json.dump(command, json_file, ensure_ascii=False,
                  indent=4, sort_keys=True)


def del_command(cmd):
    with open(COMMAND_FILE) as json_file:
        command = json.load(json_file)
        boolean = command.pop(cmd, None)
    with open(COMMAND_FILE, 'w', encoding='utf-8') as json_file:
        json.dump(command, json_file, ensure_ascii=False,
                  indent=5, sort_keys=True)
    return boolean


if __name__ == "__main__":
    bot.run()
