# NOTICE:
#### I will update this release to match the master branch until it is ready for a full release.<br>Only download this pre-release/early-release-build if you understand that there are bound to be issues.
#### v3.0.0 does not currently have updated documentation. I am working on it to be ready for the full release.

## Python Version
JJMumbleBot has been updated through multiple python revisions,
and with this update it will now require Python 3.7 or higher.

## Aliases
There is now a global_aliases.csv file that must be placed in the JJMumbleBot/cfg/ directory, which will function similarly as the previous versions of the aliases.csv file.<br>
In addition, individual plugins now require an aliases.csv file which will contain any command aliases related to that plugin.<br>
The directory structure of this new system can be seen in the Plugins section below.

## Plugins
Plugins are now separated into 'core' and 'extensions' folders.<br>
Third party plugins that extend the functionality of the bot should be placed in the 'extensions' folder.<br>
Various changes such as separating the help data and metadata into individual files have been made to improve the development and functionality of plugins.<br>
**Due to these changes, all existing custom third party plugins must be updated to the new format.**
<hr>

### Plugin Development Changes
Plugins now require the following base heirarchy:
- **plugin_name/**
   - **resources/**
       - **strings.py**:*contains static string references using in the metadata/script*
   - **utility/** (optional directory to store utility scripts for your plugin)
   - **help.html** : *contains the help data for the plugin commands*
   - **metadata.ini** : *contains plugin information and plugin-specific settings*
   - **privileges.csv** : *contains user privilege requirements for plugin commands*
   - **aliases.csv**: *contains aliases specifically to commands in the plugin*
   - **plugin_name.py** : *main driver python script for the plugin*

Any additional utility files, scripts, folders or media can be added to this.
**For more information on creating custom plugins, look at this documentation. ADD DOC HERE**
<hr>

### Core Commands Plugin [NEW]
The core commands of the bot service has now been separated into it's own core plugin.
This plugin contains all critical service commands for the bot.
This includes all commands relating to aliases, rebooting, refreshing plugins, exiting the bot, etc.

Added new commands:
- Clears the bot command history.
```!clearhistory```
<hr>

### Bot Commands Plugin
Added new commands:
- Removes the current channel if it's created by the bot service.
```!remove```
- Removed 'spam_test' command.
<hr>

### Text To Speech Plugin [NEW]
A plugin that allows users to type messages that can be read out by various TTS voices.
The plugin also allows users to download TTS clips to be played at a later time like the sound board plugin.
- Stream TTS message with specified voice`
```!tts 'voice_name' 'message'```
- Displays a list of all the TTS voices available
```!ttsvoices```
- Download TTS message with specified voice into a clip
```ttsdownload 'clip_name' 'voice_name' 'message'```
- Play existing TTS clip
```!ttsplay 'clip_name'```
- Delete existing TTS clips
```!ttsdelete 'clip_name'```
- Adjust TTS volume
```!ttsv '0...1'```
- And MORE...
```...```
**For a full list of commands, please check the documentation provided here. ADD DOC HERE**
<hr>

# Other Updates

### Removed Web Interface Plugin
The previous web interface plugin implementation was very messy and experimental.
I will be releasing v3.0.0 without a web interface plugin, and will work on implementing
it properly in the near future.

### Auto-Updater Plugin [Experimental]
I'm working on an auto-updater plugin which will keep plugins automatically updated.
There's no guarantee that this will be released with v3.0.0.

### New Default Aliases
**For the full list of default aliases, please check the documentation provided here. ADD DOC HERE**

### Safe Mode Changes
Users can now set what plugins are included in safe mode by modifying the 'SafeModePlugins' list in their bot config. 
Please note that you should always include the 'bot_commands' and 'core_commands' plugins in the list of safe mode plugins!
