## Important Notice To Everyone
One of the main dependencies of this project, and very reputable and widely used package 'youtube-dl' has been removed from Github due to a DMCA takedown.
For more information please refer to the official notice from Github: [Youtube-dl DMCA Notice](https://github.com/github/dmca/blob/master/2020/10/2020-10-23-RIAA.md)
### How does this impact JJMumbleBot?
JJMumbleBot, as well as every other media bot, uses youtube-dl to interface with youtube and provide downloading/streaming services.
As a result of this DMCA on youtube-dl, youtube-related functions of this bot may stop working in the near future.<br/>

I will continue working on this project, but please be aware that youtube-related commands such as `!link` or `!sbdownload` may stop working.
I will work on solutions to these problems, this notice is to just update everyone on the situation.
### Notice to New Users:
Unfortunately, since youtube-dl is no longer available through it's main distribution channel, in order for this bot to work you will need to have an existing version installed on your computer. 
This means that using the `pip` python command to download the package might not work.

Currently, the youtube-dl download page still works (as of 10/24/2020):
https://youtube-dl.org/

### The Good News:
On the bright side, JJMumbleBot does a LOT more than just streaming youtube content.
As a result, this issue will only affect the media plugin, and specific youtube-related commands in the sound board plugin.
Everything else should continue working as expected.

<hr>

# JJMumbleBot
[![GitHub release](https://img.shields.io/github/release/DuckBoss/JJMumbleBot.svg)](https://github.com/DuckBoss/JJMumbleBot/releases/latest)
[![Packagist](https://img.shields.io/badge/License-GPL-blue.svg)](https://github.com/DuckBoss/JJMumbleBot/blob/master/LICENSE)
<br>
[![CodeFactor](https://www.codefactor.io/repository/github/duckboss/jjmumblebot/badge)](https://www.codefactor.io/repository/github/duckboss/jjmumblebot)
[![Build Status](https://travis-ci.com/DuckBoss/JJMumbleBot.svg?branch=master)](https://travis-ci.com/DuckBoss/JJMumbleBot)

A plugin-based All-In-One mumble bot solution in python 3.7+ with extensive features and support for custom plugins.

## Features  🚀
- <b>Built-in Plugins</b> - Fast, responsive, plugin-based system for easy expandability.
  - <b>Media Plugin</b> - Streams Youtube/SoundCloud audio in the channel.
    - Youtube Playlist Support
    - Video Thumbnails
    - Queue System
    - Direct Youtube/SoundCloud Link Support
    - Search/Browse Youtube Support
    - Mumble Whisper Support
  - <b>Images Plugin</b> - Posts images from urls or from a local directory in the channel.
    - Local Images Support
    - Direct Link Images Support
  - <b>Sound Board Plugin</b> - Sound Board that plays short wav audio clips in the channel.
    - Local Audio Clips Support
    - Download and Play Audio Clips
    - Mumble Whisper Support
  - <b>Randomizer Plugin</b> - Do custom dice rolls, coin flips, etc in the channel.
    - Dice Rolls
    - Coin Flips
  - <b>Whisper Plugin</b> - Mumble Whisper support for audio data.
  - <b>Bot Commands Plugin</b> - Enhanced interactivity and management commands.
  - <b><a href="https://github.com/DuckBoss/JJMumbleBot/wiki">Full list of built-in plugins</a></b>
- <b>Web Interface</b> - Control and manage the bot with an optional web interface.
- <b>Auto-Updater</b> - A System to update dependencies through bot commands.
- <b><a href="https://github.com/DuckBoss/JJMumbleBot/wiki/Plugins">Support for custom plugins</a></b>
- <b>Pseudo-GUI System [PGUI]</b> - A pseudo graphical user interface built with html tags.
- <b>Event logging to keep track of bot usage and command history.</b>
- <b>Multi-Command Input</b> - Input multiple commands in a single line.
- <b>Command Aliases</b> - Register custom aliases to shorten command calls, and do some nifty command combinations.
- <b>Custom Command Tokens</b> - Custom command recognition tokens (ex: !command, ~command, /command, etc)
- <b>Command Tick Rates</b> - Commands in the queue are processed by the tick rate assigned in the config.
- <b>Multi-Threaded Command Processing</b> - Commands in the queue are handled in multiple threads for faster processing.
- <b>Reconfigurable Command Privileges</b> - The user privileges required to execute commands can be completely reconfigured.
- <b>User Privileges System</b> - Set user privileges to server users to limit the command usage on a per-user basis.
- <b>Extensive Callback System</b> - Create custom callbacks to mumble server events and more.

## Screenshots
#### Audio Interface System (youtube plugin, sound board plugin, etc)
![AudioInterfaceImage](https://user-images.githubusercontent.com/20238115/88094381-75fcf600-cb61-11ea-8113-495db67a415d.png)
#### Web Interface - Main Page
![WebInterfaceImage](https://user-images.githubusercontent.com/20238115/88028907-44efd780-cb07-11ea-85b8-21cc7d841ec3.png)
#### Web Interface - Media Player
![MediaPlayerImage](https://user-images.githubusercontent.com/20238115/88487343-429bdc00-cf52-11ea-9af7-81289c1949a3.png)

## Installation And Setup 🏃
- Download and install python 3.7+
    - Linux: Depends on distribution
    - Mac OSX: <a href="https://www.python.org/downloads/mac-osx/">Mac OSX Python Downloads</a>
    - Windows: <a href="https://www.python.org/downloads/windows/">Windows Python Downloads</a>
- Install project dependencies
    - `pip install -r requirements.txt`
    - <b><a href="https://ffmpeg.org/">FFmpeg</a> and <a href="https://www.videolan.org/vlc/index.html">VLC</a> must be installed on your system</b>
    - <b>Note: You must have libopus installed, and installation varies by operating system.</b>
    - <b>Note: v4.2+ requires FFmpeg and VLC. v4.1 and under uses only VLC.</b>
- Please make sure your murmur server supports sending text messages of over 90000 characters. (Configurable in your murmur.ini file)
- Please check the <a href="https://duckboss.github.io/JJMumbleBot/wiki/">Wiki Pages</a> for setup procedures and more information.
- JJMumbleBot has been tested on Linux/Windows platforms. MacOS is untested, but it should theoretically work.

## Documentation 📝
<b><a href="https://duckboss.github.io/JJMumbleBot/wiki/new/whats_new.html">JJMumbleBot Documentation Wiki</a></b> <br>
<b><a href="https://duckboss.github.io/JJMumbleBot/wiki/faq.html">F.A.Q - Solve common issues easily</a></b> <br>
<b><a href="https://duckboss.github.io/JJMumbleBot/wiki/requirements.html">Requirements and Dependencies</a></b> <br>
<b><a href="https://duckboss.github.io/JJMumbleBot/wiki/quick_start.html">Quick Start Guide</a></b> <br>
<b><a href="https://duckboss.github.io/JJMumbleBot/wiki/qsu/qsu.html">Quick Setup Utility - Web Interface For Config.ini File Creation</a></b> <br>

## Extra Plugins:
<a href="https://github.com/DuckBoss/JJMumbleBot-PluginLibrary">https://github.com/DuckBoss/JJMumbleBot-PluginLibrary</a>

### Got any questions or concerns? Please post an issue report 👋
#### Or email me @ <a href="mailto:duckboss@kakao.com">duckboss@kakao.com</a>
