import io
import os
import json

dir_path = os.path.dirname(os.path.realpath(__file__))


def get_channel():
    JSON_FILE = str(dir_path) + '/channels.json'
    with open(JSON_FILE) as json_file:
        data = json.load(json_file)
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


def get(input, channel):
    COMMAND_FILE = str(dir_path) + f'/data/{channel}/custom_commands.json'
    with open(COMMAND_FILE) as json_file:
        command = json.load(json_file)
        if input == '@all':
            return command
        else:
            return command[f'{input}']['msg']


def add(input, channel):
    COMMAND_FILE = str(dir_path) + f'/data/{channel}/custom_commands.json'
    with open(COMMAND_FILE) as json_file:
        command = json.load(json_file)
        command.update(input)
    with open(COMMAND_FILE, 'w', encoding='utf-8') as json_file:
        json.dump(command, json_file, ensure_ascii=False,
                  indent=4, sort_keys=True)


def delcmd(input, channel):
    COMMAND_FILE = str(dir_path) + f'/data/{channel}/custom_commands.json'
    with open(COMMAND_FILE) as json_file:
        command = json.load(json_file)
        result = command.pop(input, None)
    with open(COMMAND_FILE, 'w', encoding='utf-8') as json_file:
        json.dump(command, json_file, ensure_ascii=False,
                  indent=4, sort_keys=True)
        return result


def count(input, channel, var='count'):
    COMMAND_FILE = str(dir_path) + f'/data/{channel}/custom_commands.json'
    with open(COMMAND_FILE) as json_file:
        command = json.load(json_file)
    try:
        command[f'{input}']['count'][f'{var}'] += 1
    except KeyError:
        command[f'{input}']['count'].update({f'{var}': 1})
    with open(COMMAND_FILE, 'w', encoding='utf-8') as json_file:
        json.dump(command, json_file, ensure_ascii=False,
                  indent=4, sort_keys=True)
        return command[f'{input}'][f'count'][f'{var}']


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
