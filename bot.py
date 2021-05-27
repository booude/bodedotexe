import io
import os
import json
import unidecode

from dotenv import load_dotenv
from os.path import join
from twitchio.ext import commands
from twitchio.client import Client

dir_path = os.path.dirname(os.path.realpath(__file__))
dotenv_path = join(dir_path, '.env')
load_dotenv(dotenv_path)

TMI_TOKEN = os.environ.get('TMI_TOKEN')
CLIENT_ID = os.environ.get('CLIENT_ID')
BOT_NICK = os.environ.get('BOT_NICK')
BOT_PREFIX = os.environ.get('BOT_PREFIX')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')


def get_channel():
    JSON_FILE = str(os.path.dirname(
        os.path.realpath(__file__))) + '/channels.json'
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
        global CHAN
        CHAN = data['CHANNEL']
    return CHAN


def update_channel(value):
    JSON_FILE = str(os.path.dirname(os.path.realpath(__file__))
                    ) + f'/channels.json'
    data = None
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
    if data is not None:
        data['CHANNEL'] = value
    with open(JSON_FILE, 'w') as json_file:
        json.dump(data, json_file, sort_keys=True, indent=4)


bot = commands.Bot(
    irc_token=TMI_TOKEN,
    client_id=CLIENT_ID,
    nick=BOT_NICK,
    prefix=BOT_PREFIX,
    initial_channels=get_channel()
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
        CHANNEL = ctx.channel.name.lower()
        cmd = message.split(' ')[0][1:]
        if cmd == 'comando' or cmd == 'command' or cmd == 'cmd':
            if(ctx.author.is_mod) or (ctx.author == CHANNEL) or (ctx.author == '1bode'):
                message = message.replace(f'{BOT_PREFIX}{cmd}', '').strip()
                new = message.split()[0]
                if new == 'novo' or new == 'new' or new == 'add' or new == 'edit' or new == 'editar':
                    cmd = message.split()[1]
                    dsc = message.replace(f'{new} {cmd}', '').strip()
                    cmd = unidecode.unidecode(cmd.lower())
                    data = {cmd: dsc}
                    add_command(data, CHANNEL)
                    await ctx.channel.send_me(f'{ctx.author.name} -> Comando "{cmd}" criado/editado com sucesso :D')
                    return
                elif new == 'delete' or new == 'apagar' or new == 'del' or new == 'apaga':
                    cmd = unidecode.unidecode(message.split()[1].lower())
                    if del_command(cmd, CHANNEL) != None:
                        await ctx.channel.send_me(f'{ctx.author.name} -> Comando "{cmd}"" deletado :|')
                        return
                    else:
                        await ctx.channel.send_me(f'{ctx.author.name} -> Comando "{cmd}" não foi encontrado :\ ')
        else:
            msg = get_command(cmd.lower(), CHANNEL)
            words = msg.split()
            for word in words:
                if word == '(_USER_)':
                    words[words.index(word)] = ctx.author.name
                    print(words)
            words = ' '.join(map(str, words))
            await ctx.channel.send_me(f"{words}")
            #await ctx.channel.send_me(f"{ctx.author.name} -> {msg}")
        return


def get_command(cmd, channel):
    COMMAND_FILE = str(os.path.dirname(os.path.realpath(__file__))
                       ) + f'/channeldata/{channel}.json'
    with open(COMMAND_FILE) as json_file:
        command = json.load(json_file)
        return command[unidecode.unidecode(cmd)]


def add_command(data, channel):
    COMMAND_FILE = str(os.path.dirname(os.path.realpath(__file__))
                       ) + f'/channeldata/{channel}.json'
    with open(COMMAND_FILE) as json_file:
        command = json.load(json_file)
        command.update(data)
    with open(COMMAND_FILE, 'w', encoding='utf-8') as json_file:
        json.dump(command, json_file, ensure_ascii=False,
                  indent=4, sort_keys=True)


def del_command(cmd, channel):
    COMMAND_FILE = str(os.path.dirname(os.path.realpath(__file__))
                       ) + f'/channeldata/{channel}.json'
    with open(COMMAND_FILE) as json_file:
        command = json.load(json_file)
        boolean = command.pop(cmd, None)
    with open(COMMAND_FILE, 'w', encoding='utf-8') as json_file:
        json.dump(command, json_file, ensure_ascii=False,
                  indent=5, sort_keys=True)
    return boolean


if __name__ == "__main__":
    bot.run()
