from JJMumbleBot.lib.helpers.pgui_helper import PGUIHelper
from JJMumbleBot.lib.utils.print_utils import dprint
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.utils import runtime_utils
from JJMumbleBot.settings import global_settings as GS
from JJMumbleBot.lib.helpers import image_helper as IH


class PseudoGUI:
    content = None
    box_open = False

    def __init__(self):
        dprint("Pseudo-GUI initialized.")

    def quick_gui(self, content, text_type="data", text_color=None, text_font='Calibri', text_align="center", bgcolor=None, border=None, box_align=None, row_align="center", cellpadding="5", cellspacing="5", channel=None, user=None, ignore_whisper=False):
        if self.box_open:
            return False
        if channel is None:
            channel = runtime_utils.get_my_channel()
        if bgcolor is None:
            bgcolor = GS.cfg[C_PGUI_SETTINGS][P_CANVAS_BG_COL]
        if box_align is None:
            box_align = GS.cfg[C_PGUI_SETTINGS][P_CANVAS_ALGN]
        if border is None:
            border = GS.cfg[C_PGUI_SETTINGS][P_CANVAS_BORD]
        if text_color is None:
            text_color = GS.cfg[C_PGUI_SETTINGS][P_CANVAS_TXT_COL]

        self.open_box(bgcolor=bgcolor, border=border, align=box_align, cellspacing=cellspacing, cellpadding=cellpadding)
        content = self.make_content(content, text_type=text_type, text_color=text_color, text_font=text_font, text_align=text_align)
        self.append_row(content, align=row_align)
        self.close_box()
        self.display_box(channel=channel, user=user, ignore_whisper=ignore_whisper)
        self.clear_display()

    def quick_gui_img(self, directory, img_data, format=False, caption=None, bgcolor="black", channel=None, user=None, img_size=65536, cellspacing="5"):
        if self.box_open:
            return False
        if channel is None:
            channel = runtime_utils.get_my_channel()

        self.open_box(align='left', bgcolor=bgcolor, cellspacing=cellspacing)

        if format:
            formatted_string = IH.format_image(f"{img_data}", "jpg", directory, size_goal=img_size)
            content = self.make_content(formatted_string, image=True, text_align='center')
            if content is not None:
                self.append_row(content)
        else:
            content = self.make_content(img_data, image=True, text_align='center')
            if content is not None:
                self.append_row(content)

        if caption is not None:
            caption = self.make_content(caption, text_type="header", text_font='Calibri', image=False)
            self.append_row(caption)

        self.close_box()

        self.display_box(channel=channel, user=user)
        self.clear_display()

    def open_box(self, bgcolor=None, border=None, align=None, cellspacing="5", cellpadding="5"):
        if self.box_open:
            return False
        if bgcolor is None:
            bgcolor = GS.cfg[C_PGUI_SETTINGS][P_CANVAS_BG_COL]
        if align is None:
            align = GS.cfg[C_PGUI_SETTINGS][P_CANVAS_ALGN]
        if border is None:
            border = GS.cfg[C_PGUI_SETTINGS][P_CANVAS_BORD]

        self.content = f'<table bgcolor="{bgcolor}" border="{border}" align="{align}" cellspacing="{cellspacing}" cellpadding="{cellpadding}">'
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

    def make_content(self, text, text_type="data", text_color=None, text_font='Calibri', text_align="center", image=False):
        if not self.box_open:
            return None
        if image:
            return PGUIHelper.img_content(text)
        if text_color is None:
            text_color = GS.cfg[C_PGUI_SETTINGS][P_CANVAS_TXT_COL]
        new_content = PGUIHelper.content(text, tt=text_type, tc=text_color, tf=text_font, ta=text_align)
        return new_content

    def display_box(self, channel, user=None, ignore_whisper=False):
        if self.content is None or self.box_open:
            return
        if user is not None:
            runtime_utils.msg(user, self.content)
            self.clear_display()
            return
        runtime_utils.echo(channel, self.content, ignore_whisper=ignore_whisper)
        self.clear_display()

    def clear_display(self):
        self.content = None




