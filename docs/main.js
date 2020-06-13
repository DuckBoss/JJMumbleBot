function get_connection_settings() {
  return `
[Connection Settings]
; Enter your server ip here, don't use quotations.
ServerIP = ${document.getElementById('server-ip').value}
; Enter the server password here to authenticate the bot. If your server has no password, leave it blank.
ServerPassword = ${document.getElementById('server-pass').value}
; Enter the server port number here so the bot can connect to the server.
ServerPort = ${document.getElementById('server-port').value}
; Enter your bot username here, If the bot is registered with a certificate, the name must match the name in the certificate.
UserID = ${document.getElementById('server-user').value}
; Enter the file path to your certificate. If your server doesn't require a certificate, leave this blank.
UserCertification = ${document.getElementById('server-cert').value}
; Specify the default channel the bot should join when it connects to the server.
DefaultChannel = ${document.getElementById('server-default-channel').value}
; Enter the bot owner's display name here. The bot must have at least 1 super user to be able to control all bot commands.
DefaultSuperUser = ${document.getElementById('server-superuser').value}
; The default comment associated with the bot that is shown to users when they view the bot's comment. This can be left blank.
DefaultComment = ${document.getElementById('server-comment').value}
`;
}

function get_media_directories() {
  return `
[Media Directories]
; Temporary media directory to store youtube thumbnails and other images content. This directory is cleared when the bot exits
TemporaryMediaDirectory = ${document.getElementById('media-temp-path').value}
; Permanent media directory to store sound board clips, and other media that won't be deleted when the bot exits
PermanentMediaDirectory = ${document.getElementById('media-perm-path').value}
`;
}

function get_logging() {
  return `
[Logging]
; To enable logging for the bot, set this to true. Set it to false to disable.
EnableLogging = ${document.getElementById('logging-enable').value}
; This sets the maximum number of logs the bot can have at a time before it overwrites the oldest one.
MaxLogs = ${document.getElementById('logging-max-logs').value}
; This is the path to directory where logs are stored. All bot logs will be stored in this directory.
LogDirectory = ${document.getElementById('logging-path').value}
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
; Enable stereo output by setting this to True, or disable by setting it to False.
UseStereoOutput = ${document.getElementById('main-settings-stereo').value}
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
; Determines the default canvas alignment using html alignment tags
CanvasAlignment = ${document.getElementById('pgui-canvas-align').value}
; Determines the default canvas border size [Recommended: 0]
CanvasBorder = ${document.getElementById('pgui-canvas-border-size').value}
; Determines the default canvas text color
CanvasTextColor = ${document.getElementById('pgui-canvas-color').value}
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
        alert('Some required fields are empty!\nPlease make sure that all fields marked with a red outline are filled.');
        return false;
      }
  }

  var ini_out = `${get_connection_settings()}\n${get_media_directories()}\n${get_logging()}\n${get_plugin_settings()}\n${get_main_settings()}\n${get_pgui_settings()}`;
  console.log(ini_out.trim())
  download(ini_out.trim(), 'config.ini', 'text/plain')
}
