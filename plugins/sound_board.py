from templates.plugin_template import PluginBase
from helpers.global_access import GlobalMods as GM
import utils
import privileges as pv
import subprocess as sp
import audioop
import time
import os


class Plugin(PluginBase):

    help_data = "<br><b><font color='red'>#####</font> Sound_Board Plugin Help <font color='red'>#####</font></b><br> \
                    All commands can be run by typing it in the channel or privately messaging JJMumbleBot.<br>\
                    <b>!sb 'file_name'</b>: The file must be in wav format.<br>\
                    <b>!sbv '0..1'</b>: Sets the sound board audio volume.<br>\
                    <b>!sbreplay/!sbr</b>: Replays the last played sound board track.<br>\
                    <b>!sblist</b>: Displays all the available sound board tracks in private messages.<br>\
                    <b>!sblist_echo</b> Displays all the available sound board tracks in the channel chat.<br>\
                    <b>!sbstop/!sbs</b>: Stops the currently playing sound board track."
    plugin_version = "1.5.0"
    
    exit_flag = False
    current_song = None
    audio_thread = None
    #default volume
    volume = 0.5

    config = None
    youtube_plugin = None

    def __init__(self):
        print("Sound_Board Plugin Initialized...")    
        super().__init__()
        self.volume = float(GM.cfg['Plugin_Settings']['SoundBoard_DefaultVolume'])

    def set_youtube_plugin(self, yt_plugin):
        self.youtube_plugin = yt_plugin

    def process_command(self, mumble, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        all_messages = message[1:].split()
        command = message_parse[0]
        if command == "sbstop" or command == "sbs":
            if pv.privileges_check(mumble.users[text.actor]) == pv.Privileges.BLACKLIST.value:
                print("User [%s] must not be blacklisted to use this command." % (mumble.users[text.actor]['name']))
                return
            if self.audio_thread is not None:
                self.stop_audio()
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "Stopping sound board audio thread...")
                return
            return

        elif command == "sblist":
            if pv.privileges_check(mumble.users[text.actor]) == pv.Privileges.BLACKLIST.value:
                print("User [%s] must not be blacklisted to use this command." % (mumble.users[text.actor]['name']))
                return
            file_counter = 0
            internal_list = []

            for file_item in os.listdir(utils.get_permanent_media_dir()+"sound_board/"):
                if file_item.endswith(".wav"):
                    internal_list.append("<br><font color='cyan'>[%d]:</font> <font color='yellow'>%s</font>" % (file_counter, file_item))
                    file_counter += 1

            cur_text = "<br><font color='red'>Local Sound Board Files</font>"
            for i, item in enumerate(internal_list):
                cur_text += item
                if i % 50 == 0 and i != 0:
                    utils.msg(mumble, mumble.users[text.actor]['name'],
                       "%s" % cur_text)
                    cur_text = ""
            utils.msg(mumble, mumble.users[text.actor]['name'],
                       "%s" % cur_text)
            return

        elif command == "sblist_echo":
            if pv.privileges_check(mumble.users[text.actor]) == pv.Privileges.BLACKLIST.value:
                print("User [%s] must not be blacklisted to use this command." % (mumble.users[text.actor]['name']))
                return
            file_counter = 0
            internal_list = []

            for file_item in os.listdir(utils.get_permanent_media_dir()+"sound_board/"):
                if file_item.endswith(".wav"):
                    internal_list.append("<br><font color='cyan'>[%d]:</font> <font color='yellow'>%s</font>" % (file_counter, file_item))
                    file_counter += 1

            cur_text = "<br><font color='red'>Local Sound Board Files</font>"
            for i, item in enumerate(internal_list):
                cur_text += item
                if i % 50 == 0 and i != 0:
                    utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                               '%s' % cur_text)
                    cur_text = ""
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       '%s' % cur_text)
            return

        elif command == "sbreplay" or command == "sbr":
            if pv.privileges_check(mumble.users[text.actor]) == pv.Privileges.BLACKLIST.value:
                print("User [%s] must not be blacklisted to use this command." % (mumble.users[text.actor]['name']))
                return
            if self.audio_thread is not None:
                if self.current_song is not None:
                    self.youtube_plugin.clear_audio_plugin()

                    uri = "file:///%s/sound_board/%s.wav" % (utils.get_permanent_media_dir(), self.current_song)
                    command = utils.get_vlc_dir()
                    self.clear_audio_thread()
                    time.sleep(0.3)

                    mumble.sound_output.clear_buffer()
                    self.audio_thread = sp.Popen([command, uri] + ['-I', 'dummy', '--no-repeat', '--sout',
                                                                   '#transcode{acodec=s16le, channels=2, samplerate=24000, ab=128, threads=8}:std{access=file, mux=wav, dst=-}'],
                                                 stdout=sp.PIPE, bufsize=4096)

                    utils.unmute(mumble)

                    while not self.exit_flag and mumble.isAlive():
                        while mumble.sound_output.get_buffer_size() > 0.5 and not self.exit_flag:
                            time.sleep(0.01)
                        if self.audio_thread:
                            raw_music = self.audio_thread.stdout.read(4096)
                            if raw_music and self.audio_thread:  # raw_music and
                                mumble.sound_output.add_sound(audioop.mul(raw_music, 2, self.volume))
                            else:
                                time.sleep(0.1)
                        else:
                            time.sleep(0.1)
                    while mumble.sound_output.get_buffer_size() > 0:
                        time.sleep(0.01)
            else:
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "There is no sound board track available to replay.")
                return
            return

        elif command == "sbv":
            if pv.privileges_check(mumble.users[text.actor]) == pv.Privileges.BLACKLIST.value:
                print("User [%s] must not be blacklisted to use this command." % (mumble.users[text.actor]['name']))
                return
            try:
                vol = float(message[1:].split(' ', 1)[1])
            except IndexError:
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "Current sound board volume: %s" % self.volume)
                return
            if vol > 1:
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "Invalid sound_board volume Input: [0-1]")
                return
            if vol < 0:
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "Invalid sound_board volume Input: [0-1]")
                return
            self.volume = vol
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       "Set sound_board volume to %s" % self.volume)
            return

        elif command == "sb":
            if pv.privileges_check(mumble.users[text.actor]) == pv.Privileges.BLACKLIST.value:
                print("User [%s] must not be blacklisted to use this command." % (mumble.users[text.actor]['name']))
                return
            parameter = message_parse[1]

            if self.youtube_plugin.clear_audio_plugin() is False:
                return

            self.current_song = "%s" % parameter
            uri = "file:///%s/sound_board/%s.wav" % (utils.get_permanent_media_dir(), self.current_song)
            command = utils.get_vlc_dir()
            self.clear_audio_thread()
            time.sleep(0.3)
            mumble.sound_output.clear_buffer()
            self.audio_thread = sp.Popen([command, uri] + ['-I', 'dummy', '--no-repeat', '--sout',
                                                               '#transcode{acodec=s16le, channels=2, samplerate=24000, ab=128, threads=8}:std{access=file, mux=wav, dst=-}'], stdout=sp.PIPE, bufsize=4096)

            utils.unmute(mumble)

            while not self.exit_flag and mumble.isAlive():
                while mumble.sound_output.get_buffer_size() > 0.5 and not self.exit_flag:
                    time.sleep(0.01)
                if self.audio_thread:
                    raw_music = self.audio_thread.stdout.read(4096)
                    if raw_music and self.audio_thread:  # raw_music and
                        mumble.sound_output.add_sound(audioop.mul(raw_music, 2, self.volume))
                    else:
                        time.sleep(0.1)
                else:
                    time.sleep(0.1)
            while mumble.sound_output.get_buffer_size() > 0:
                time.sleep(0.01)
            return

    def clear_audio_thread(self):
        if self.audio_thread is not None:
            print("Clearing sound_board audio thread...")
            self.audio_thread.terminate()
            self.audio_thread.kill()
            self.audio_thread = None
            return True
        return False

    def stop_audio(self):
        if self.audio_thread is not None:
            print("Stopping sound_board audio thread...")
            self.audio_thread.terminate()
            self.audio_thread.kill()
            self.audio_thread = None
            self.current_song = None
            return True
        return False

    def plugin_test(self):
        print("Sound_Board Plugin self-test callback.")

    def quit(self):
        self.clear_audio_thread()
        self.stop_audio()
        self.exit_flag = True
        print("Exiting Sound_Board Plugin...")

    def help(self):
        return self.help_data

    def get_plugin_version(self):
        return self.plugin_version
