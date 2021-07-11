# JJMumbleBot
<h4 align="center">A plugin-based All-In-One mumble bot solution in python 3.7+ with extensive features and support for custom plugins.</h4>
<p align="center">
  <a href="https://github.com/DuckBoss/JJMumbleBot/releases/latest"><img src="https://img.shields.io/github/release/DuckBoss/JJMumbleBot.svg"></a>
  <a href="https://github.com/DuckBoss/JJMumbleBot/blob/master/LICENSE"><img src="https://img.shields.io/badge/License-GPL-blue.svg"></a>
  <a href="https://www.codefactor.io/repository/github/duckboss/jjmumblebot"><img src="https://www.codefactor.io/repository/github/duckboss/jjmumblebot/badge"></a>
  <a href="https://travis-ci.com/DuckBoss/JJMumbleBot"><img src="https://travis-ci.com/DuckBoss/JJMumbleBot.svg?branch=master"></a><br>
</p>
<p align="center">
  :mailbox: <b>How to reach me:</b> <a href="mailto:duckboss@kakao.com" alt="duckboss@kakao.com">duckboss@kakao.com</a><br>
  :information_desk_person: <b>Join my Discord:</b> <a href="https://discord.gg/7hHwyk85Wx">https://discord.gg/7hHwyk85Wx</a>
</p>




  ## Features  🔥


  ### Feature-rich Command and Alias System
  - <b>Multi-Command Input</b> - Input multiple commands in a single line.
  - <b>Command Aliases</b> - Register custom aliases to shorten command calls, and do some nifty command combinations.
  - <b>Custom Command Tokens</b> - Custom command recognition tokens (ex: !command, ~command, /command, etc)
  - <b>Command Tick Rates</b> - Commands in the queue are processed by the tick rate assigned in the config.
  - <b>Multi-Threaded Command Processing</b> - Commands in the queue are handled in multiple threads for faster processing.
  - <b>Reconfigurable Command Privileges</b> - The user privileges required to execute commands can be completely reconfigured.

  ### Built-in Web Interface
  - <b>A fully featured web interface is included in JJMumbleBot by default</b>

  ### Built-in Plugins
  #### Fast Multi-threaded, responsive, plugin-based system for easy expandability.
  The list of features shown under each plugin is not inclusive of all the features the plugins contain,
  but only the most important features.<br/>
  **This means that most plugins have more features than the ones listed below!**
  
  | Server/Web Administration Plugins List | Features |
  | :---: | :--- |
  | Auto Updater Plugin | <p>A System to update dependencies through bot commands</p><details><summary><strong>Click To List Features</strong></summary><ul><li>Check For Dependency Updates</li><li>Update Dependencies Directly Through The Bot</li></ul></details> |
  | Bot Commands Plugin | <p>Enhanced interactivity and management commands</p><details><summary><strong>Click To List Features</strong></summary><ul><li><b>User Administration:</b> Kick/User/Ban/Move/Mute/Deafen Commands</li><li><b>Channel Administration:</b> Create/Remove/Rename Temporary and Permanent Channels</li><li><b>User Privileges:</b> Set User Privileges, Blacklist/Whitelist Users</li></ul></details>|
  | Core Commands Plugin | <p>Core bot administration commands</p><details><summary><strong>Click To List Features</strong></summary><ul><li><b>Plugin Administration:</b>Start/Stop/Restart Plugins At Runtime</li><li><b>Bot Information:</b> Set Mumble Comment, Display Version/Uptime/About</li><li><b>Alias System</b>: Add/Update/Import Aliases For Commands At Runtime</li><li><b>Command Permission System</b>: Add/Update/Import Permissions For Commands At Runtime</li><li><b>Command History</b>: Display Recently Used Commands</li></ul></details> | 
  | Server Tools Plugin | <p>Additional administrative features and server callback-related events</p><details><summary><strong>Click To List Features</strong></summary><ul><li>Display A Link To The JJMumbleBot Wiki</li><li><b>User Connection Sounds:</b> Play Audio Clip When Users Join</li></ul></details> |
  | Whisper Plugin | <p>Mumble Whisper integration for audio data, which allows audio to be played to specific users only.</p><details><summary><strong>Click To List Features</strong></summary><ul><li><b>User Whisper Support:</b> Set Mumble's whisper to single/multiple users.</li><li><b>Channel Whisper Support:</b> Set Mumble's whisper to channels.</li></ul></details> |
  | Audio Commands Plugin | <p>Full audio control of the bot with additional audio features like "audio ducking"</p><br/><details><summary><strong>Click To List Features</strong></summary><ul><li>Queue Audio/Video Clips</li><li>Audio Controls - Pause/Resume/Shuffle/Skip/Loop/Seek/Stop</li><li>Audio Ducking Integration (Method of lowering currently playing audio when users are speaking)</li></ul></details> |
  | Web Server Plugin | <p>Control and manage the bot with an optional web interface, which allows remote usage of the bot and administrative features.<br/>This is a popular feature that server owners utilize to manage the bot.</p><details><summary><strong>Click To List Features</strong></summary><ul><li><b>Web Interface Security:</b> HTTPS/SSL Support</li><li><b>Web Server Commands</b>: Start/Stop The Web Server Through Commands</li><li>Optional Automatic Certificate Generation</li></ul></details> |
  
  | Entertainment/Media Plugins List | Features |
  | :---: | :--- |
  | Media Plugin  | <p>Stream Youtube videos/playlists or SoundCloud tracks with thumbnail image support</p><br/><details><summary><strong>Click To List Features</strong></summary><ul><li>Youtube Playlist Support</li><li>Video Thumbnails</li><li>Audio Queue System</li><li>Direct Youtube/SoundCloud Link Support</li><li>Search/Browse Youtube Support</li><li>Mumble Whisper Integration</li></ul></details>  |
  | Images Plugin  | <p>Display images from local files or download images from the internet</p></br><details><summary><strong>Click To List Features</strong></summary><ul><li>Local Images Support</li><li>Direct URL Images Support</li><li>Audio Queue System</li><li>Direct Youtube/SoundCloud Link Support</li><li>Search/Browse Youtube Support</li><li>Mumble Whisper Integration</li></ul></details>  |
  | Sound Board Plugin | <p>Stream audio clips from local files or download audio tracks from Youtube</p><br/><details><summary><strong>Click To List Features</strong></summary><ul><li>Local Audio Clips Support</li><li>Download And Play Audio Clips From Youtube</li><li>Mumble Whisper Integration</li><li>Play Random Audio Clips From Library</li><li>Supports Popular File Types</li></ul></details> |
  | Randomizer Plugin | <p>Do custom dice rolls, coin flips, etc. in the channel</p></br><details><summary><strong>Click To List Features</strong></summary><ul><li>Custom Dice Rolls</li><li>Coin Flips</li><li>Standard Dice Rolls (d6, d12, d100, etc.)</li></ul></details> |
  | Text-To-Speech Plugin | <p>Full-featured text-to-speech plugin with support for advanced <a href="https://docs.aws.amazon.com/polly/latest/dg/voicelist.html">Amazon Polly</a> voices, multiple language recognition, etc!</p></br><details><summary><strong>Click To List Features</strong></summary><ul><li>Choose voices from a list of over 50 voices by Amazon Polly</li><li>Choose a default TTS voice</li><li>Set maximum character limits for TTS</li><li>Stream or Download TTS voice clips</li></ul></summary> |

  ### Easy Expansion With Custom Plugins
  - Easily expand the features of your bot by building custom plugins with the extensive and detailed API provided by JJMumbleBot.  
  - <a href="https://duckboss.github.io/JJMumbleBot/wiki/general/plugins.html">Click here to check the Wiki Guide!</a></b>

<details>
  <summary><strong>Additional Features</strong></summary>
  <ul>

  ### Custom GUI System  
  - <b>Pseudo-GUI System [PGUI]</b> - A pseudo graphical user interface built with html tags.<br/>
  -  <a href="">Pseudo-GUI API</a>
      
  </ul>
</details>

<details>
  <summary><strong>Screenshots 📷</strong></summary>
  <ul>

  ## Screenshots 📷
  
  <h3> Audio Interface System (youtube plugin, sound board plugin, etc) </h3>
  <img width=700 style="border-radius:3%" src="https://user-images.githubusercontent.com/20238115/88094381-75fcf600-cb61-11ea-8113-495db67a415d.png" alt="Channel Chat Image"/>
  
  <h3> Web Interface - Commands Page </h3>
  <img width=700 style="border-radius:3%" src="https://user-images.githubusercontent.com/20238115/106856286-3bd1ec80-668c-11eb-88dd-290e7e1dc027.png" alt="Commands Tab Image"/>
  
  <h3> Web Interface - Audio Page </h3>
  <img width=700 style="border-radius:3%" src="https://user-images.githubusercontent.com/20238115/106061227-1f014c00-60c3-11eb-9540-dd8a9222438d.png" alt="Audio Tab Image"/>
  
  <h3> Web Interface - Debug Page </h3>
  <img width=700 style="border-radius:3%" src="https://user-images.githubusercontent.com/20238115/106063400-1e1de980-60c6-11eb-8ab0-c52b1f097186.png" alt="Debug Tab Image"/>
  </ul>
</details>

<details>
  <summary><strong>Installation And Setup 🏃</strong></summary>
  <ul>

  ### Installation And Setup 🏃
  Please refer to the <b><a href="https://duckboss.github.io/JJMumbleBot/wiki/requirements.html">Requirements Wiki Page</a></b> for a full list of requirements, and instructions for installation.
  Additionally, the <b><a href="https://duckboss.github.io/JJMumbleBot/wiki/quick_start.html">Quick Start Guide</a></b> is also helpful for setting up the bot.

  ### Docker Setup 🏃
  Please check the <b><a href="https://duckboss.github.io/JJMumbleBot/wiki/general/docker.html">Docker Setup Wiki Page</a></b> for more information.
  </ul>
</details>

<details>
  <summary><strong>Documentation 📝</strong></summary>
  
  <ul>

  ### Documentation 📝
  <b><a href="https://duckboss.github.io/JJMumbleBot/wiki/new/whats_new.html">JJMumbleBot Documentation Wiki</a></b> <br>
  <b><a href="https://duckboss.github.io/JJMumbleBot/wiki/faq.html">F.A.Q - Solve common issues easily</a></b> <br>
  <b><a href="https://duckboss.github.io/JJMumbleBot/wiki/requirements.html">Requirements and Dependencies</a></b> <br>
  <b><a href="https://duckboss.github.io/JJMumbleBot/wiki/quick_start.html">Quick Start Guide</a></b> <br>
  </ul>

</details>

### Got any questions or concerns? Please post an issue report 👋
