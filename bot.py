import os
import re
import mod

from unidecode import unidecode as ud
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
CHANNELS = mod.get_channel()

bot = commands.Bot(
    irc_token=TMI_TOKEN,
    client_id=CLIENT_ID,
    nick=BOT_NICK,
    prefix=BOT_PREFIX,
    initial_channels=CHANNELS
)

client = Client(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

alias = {'cmd': ['comando', 'command', 'cmd'],
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
        cmds = message.split(' ')[0][1:].lower()
        if cmds in alias['cmd']:
            if(ctx.author.is_mod) or (ctx.author == CHANNEL) or (ctx.author == '1bode'):
                message = message.replace(f'{BOT_PREFIX}{cmds}', '').strip()
                opt = message.split()[0]
                if opt in alias['new']:
                    cmd = message.split()[1]
                    if cmd[0] == BOT_PREFIX:
                        cmd = cmd.split(' ')[0][1:]
                    cmd = ud(cmd.lower())
                    dsc = ' '.join(message.split()[2:])
                    input = {cmd: {"msg": dsc, "count": {}}}
                    mod.add(input, CHANNEL)
                    await ctx.channel.send_me(f'{ctx.author.name} -> Comando "{cmd}" criado/editado com sucesso :D')
                    return
                elif opt in alias['del']:
                    cmd = ud(message.split()[1].lower())
                    if mod.delcmd(cmd, CHANNEL) != None:
                        await ctx.channel.send_me(f'{ctx.author.name} -> Comando "{cmd}" deletado :|')
                        return
                    else:
                        await ctx.channel.send_me(f'{ctx.author.name} -> Comando "{cmd}" não foi encontrado :\ ')
                        return
        else:
            # Procura o comando no commands.json do canal
            try:
                cmd = ud(cmds.lower())
                msg = mod.get(cmd, CHANNEL)

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
                        '$(count)', f'{mod.count(cmd, CHANNEL)}')

                # Substitui todos os $(count nome) pelo incremento +1 de acordo com o nome.
                if msg.find('$(count ') != -1:
                    counter = re.findall(r'\$\(count (.*?)\)', msg)
                    for i in counter:
                        msg = msg.replace(
                            f'$(count {i})', f'{mod.count(cmd, CHANNEL, i)}', 1)

                # Substitui todos os $(random) por um número de 1 a 100.
                while msg.find('$(random)') != -1:
                    msg = msg.replace('$(random)', f'{randint(0,100)}', 1)

                # Substitui todos os $(random.chatter) por um viewer aleatório
                while msg.find('$(random.chatter)') != -1:
                    chatters = await client.get_chatters(CHANNEL)
                    all_chatters = ' '.join(chatters.all).split()
                    msg = msg.replace('$(random.chatter)',
                                      choice(all_chatters))

                # Substitui o $(random.pick) por um valor aleatório da lista informada
                if msg.find('$(random.pick ') != -1:
                    picks = re.findall(r'\$\(random\.pick (.*?)\)', msg)
                    choices = []
                    for i in picks:
                        a = re.split(r"[\"|\']\W+[\"|\']",
                                     picks[picks.index(i)])
                        choices.append(choice(a).replace(
                            '"', '').replace("'", ''))
                        msg = re.sub(r'\$\(random\.pick(.*?)\)',
                                     f'{choices[picks.index(i)]}', msg, 1)

                # Mesmo que $(random) em caso do random possuir um range determinado.
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
                # await ctx.channel.send(f'{msg}')
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
        try:
            AUTHOR = ctx.content.split()[1]
        except IndexError:
            pass
    if ctx.channel.name.lower() == BOT_NICK.lower():
        if AUTHOR in CHANNELS:
            await ctx.send_me(f'Bot JÁ ESTÁ no canal {AUTHOR}')
        else:
            CHANNELS.append(AUTHOR)
            mod.update_channel(CHANNELS)
            mod.file_check(AUTHOR)
            await bot.join_channels(CHANNELS)
            await ctx.send_me(f'Bot ENTROU no canal {AUTHOR}')


# Remove o bot do próprio canal ao utilizar o comando no chat do bot
@bot.command(name='sair')
async def command_leave(ctx):
    AUTHOR = ctx.author.name.lower()
    if AUTHOR == '1bode':
        try:
            AUTHOR = ctx.content.split()[1]
        except IndexError:
            pass
    if ctx.channel.name.lower() == BOT_NICK.lower():
        if AUTHOR in CHANNELS:
            CHANNELS.remove(AUTHOR)
            mod.update_channel(CHANNELS)
            await bot.part_channels([AUTHOR])
            await ctx.send_me(f'Bot SAIU do canal {AUTHOR}')
        else:
            await ctx.send_me(f'Bot NÃO ESTÁ no canal {AUTHOR}')

# Lista os comandos do canal
@bot.command(name='comandos')
async def command_commands(ctx):
    list1 = ', '.join(list(mod.get("@all", *CHANNELS).keys()))
    await ctx.send(f'Comandos do canal: {list1}')

# Teste de comando e tratamento de erro
for i in list(mod.get('@all', *CHANNELS).keys()):
    @bot.command(name=f'{i}')
    async def command_test(ctx):
        await ctx.send(f'{mod.get(i, *CHANNELS)}')
        print('Passou')

# @bot.command(name='followage')
# @bot.command(name='uptime')

if __name__ == "__main__":
    bot.run()
