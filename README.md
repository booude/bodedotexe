# BodeDotEXE (Twitch Chat Bot)
## Setup and Run

Requires Python `3.7.3`.

Install necessary packages (locally):

```bash
python3 -m pip install -r requirements.txt
```

Copy `.env.sample` to `.env`

```
cp .env.sample .env

```

Open `.env` and insert the following fields:

| Field          | Explanation                                                           |
|----------------|-----------------------------------------------------------------------|
| `TMI_TOKEN`    | OAuth Token with `oauth:` as a prefix                                 |
| `CLIENT_ID`    | Client ID obtained from Twitch's Developer site                       |
| `CLIENT_SECRET`| Client SECRET obtained from Twitch's Developer site                   |
| `BOT_NICK`     | Twitch name of the Bot                                                | 
| `BOT_PREFIX`   | Prefix for commands the bot should listen to (set to `!` per default) |

Start Bot:

```
python3 bot.py
```

## Add the Bot to Autostart/systemd (Raspberry Pi OS)

Install necessary packages (globally):

```bash
sudo -H python3 -m pip install -r requirements.txt
```

Open the unit file [`bodedotexe.service`](./bodedotexe.service) and check if the path to `bot.py` under `[Serivce]` `ExecStart` is correct.

Copy systemd unit file to unit file directory:

```bash
sudo cp bodedotexe.service /lib/systemd/system
```

Reload all units:

```bash
sudo systemctl daemon-release
```

Enable the BodeDotEXE Unit:

```
sudo systemctl enable bodedotexe.service
```

Start the bot:

```
sudo systemctl start bodedotexe.service
```

Check if the bot is running with:

```
sudo systemctl status bodedotexe.service
```

Check if the output of the bot if an error occurs:

```
sudo systemctl enable bodedotexe.service
```
