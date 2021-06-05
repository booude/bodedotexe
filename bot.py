import io
import os
import json
import unidecode
import re

from random import randint, choice
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
    JSON_FILE = str(dir_path) + '/channels.json'
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
        global CHAN
        CHAN = data['CHANNEL']
    return CHAN


def update_channel(value):
    JSON_FILE = str(dir_path) + f'/channels.json'
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

alias = {'cmd': ['comando', 'command', 'cmd', 'commands'],
         'new': ['novo', 'new', 'add', 'adicionar', 'edit', 'editar'],
         'del': ['delete', 'apagar', 'apaga', 'del']}


@bot.event
async def event_ready():
    print(f"{BOT_NICK} ta online!")


@bot.event
async def event_message(ctx):

    if ctx.author.name.lower() == BOT_NICK.lower():
        return

    message = ctx.content
    CHANNEL = ctx.channel.name.lower()
    if message[0] == BOT_PREFIX:
        cmd = message.split(' ')[0][1:].lower()
        if cmd in alias['cmd']:
            if(ctx.author.is_mod) or (ctx.author == CHANNEL) or (ctx.author == '1bode'):
                message = message.replace(f'{BOT_PREFIX}{cmd}', '').strip()
                new = message.split()[0]
                if new in alias['new']:
                    cmd = message.split()[1]
                    if cmd[0] == BOT_PREFIX:
                        cmd = cmd.split(' ')[0][1:]
                    dsc = ' '.join(message.split()[2:])
                    cmd = unidecode.unidecode(cmd)
                    input = {cmd: {"msg": dsc}}
                    command(input, CHANNEL, 'add')
                    await ctx.channel.send_me(f'{ctx.author.name} -> Comando "{cmd}" criado/editado com sucesso :D')
                    return
                elif new in alias['del']:
                    cmd = unidecode.unidecode(message.split()[1].lower())
                    if command(cmd, CHANNEL, 'del') != None:
                        await ctx.channel.send_me(f'{ctx.author.name} -> Comando "{cmd}" deletado :|')
                        return
                    else:
                        await ctx.channel.send_me(f'{ctx.author.name} -> Comando "{cmd}" não foi encontrado :\ ')
        else:
            # Procura o comando no commands.json do canal
            try:
                msg = command(cmd, CHANNEL, 'get')

                # Substitui $(channel) pelo nome do canal
                msg = msg.replace('$(channel)', CHANNEL)

                # Substitui todos os $(user) da resposta por quem foi mencionado após o comando.
                try:
                    msg = msg.replace('$(user)', message.split()[1])

                    # Caso não tenha menção, substitui por quem enviou o comando.
                except IndexError:
                    msg = msg.replace('$(user)', ctx.author.name)

                    # Substitui todos os $(touser) da resposta por quem foi mencionado após o comando.
                try:
                    msg = msg.replace('$(touser)', message.split()[1])

                    # Caso não tenha menção, substitui por um viewer aleatório.
                except IndexError:
                    chatters = await client.get_chatters(CHANNEL)
                    all_chatters = ' '.join(chatters.all).split()
                    msg = msg.replace('$(touser)', choice(all_chatters))

                    # Substitui todos os $(count) pelo incremento +1 do contador do comando utilizado.
                if msg.find('$(count)') != -1:
                    msg = msg.replace(
                        '$(count)', f'{command(unidecode.unidecode(cmd), CHANNEL, "count")}')  # <- refazer com regex?

                # Substitui todos os $(random) da resposta por um número de 1 a 100.
                while msg.find('$(random)') != -1:
                    msg = msg.replace('$(random)', f'{randint(0,100)}', 1)

                # Substitui o $(random.pick) por um valor aleatório da lista informada
                if msg.find('$(random.pick') != -1:
                    picks = re.findall(r'\$\(random\.pick (.*?)\)', msg)
                    choices = []
                    for i in picks:
                        a = re.split(r"[\"|\']\W+[\"|\']",
                                     picks[picks.index(i)])
                        choices.append(choice(a).replace(
                            '"', '').replace("'", ''))
                        #msg = msg.replace('$(random.pick', '').replace(i, choices[picks.index(i)]).replace(')', '')
                        print(choices)
                        msg = re.sub(r'\$\(random\.pick(.*?)\)',
                                     f'{choices[picks.index(i)]}', msg, 1)

                # Caso o random possua um range determinado.
                if msg.find('$(random') != -1:
                    numbers = re.findall(r'\$\(random\.(.*?)\)', msg)
                    value = []
                    for i in numbers:
                        value.append(i.split('-'))
                        try:
                            msg = re.sub(
                                r'\$\(random\.(.*?)\)', f'{randint(int(value[numbers.index(i)][0]),int(value[numbers.index(i)][1]))}', msg, 1)
                        except ValueError:
                            msg = re.sub(r'\$\(random(.*?)\)',
                                         f'{randint(0,100)}', msg, 1)

                # todo: programar ${url fetch http://API} para leagueoflegends
                await ctx.channel.send(f'{msg}')
            except KeyError:
                print(
                    f'Comando "{cmd}" não foi encontrado no canal "{CHANNEL}"')

    # todo: else comandos sem prefixo
    await bot.handle_commands(ctx)


# Insere o bot no próprio canal ao utilizar o comando no chat do bot
@bot.command(name='entrar')
async def command_join(ctx):
    AUTHOR = ctx.author.name.lower()
    if AUTHOR == '1bode':
        AUTHOR = ctx.content.split()[1]
    if ctx.channel.name.lower() == BOT_NICK.lower():
        CONTA = f'#{AUTHOR}'
        if CONTA in CHAN:
            await ctx.send_me(f'Bot JÁ ESTÁ no canal {AUTHOR}')
        else:
            CHAN.append(f'#{AUTHOR}')
            update_channel(CHAN)
            file_check(AUTHOR)
            await bot.join_channels(CHAN)
            await ctx.send_me(f'Bot ENTROU no canal {AUTHOR}')


# Remove o bot do próprio canal ao utilizar o comando no chat do bot
@bot.command(name='sair')
async def command_join(ctx):
    AUTHOR = ctx.author.name.lower()
    if AUTHOR == '1bode':
        AUTHOR = ctx.content.split()[1]
    if ctx.channel.name.lower() == BOT_NICK.lower():
        CONTA = f'#{AUTHOR}'
        if CONTA in CHAN:
            CHAN.remove(f'#{AUTHOR}')
            update_channel(CHAN)
            await bot.part_channels([AUTHOR])
            await ctx.send_me(F'Bot SAIU do canal {AUTHOR}')
        else:
            await ctx.send_me(F'Bot NÃO ESTÁ no canal {AUTHOR}')

# @bot.command(name='followage')
# @bot.command(name='uptime')


def command(input, channel, type):
    COMMAND_FILE = str(dir_path) + f'/data/{channel}/custom_commands.json'
    with open(COMMAND_FILE) as json_file:
        command = json.load(json_file)
    if type == 'get':
        return command[f'{input}']['msg']
    elif type == 'add':
        command.update(input)
    elif type == 'del':
        boolean = command.pop(input, None)
    elif type == 'count':
        try:
            command[f'{input}'][f'{type}'] += 1
        except KeyError:
            command[f'{input}'][f'{type}'] = 1
    with open(COMMAND_FILE, 'w', encoding='utf-8') as json_file:
        json.dump(command, json_file, ensure_ascii=False,
                  indent=4, sort_keys=True)
        if type == 'del':
            return boolean
        elif type == 'count':
            return command[f'{input}'][f'{type}']


def file_check(channel):
    try:
        # Tenta criar pasta para o canal
        os.mkdir(str(dir_path) + f'/data/{channel}')
    except FileExistsError:
        pass
    # Checa se já existe o json. Caso não exista, cria o arquivo com os valores {}
    JSON_FILE = str(dir_path) + f'/data/{channel}/custom_commands.json'
    if os.path.isfile(JSON_FILE) and os.access(JSON_FILE, os.R_OK):
        return True
    else:
        with io.open(os.path.join(JSON_FILE), 'w') as json_file:
            json_file.write(json.dumps({}))


if __name__ == "__main__":
    bot.run()
