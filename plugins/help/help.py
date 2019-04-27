from templates.plugin_template import PluginBase
from helpers.global_access import GlobalMods as GM
from helpers.global_access import debug_print, reg_print
from helpers.gui_helper import GUIHelper
import privileges as pv
import utils


class Plugin(PluginBase):
    help_data = "All commands can be run by typing it in the chat or privately messaging JJMumbleBot.<br>\
                <b>!help</b>: Displays this general help screen.<br>\
                <b>!bot_help</b>: Displays the bot_commands plugin help screen.<br>\
                <b>!youtube_help/!yt_help</b>: Displays the youtube plugin help screen.<br>\
                <b>!sound_board_help/!sb_help</b>: Displays the sound_board plugin help screen.<br>\
                <b>!images_help/!img_help</b>: Displays the images plugin help screen.<br>\
                <b>!randomizer_help</b>: Displays the randomizer plugin help screen.<br>"
    plugin_version = "2.0.0"
    priv_path = "help/help_privileges.csv"
    bot_plugins = {}

    def __init__(self, bot_plugins):
        debug_print("Help Plugin Initialized.")
        super().__init__()
        self.bot_plugins = bot_plugins

    def process_command(self, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        if command == "help":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            GM.gui.open_box()
            all_help_lines = [msg.strip() for msg in self.help_data.split('<br>')]
            content = GM.gui.make_content(f'<font color="red">#####</font> '
                                          f'{GUIHelper.bold(f"{utils.get_bot_name()} General Help Commands")} '
                                          f'<font color="red">#####</font>')
            GM.gui.append_row(content)
            content = GM.gui.make_content(f'Plugin Version: {self.get_plugin_version()}<br>', text_color='cyan')
            GM.gui.append_row(content)

            for i, item in enumerate(all_help_lines):
                content = GM.gui.make_content(f'{item}', 'header', text_color='yellow', text_align="left")
                GM.gui.append_row(content)
            GM.gui.close_box()
            GM.gui.display_box(channel=utils.get_my_channel())

            reg_print("Displayed general help screen in the channel.")
            GM.logger.info("Displayed general help screen in the channel.")
            return

        elif command == "bot_help":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            GM.gui.open_box()
            all_help_lines = [msg.strip() for msg in self.bot_plugins.get("bot_commands").help().split('<br>')]
            content = GM.gui.make_content(f'<font color="red">#####</font> '
                                          f'{GUIHelper.bold("Bot_Commands Plugin Help")} '
                                          f'<font color="red">#####</font>')
            GM.gui.append_row(content)
            content = GM.gui.make_content(f'Plugin Version: {self.bot_plugins.get("bot_commands").get_plugin_version()}<br>', text_color='cyan')
            GM.gui.append_row(content)

            for i, item in enumerate(all_help_lines):
                content = GM.gui.make_content(f'{item}', 'header', text_color='yellow', text_align="left")
                GM.gui.append_row(content)
            GM.gui.close_box()
            GM.gui.display_box(channel=utils.get_my_channel())

            reg_print("Displayed bot commands plugin help screen in the channel.")
            GM.logger.info("Displayed bot commands plugin help screen in the channel.")
            return

        elif command == "sound_board_help":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            GM.gui.open_box()
            all_help_lines = [msg.strip() for msg in self.bot_plugins.get("sound_board").help().split('<br>')]
            content = GM.gui.make_content(f'<font color="red">#####</font> '
                                          f'{GUIHelper.bold("Sound_Board Plugin Help")} '
                                          f'<font color="red">#####</font>')
            GM.gui.append_row(content)
            content = GM.gui.make_content(
                f'Plugin Version: {self.bot_plugins.get("sound_board").get_plugin_version()}<br>', text_color='cyan')
            GM.gui.append_row(content)

            for i, item in enumerate(all_help_lines):
                content = GM.gui.make_content(f'{item}', 'header', text_color='yellow', text_align="left")
                GM.gui.append_row(content)
            GM.gui.close_box()
            GM.gui.display_box(channel=utils.get_my_channel())

            reg_print("Displayed sound_board plugin help screen in the channel.")
            GM.logger.info("Displayed sound_board plugin help screen in the channel.")
            return

        elif command == "youtube_help":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            GM.gui.open_box()
            all_help_lines = [msg.strip() for msg in self.bot_plugins.get("youtube").help().split('<br>')]
            content = GM.gui.make_content(f'<font color="red">#####</font> '
                                          f'{GUIHelper.bold("Youtube Plugin Help")} '
                                          f'<font color="red">#####</font>')
            GM.gui.append_row(content)
            content = GM.gui.make_content(
                f'Plugin Version: {self.bot_plugins.get("youtube").get_plugin_version()}<br>', text_color='cyan')
            GM.gui.append_row(content)

            for i, item in enumerate(all_help_lines):
                content = GM.gui.make_content(f'{item}', 'header', text_color='yellow', text_align="left")
                GM.gui.append_row(content)
            GM.gui.close_box()
            GM.gui.display_box(channel=utils.get_my_channel())

            reg_print("Displayed youtube plugin help screen in the channel.")
            GM.logger.info("Displayed youtube plugin help screen in the channel.")
            return

        elif command == "images_help":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            GM.gui.open_box()
            all_help_lines = [msg.strip() for msg in self.bot_plugins.get("images").help().split('<br>')]
            content = GM.gui.make_content(f'<font color="red">#####</font> '
                                          f'{GUIHelper.bold("Images Plugin Help")} '
                                          f'<font color="red">#####</font>')
            GM.gui.append_row(content)
            content = GM.gui.make_content(
                f'Plugin Version: {self.bot_plugins.get("images").get_plugin_version()}<br>', text_color='cyan')
            GM.gui.append_row(content)

            for i, item in enumerate(all_help_lines):
                content = GM.gui.make_content(f'{item}', 'header', text_color='yellow', text_align="left")
                GM.gui.append_row(content)
            GM.gui.close_box()
            GM.gui.display_box(channel=utils.get_my_channel())

            reg_print("Displayed images plugin help screen in the channel.")
            GM.logger.info("Displayed images plugin help screen in the channel.")
            return

        elif command == "uptime_help":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            GM.gui.open_box()
            all_help_lines = [msg.strip() for msg in self.bot_plugins.get("uptime").help().split('<br>')]
            content = GM.gui.make_content(f'<font color="red">#####</font> '
                                          f'{GUIHelper.bold("Uptime Plugin Help")} '
                                          f'<font color="red">#####</font>')
            GM.gui.append_row(content)
            content = GM.gui.make_content(
                f'Plugin Version: {self.bot_plugins.get("uptime").get_plugin_version()}<br>', text_color='cyan')
            GM.gui.append_row(content)

            for i, item in enumerate(all_help_lines):
                content = GM.gui.make_content(f'{item}', 'header', text_color='yellow', text_align="left")
                GM.gui.append_row(content)
            GM.gui.close_box()
            GM.gui.display_box(channel=utils.get_my_channel())

            reg_print("Displayed uptime plugin help screen in the channel.")
            GM.logger.info("Displayed uptime plugin help screen in the channel.")
            return

        elif command == "randomizer_help":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            GM.gui.open_box()
            all_help_lines = [msg.strip() for msg in self.bot_plugins.get("randomizer").help().split('<br>')]
            content = GM.gui.make_content(f'<font color="red">#####</font> '
                                          f'{GUIHelper.bold("Randomizer Plugin Help")} '
                                          f'<font color="red">#####</font>')
            GM.gui.append_row(content)
            content = GM.gui.make_content(
                f'Plugin Version: {self.bot_plugins.get("randomizer").get_plugin_version()}<br>', text_color='cyan')
            GM.gui.append_row(content)

            for i, item in enumerate(all_help_lines):
                content = GM.gui.make_content(f'{item}', 'header', text_color='yellow', text_align="left")
                GM.gui.append_row(content)
            GM.gui.close_box()
            GM.gui.display_box(channel=utils.get_my_channel())

            reg_print("Displayed randomizer plugin help screen in the channel.")
            GM.logger.info("Displayed randomizer plugin help screen in the channel.")
            return

    def plugin_test(self):
        debug_print("Help Plugin self-test callback.")

    def quit(self):
        debug_print("Exiting Help Plugin")

    def help(self):
        return self.help_data

    def is_audio_plugin(self):
        return False

    def get_plugin_version(self):
        return self.plugin_version

    def get_priv_path(self):
        return self.priv_path
