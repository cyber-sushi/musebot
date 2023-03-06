# MuseBot

## <b>A Discord music bot that can play audio from Youtube and Soundcloud</b>

### Available commands:

```
,p - Play a song via Youtube/Soundcloud link or search by keywords. If a song is already playing, put the new one in queue.
,s - Skip the current song.
,loop - Loop the current song.
,queue - Show the current queue.
,remove - Remove the specified song from the queue (use order number from ,queue).
,pause - Pause playback.
,resume - Resume playback.
,skipall - Empty queue and skip the current song.
,leave - Ask the bot to leave the current channel.
,delete - Delete the specified amount of bot's messages from the channel (default 10).
,help - List the available commands.
```

### Create bot token:

1. Create a new application on the [Discord Development Portal](https://discord.com/developers/applications).

2. Click on the application you just created, go to "Bot" on the left and click "Add Bot".

3. Scroll down and tick "Presence Intent", "Server Members Intent" and "Message Content Intent".

4. Click on "Reset Token", then save the given token somewhere. Never share it with anyone.

5. Go to "OAuth2" on the left and then "URL Generator". Tick "bot". Then, in the new tab that just opened, give the bot the necessary permissions for your channel (Connect, Speak, Send Messages, Manage Messages). An invite link for the bot should appear below, use it to add the bot to your server.

### Set up bot:

1. Make sure you have Python 3.5 (or above), `pip3` and `ffmpeg` installed on your system.

**If you're on Windows**, you can install Python 3.x and `pip3` by typing `python3` in your command line or PowerShell and you should get a prompt to automatically install them. Alternatively, you can download Python from [python.org](https://www.python.org/), although this is not recommended since some users reportedly had issues with `pip` afterwards. Then, install `ffmpeg` by following [this tutorial](https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/).

**If you're on Linux**, use your distro's package manager to install those packages directly (e.g. `sudo apt install python3 python3-pip ffmpeg`, `sudo pacman -S python python-pip ffmpeg`, etc, depending on your distro).

2. Download the files from this repo (either `git clone` through your terminal, or download and extract the zip from Github).

3. From your terminal, `cd` into the folder containing the repo files and run `pip3 install -r requirements.txt` to install the necessary dependencies on your system.

4. Open the `token.txt` file and replace the content with the token that you were given in step 4 of "Create bot token", then save.

5. Run the `main.py` file using Python3.

6. Enjoy!

P.S.: the current prefix for bot commands is `,`. To change it, open `main.py` and edit `command_prefix=','` to something else.

### Implementing new modules into the bot:

The bot modules (officially called "cogs") are stored in the `cogs` folder. If you want to make new ones, add them to that folder and remember to load them from the `main.py` file by adding `await bot.load_extension("cogs.<cog_name>")` in the `start_bot` function.
