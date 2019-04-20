from helpers.gui_helper import GUIHelper
from helpers.global_access import debug_print, reg_print
from helpers.global_access import GlobalMods as GM
import utils
import helpers.image_helper as IH


class PseudoGUI:

    mumble = None
    content = None
    box_open = False

    def __init__(self, mumble):
        self.mumble = mumble
        debug_print("Pseudo-GUI initialized.")

    def quick_gui(self, content, text_type="data", text_color=None, text_font='Calibri', text_align="center", bgcolor=None, border=None, box_align=None, row_align="center", cellpadding="5", cellspacing="5", channel=None, user=None):
        if self.box_open:
            return False
        if channel is None:
            channel = utils.get_my_channel(self.mumble)
        if bgcolor is None:
            bgcolor = GM.cfg['PGUI_Settings']['CanvasBGColor']
        if box_align is None:
            box_align = GM.cfg['PGUI_Settings']['CanvasAlignment']
        if border is None:
            border = GM.cfg['PGUI_Settings']['CanvasBorder']
        if text_color is None:
            text_color = GM.cfg['PGUI_Settings']['CanvasTextColor']

        self.open_box(bgcolor=bgcolor, border=border, align=box_align, cellspacing=cellspacing, cellpadding=cellpadding)
        content = self.make_content(content, text_type=text_type, text_color=text_color, text_font=text_font, text_align=text_align)
        self.append_row(content, align=row_align)
        self.close_box()
        self.display_box(channel=channel, user=user)
        self.clear_display()

    def quick_gui_img(self, directory, img_data, format=False, caption=None, bgcolor="black", channel=None, user=None, img_size=65536, cellspacing="5"):
        if self.box_open:
            return False
        if channel is None:
            channel = utils.get_my_channel(self.mumble)

        self.open_box(align='left', bgcolor=bgcolor, cellspacing=cellspacing)

        if format:
            formatted_string = IH.format_image(f"{img_data}", "jpg", directory, size_goal=img_size)
            content = self.make_content(formatted_string, image=True, text_align='center')
            self.append_row(content)
        else:
            content = self.make_content(img_data, image=True, text_align='center')
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
            bgcolor = GM.cfg['PGUI_Settings']['CanvasBGColor']
        if align is None:
            align = GM.cfg['PGUI_Settings']['CanvasAlignment']
        if border is None:
            border = GM.cfg['PGUI_Settings']['CanvasBorder']

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
            return GUIHelper.img_content(text)
        if text_color is None:
            text_color = GM.cfg['PGUI_Settings']['CanvasTextColor']
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




