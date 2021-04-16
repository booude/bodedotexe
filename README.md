# Twitch Count Bot 

Simple Twitch bot template with three commands:

 * `!count`: shows the `count` from [`data.json`](./data.json)
 * `!add NUMBER`: adds `NUMBER` to `count` in  [`data.json`](./data.json)
 * `!sub NUMBER`: subtracts `NUMBER` from `count` in  [`data.json`](./data.json)

## Setup Video
<a href="https://youtu.be/CPVSoowZhVw">
    <img src="./images/youtube_thumbnail.png" width="500"/>
</a>

[Youtube Video Link](https://youtu.be/CPVSoowZhVw)

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

| Field        | Explanation                                                           |
|--------------|-----------------------------------------------------------------------|
| `TMI_TOKEN`  | OAuth Token with `oauth:` as a prefix                                 |
| `CLIENT_ID`  | Client ID obtained from Twitch's Developer site                       |
| `BOT_NICK`   | Twitch name of the Bot                                                | 
| `BOT_PREFIX` | Prefix for commands the bot should listen to (set to `!` per default) |
| `CHANNEL`    | The name of the your Twitch channel you want the bot to run at        |

Start Bot:

```
python3 bot.py
```

## Add the Bot to Autostart/systemd (Raspberry Pi OS)

Install necessary packages (globally):

```bash
sudo -H python3 -m pip install -r requirements.txt
```

Open the unit file [`twitch_count_bot.service`](./twitch_count_bot.service) and check if the path to `bot.py` under `[Serivce]` `ExecStart` is correct.

Copy systemd unit file to unit file directory:

```bash
sudo cp twitch_count_bot.service /lib/systemd/system
```

Reload all units:

```bash
sudo systemctl daemon-release
```

Enable the Twitch Count Bot Unit:

```
sudo systemctl enable twitch_count_bot.service
```

Start the bot:

```
sudo systemctl start twitch_count_bot.service
```

Check if the bot is running with:

```
sudo systemctl status twitch_count_bot.service
```

Check if the output of the bot if an error occurs:

```
sudo systemctl enable twitch_count_bot.service
```

## Credits
![K0nze Logo](./images/k_logo_30x30.png "Logo") Created by Konstantin (Konze) Lübeck

 * Discord: [discord.k0nze.gg](https://discord.k0nze.gg) 
 * Twitch: [twitch.tv/k0nze](https://twitch.tv/k0nze) 
 * Youtube: [youtube.com/k0nze](https://youtube.com/k0nze) 
 * Twitter: [twitter.com/k0nze_gg](https://twitter.com/k0nze_gg) 
 * Instagram: [instagram.com/k0nze.gg](https://instagram.com/k0nze.gg) 
