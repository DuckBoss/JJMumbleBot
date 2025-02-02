## JJMumbleBot v5.3.0 - New features and fixes

<b>This project is no longer under active development, and the bot is being reworked in the following rework project: [Mumimo](https://github.com/DuckBoss/Mumimo)</b>
However I wanted to release a patch for existing users while they wait for the rework project to be ready for an initial release. This patch mostly aims to add small features and fix some existing issues that prevented the bot from working. This patch includes dependency updates and contains some breaking changes as a result.
Most pre-existing issues and new features going forward will be addressed in the rework project: [Mumimo](https://github.com/DuckBoss/Mumimo).

### New Features, Changes and Fixes
- <b>Media Plugin</b>:
    - Added support for streaming audio from radio stations.
    Simply use the `!radiolink <link>` command to start streaming from compatible radio stations.
    Radio streaming isn't supported for all radio stations and it requires a direct link to the icecast stream.
    Some examples of working radio station links are provided in the plugin's metadata file.
        - You can use existing audio commands with the radio streaming feature such as: `!stop`/`!pause`/`!resume`/`!playing`
    - Fixed audio-related stuttering and playback issues with the media plugin.
    - Fixed audio skipping at the end of the track when multiple tracks are in the queue.
    - Fixed parsing errors when playing youtube links and using the youtube search feature.
    - Increased the default maximum youtube video length to 14400 seconds. This can be changed in the `metadata.ini` file for the media plugin of course.
    - Renamed alias for the `!ytplaylist` command from `!ytlist` to `!ytplist`
    - Updated plugin version to `v5.3.0`
- <b>Sound Board Plugin</b>:
    - Adjusted logic for the `!sbrandom...` related commands to choose a different audio clip if it picks the same audio clip as the last time it was run. This change is to mitigate cases when it chooses the same audio clip back to back, making it feel less random.
    - Updated plugin version to `v5.3.0`
- <b>Audio API + Audio Commands Plugin</b>:
    - Split the audio ducking delay option into two separate delay options for finer control
    over the audio ducking feature:
        - Use `!duckstartdelay <seconds>` to specify how long the bot should wait before ducking the audio volume when it detects user voice activity.
        - Use `!duckenddelay <seconds>` to specify how long the bot should wait before restoring the ducked volume back to the original value when it detects no user voice activity.
        - Removed `!duckdelay` command and replaced it with  `!duckstartdelay` and `!duckenddelay`.
        - Updated command line arguments and config options to match the above changes.
    - Updated plugin version to `v5.3.0`
- <b>Image Plugin</b>:
    - Fixed an issue where image thumbnails could not be generated due to an outdated API.
- <b>Server Tools Plugin</b>:
    - Added missing default user connection sound file: `default_user_sound.wav`
    - Improved error-handling and error log details.
    - Added utility methods to find audio clips from the plugin media directory and integrate better with the sound board plugin.
    
- <b>Misc Changes</b>:
    - General formatting fixes and test cases updates.
    - Improved and fixed documentation in several plugins.
    - Updated plugin templating to improve plugin creation experience.
    - Updated pymumble and pymumble callback references to use updated API.

### Minimum Requirements Updates
 - This project now requires a minimum of Python 3.9+ (previously 3.7+) to improve compatibility with the 'yt-dlp' dependency and newer VLC versions which is heavily used for audio-related plugins.

### Dependency Updates
 - The project has been updated to use 'yt-dlp' instead of 'youtube-dl' since the original project is no longer in development. This new library works identically and is actively maintained.
 - I've updated the pymumble dependency to use a [stable fork that I've created](https://github.com/DuckBoss/pymumble) of [another fork by oopsbagel](https://github.com/oopsbagel/pymumble) which aims to improve and modernize pymumble since the original project is no longer in active development. I've decided to fork it into my own repository so I can verify patches and ensure stability for usage in this bot.

### Known Issues
 - <b>Server Tools Plugin</b>: The feature to play a 'connection sound' when a user connects to the server is
 currently broken. I highly suggest not using this feature. I don't plan on
 fixing it in this project and I will be addressing it in the larger rework project 'Mumimo'.
 If you still decide to use it and the audio queue freezes, simply use `!stop` to flush the audio queue.
