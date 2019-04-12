# JJMumbleBot
[![GitHub release](https://img.shields.io/github/release/DuckBoss/JJMumbleBot.svg)](https://github.com/DuckBoss/JJMumbleBot/releases/latest)
[![Packagist](https://img.shields.io/badge/License-GPL-blue.svg)](https://github.com/DuckBoss/JJMumbleBot/blob/master/LICENSE)
[![CodeFactor](https://www.codefactor.io/repository/github/duckboss/jjmumblebot/badge)](https://www.codefactor.io/repository/github/duckboss/jjmumblebot)

A plugin-based python 3 mumble bot with extensive features.


## Features
- <b>Built-in Plugins</b> - Fast, responsive, plugin-based system for easy expandability.
  - <b>Youtube Plugin</b> - Streams youtube songs in the channel.
  - <b>Images Plugin</b> - Posts images from urls or from a local directory in the channel.
  - <b>Sound Board Plugin</b> - Sound Board that plays short wav audio clips in the channel.
  - <b>Randomizer Plugin</b> - Do custom dice rolls, coin flips, etc in the channel.
  - <b><a href="https://github.com/DuckBoss/JJMumbleBot/wiki/Quick-Start">Full list of built-in plugins</a></b>
- <b>Support for adding plugins at runtime.</b>
- <b><a href="https://github.com/DuckBoss/JJMumbleBot/wiki/Plugins">Support for custom plugins</a></b>
- <b>Event logging to keep track of bot usage and command history.</b>
- <b>Multi-Command Input</b> - Input multiple commands in a single line.
- <b>Command Aliases</b> - Register custom aliases to shorten command calls.
- <b>Custom Command Tokens</b> - Custom command recognition tokens (ex: !command, ~command, /command, etc)
- <b>Command Tick Rates</b> - Commands in the queue are processed by the tick rate assigned in the config.
- <b>Multi-Threaded Command Processing</b> - Commands in the queue are handled in multiple threads for faster processing.
- <b>Reconfigurable Command Privileges</b> - The user privileges required to execute commands can be completely reconfigured.

## Future Updates:
NOTE: With v1.7.0 I plan on removing the current download system to play youtube videos and instead migrate to a fully streaming pattern so that no videos are downloaded. <br>This future change will not be noticeable to any users and will be a purely back-end design change. <br>I will create a legacy branch so that users that wish to use the download-system can still use it.
<br>
<b>TL;DR:
- The current youtube plugin downloads videos to a temporary folder (in the config.ini file) before playing it through a vlc instance.
- This can be streamlined by allowing vlc to stream the youtube link directly instead of downloading it first.
- After much testing, the audio quality hasn't been affected and it saved hard drive space.
<br>Got any questions or concerns about this upcoming update? Please post an issue report!</b>

## Wiki
<b> Please check out the wiki for documentation </b> <br>
<a href="https://github.com/DuckBoss/JJMumbleBot/wiki">https://github.com/DuckBoss/JJMumbleBot/wiki</a> <br>
<b> Quick Start guide: </b> <br>
<a href="https://github.com/DuckBoss/JJMumbleBot/wiki/Quick-Start">https://github.com/DuckBoss/JJMumbleBot/wiki/Quick-Start</a> <br>

## Extra Plugins:
<a href="https://github.com/DuckBoss/JJMumbleBot-PluginLibrary">https://github.com/DuckBoss/JJMumbleBot-PluginLibrary</a>

## Legacy Branches:
- <b>pre-v1.3</b> - A legacy branch for pre-v1.3. <br>
v1.3 implemented a new config system that required reconfiguring the config.ini file if a user was updating to v1.3.
- <b>pre-v1.4</b> - A legacy branch for pre-v1.4. <br>
v1.4 implemented a new and upgraded user privilege system that required how user privileges are handled and an update to the plugin template requiring the updating of all plugins.
- <b>pre-v1.5</b> - A legacy branch for pre-v1.5. <br>
v1.5 implemented a way to send commands to the bot, command queues, command tick rates, updated built-in plugins, command aliases, and fixed some major bugs. <br>
- <b>pre-v1.6</b> - A legacy branch for pre-v1.6. <br>
v1.6 implemented a restructured plugin system, updated aliases, and reconfigurable user privileges for all built-in commands. <br>
#### Need a very specific version of the legacy branches? <br>Check out the full list of tags here : <a href="https://github.com/DuckBoss/JJMumbleBot/tags">Release Tags</a>
