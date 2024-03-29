function get_connection_settings() {
  return `
[Connection Settings]
; Enter your bot username here, If the bot is registered with a certificate, the name must match the name in the certificate.
UserID = ${document.getElementById('server-user').value}
; Enter the file path to your certificate. If your server doesn't require a certificate, leave this blank.
UserCertification = ${document.getElementById('server-cert').value}
; Auto-Reconnect to the server if connection is lost.
AutoReconnect = ${document.getElementById('server-reconnect').value}
; Specify the default channel the bot should join when it connects to the server.
DefaultChannel = ${document.getElementById('server-default-channel').value}
; Enter the bot owner's display name here. The bot must have at least 1 super user to be able to control all bot commands.
DefaultSuperUser = ${document.getElementById('server-superuser').value}
; Allows the bot to attempt to self-register to the server.
SelfRegister = ${document.getElementById('main-settings-self-register').value}
; The default comment associated with the bot that is shown to users when they view the bot's comment. This can be left blank.
DefaultComment = ${document.getElementById('server-comment').value}
`;
}

function get_media_settings() {
  return `
[Media Settings]
; FFmpeg location
FfmpegPath = ${document.getElementById('media-ffmpeg-path').value}
; VLC location
VlcPath = ${document.getElementById('media-vlc-path').value}
; Use Stereo Audio
UseStereoAudio = ${document.getElementById('media-stereo-enable').value}
; Enable/Disable Audio Library Console Messages
AudioLibraryRunQuiet = ${document.getElementById('media-quiet-enable').value}
; The default volume when the bot starts (default=0.3)
DefaultVolume = ${document.getElementById('media-default-volume').value}
; Enable Audio Ducking (off by default, use !duckaudio to toggle on and off)
UseAudioDuck = ${document.getElementById('media-duck-audio-enable').value}
; The default audio ducking volume (How low the volume will drop down when ducking) (default=0.05)
DuckingVolume: ${document.getElementById('media-ducking-volume').value}
; The default threshold before audio is ducked (default=2500.0)
DuckingThreshold: ${document.getElementById('media-ducking-threshold').value}
; The default delay before the audio ducking reacts to user voices (default=1.0)
DuckingDelay: ${document.getElementById('media-ducking-delay').value}
; The default maximum queue length for the audio interface (default=50)
MaxQueueLength = ${document.getElementById('media-max-queue-length').value}
; Optional Proxy URL - If you want to use a proxy server to use the youtube-dl library, fill this out.
YoutubeDLProxyURL = ${document.getElementById('media-proxy-url').value}
; Optionally use a cookies.txt file for the youtube-dl library (useful to deal with rate limits).
YoutubeDLCookieFile = ${document.getElementById('media-cookies-path').value}
; Temporary media directory to store youtube thumbnails and other images content. This directory is cleared when the bot exits
TemporaryMediaDirectory = ${document.getElementById('media-temp-path').value}
; Permanent media directory to store sound board clips, and other media that won't be deleted when the bot exits
PermanentMediaDirectory = ${document.getElementById('media-perm-path').value}
`;
}

function get_logging() {
  return `
[Logging]
; To enable logging for the bot, check the box. Uncheck it to disable.
EnableLogging = ${document.getElementById('logging-enable').value}
; This sets the maximum number of logs the bot can have at a time before it overwrites the oldest one.
MaxLogs = ${document.getElementById('logging-max-logs').value}
; Maximum size per log (in Bytes)
MaxLogSize = ${document.getElementById('logging-max-log-size').value}
; Enable/Disable channel message logging (Enabling it will hide message logs to: Message Received: [User -> #####])
HideMessageLogging = ${document.getElementById('logging-hide-message-enable').value}
; This is the path to directory where logs are stored. All bot logs will be stored in this directory.
LogDirectory = ${document.getElementById('logging-path').value}
; Enable/Disable Stack Trace Logging. This will create large log files and log the stack trace of each logging event.
LogStackTrace = ${document.getElementById('logging-stack-trace').value}
`;
}

function get_plugin_settings() {
  return `
[Plugin Settings]
; Disables plugins that are included in this list for regular operation. You can leave the list empty.
DisabledPlugins = [${document.getElementById('plugins-disabled').value}]
; This sets the maximum number of logs the bot can have at a time before it overwrites the oldest one.
SafeModePlugins = [${document.getElementById('plugins-safe').value}]
; This is the path to directory where logs are stored. All bot logs will be stored in this directory.
AllowedRootChannelsForTempChannels = [${document.getElementById('allowed-root').value}]
`;
}

function get_main_settings() {
  return `
[Main Settings]
; EnableDatabaseIntegrityCheck: Enable or disable version/plugin integrity checking for the database.
; Disabling this may cause database conflicts after code updates, plugin updates, or plugin addition/removal!
EnableDatabaseIntegrityCheck = ${document.getElementById('main-settings-db-integrity').value}
; Enable or disable automatic internal database backups
EnableDatabaseBackup = ${document.getElementById('main-settings-db-backups').value}
; The execution tick rate of commands in the command queue [Must be an integer/float].
CommandTickRate  = ${document.getElementById('main-settings-cmd-tick-rate').value}
; Maximum commands in a multi-command input (this includes multi-commands in aliases) [Must be an integer] This determines the number of commands that can be inputted in a single line
MultiCommandLimit = ${document.getElementById('main-settings-cmd-limit').value}
; Maximum commands per queue (this includes commands in aliases) [Must be an integer] This determines the maximum number of commands that the bot can process in it's queue.
CommandQueueLimit = ${document.getElementById('main-settings-cmd-queue-limit').value}
; The command token to identify commands in the chat [Must be a single character]
CommandToken = ${document.getElementById('main-settings-cmd-token').value}
; The number of commands to store in the command history tracker [Must be an integer]
CommandHistoryLimit = ${document.getElementById('main-settings-cmd-hist-limit').value}
`;
}

function get_pgui_settings() {
  return `
[PGUI Settings]
; Determines the default background color of the UI canvas.
; Refer to the following for more information on the limitations:
; https://doc.qt.io/qt-5/richtext-html-subset.html
; https://doc.qt.io/qt-5/qcolor.html#setNamedColor
CanvasBGColor = ${document.getElementById('pgui-canvas-bg-color').value}
; Determines the default Canvas Image BG Color
CanvasImageBGColor = ${document.getElementById('pgui-canvas-img-bg-color').value}
; Determines the default canvas alignment using html alignment tags
CanvasAlignment = ${document.getElementById('pgui-canvas-align').value}
; Determines the default canvas border size [Recommended: 0]
CanvasBorder = ${document.getElementById('pgui-canvas-border-size').value}
; Determines the default canvas text color
CanvasTextColor = ${document.getElementById('pgui-canvas-color').value}
; Determines the default canvas text font
DefaultFont = ${document.getElementById('pgui-canvas-default-font').value}
; Determines the default header text color
HeaderTextColor = ${document.getElementById('pgui-canvas-header-color').value}
; Determines the default index text color
IndexTextColor = ${document.getElementById('pgui-canvas-index-color').value}
; Determines the default sub-header text color
SubHeaderTextColor = ${document.getElementById('pgui-canvas-subheader-color').value}
`;
}

// Function to download data to a file
function download(data, filename, type) {
    var file = new Blob([data], {type: type});
    if (window.navigator.msSaveOrOpenBlob) // IE10+
        window.navigator.msSaveOrOpenBlob(file, filename);
    else { // Others
        var a = document.createElement("a"),
                url = URL.createObjectURL(file);
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        setTimeout(function() {
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        }, 0);
    }
}

function get_all_data() {
  form = document.getElementsByTagName('input')
  for(var i=0; i < form.length; i++) {
      if(form[i].value === '' && form[i].hasAttribute('required')) {
        $('.alert').show();
        return false;
      }
  }

  var ini_out = `${get_connection_settings()}\n${get_media_settings()}\n${get_logging()}\n${get_plugin_settings()}\n${get_main_settings()}\n${get_pgui_settings()}`;
  console.log(ini_out.trim())
  download(ini_out.trim(), 'config.ini', 'text/plain')
}
