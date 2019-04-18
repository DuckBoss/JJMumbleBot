from helpers.gui_helper import GUIHelper
from helpers.global_access import debug_print, reg_print
import utils


class PseudoGUI:

    mumble = None
    content = None
    box_open = False

    def __init__(self, mumble):
        self.mumble = mumble
        debug_print("Pseudo-GUI initialized.")

    def quick_gui(self, content, text_type="data", text_color='white', text_font='Calibri', text_align="center", bgcolor="black", border="0", box_align="center", row_align="center", cellspacing="5", channel=None, user=None):
        if self.box_open:
            return False
        if channel is None:
            channel = utils.get_my_channel(self.mumble)
        self.open_box(bgcolor=bgcolor, border=border, align=box_align, cellspacing=cellspacing)
        content = self.make_content(content, text_type=text_type, text_color=text_color, text_font=text_font, text_align=text_align)
        self.append_row(content, align=row_align)
        self.close_box()
        self.display_box(channel=channel, user=user)
        self.clear_display()

    def open_box(self, bgcolor="black", border="0", align="center", cellspacing="5"):
        if self.box_open:
            return False
        self.content = f'<table bgcolor="{bgcolor}" border="{border}" align="{align}" cellspacing="{cellspacing}">'
        self.box_open = True
        return True

    def close_box(self):
        if not self.box_open:
            return False
        self.content += '</table>'
        self.box_open = False
        return True

    def append_row(self, content, align="center"):
        if not self.box_open:
            return False
        self.content += f'<tr align="{align}">' + content + '</tr>'
        return True

    def append_content(self, content):
        if not self.box_open:
            return False
        self.content += content
        return True

    def make_content(self, text, text_type="data", text_color='white', text_font='Calibri', text_align="center"):
        if not self.box_open:
            return None
        new_content = GUIHelper.content(text, tt=text_type, tc=text_color, tf=text_font, ta=text_align)
        return new_content

    def display_box(self, channel, user=None):
        if self.content is None or self.box_open:
            return
        if user is not None:
            utils.msg(self.mumble, user, self.content)
            self.clear_display()
            return
        utils.echo(channel, self.content)
        self.clear_display()

    def clear_display(self):
        self.content = None

