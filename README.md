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
- <b>Docker Support</b> - Deploy JJMumbleBot on the cloud or on any docker-supported device.
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
#### Web Interface - Commands Page
<img width=500 src="https://user-images.githubusercontent.com/20238115/106063315-f9c20d00-60c5-11eb-9846-25d3b79c551f.png" alt="Commands Tab Image"/>
#### Web Interface - Main Page
<img width=500 src="https://user-images.githubusercontent.com/20238115/106061227-1f014c00-60c3-11eb-9540-dd8a9222438d.png" alt="Audio Tab Image"/>
#### Web Interface - Main Page
<img width=500 src="https://user-images.githubusercontent.com/20238115/106063400-1e1de980-60c6-11eb-8ab0-c52b1f097186.png" alt="Debug Tab Image"/>

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

## Docker Setup 🏃
- Please check the <a href="https://duckboss.github.io/JJMumbleBot/wiki/general/docker.html">Docker Setup Wiki Page</a> for more information.

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
