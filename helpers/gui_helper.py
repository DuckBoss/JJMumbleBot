class GUIHelper:

    @staticmethod
    def font_mod(text, params=None):
        if params is None:
            params = []
        txt = f'<font '
        for i, item in enumerate(params):
            txt += f'{item} '
        txt += f'>{text}</font>'
        return txt

    @staticmethod
    def color(color):
        return f'color="{color}"'

    @staticmethod
    def face(font):
        return f'face="{font}"'

    @staticmethod
    def bold(text):
        return f'<b>{text}</b>'

    @staticmethod
    def content(text, tt="data", tc='white', tf='Calibri', ta="center"):
        txt_color = GUIHelper.color(tc)
        txt_face = GUIHelper.face(tf)
        if tt == 'data':
            content = f'<td align={ta}>{GUIHelper.font_mod(text, params=[txt_color, txt_face])}</td>'
            return content
        elif tt == 'header':
            content = f'<th align={ta}>{GUIHelper.font_mod(text, params=[txt_color, txt_face])}</th>'
            return content
        return None


