from JJMumbleBot.settings import global_settings
from pymumble_py3.constants import PYMUMBLE_CLBK_USERCREATED, PYMUMBLE_CLBK_CONNECTED, PYMUMBLE_CLBK_SOUNDRECEIVED, \
    PYMUMBLE_CLBK_TEXTMESSAGERECEIVED, PYMUMBLE_CLBK_DISCONNECTED, PYMUMBLE_CLBK_CHANNELUPDATED, \
    PYMUMBLE_CLBK_CHANNELREMOVED, PYMUMBLE_CLBK_CHANNELCREATED, PYMUMBLE_CLBK_USERREMOVED, PYMUMBLE_CLBK_USERUPDATED


class CallbackService:
    def __init__(self):
        pass

    @staticmethod
    def message_received(text, remote_cmd=False):
        global_settings.core_callbacks.callback(PYMUMBLE_CLBK_TEXTMESSAGERECEIVED, text, remote_cmd)

    @staticmethod
    def sound_received(user, audio_chunk):
        global_settings.core_callbacks.callback(PYMUMBLE_CLBK_SOUNDRECEIVED, user, audio_chunk)

    @staticmethod
    def connected():
        global_settings.core_callbacks.callback(PYMUMBLE_CLBK_CONNECTED)

    @staticmethod
    def disconnected():
        global_settings.core_callbacks.callback(PYMUMBLE_CLBK_DISCONNECTED)

    @staticmethod
    def channel_created(channel):
        global_settings.core_callbacks.callback(PYMUMBLE_CLBK_CHANNELCREATED, channel)

    @staticmethod
    def channel_updated(channel, modified_params):
        global_settings.core_callbacks.callback(PYMUMBLE_CLBK_CHANNELUPDATED, channel, modified_params)

    @staticmethod
    def channel_removed(channel):
        global_settings.core_callbacks.callback(PYMUMBLE_CLBK_CHANNELREMOVED, channel)

    @staticmethod
    def user_created(user):
        global_settings.core_callbacks.callback(PYMUMBLE_CLBK_USERCREATED, user)

    @staticmethod
    def user_updated(user, modified_params):
        global_settings.core_callbacks.callback(PYMUMBLE_CLBK_USERUPDATED, user, modified_params)

    @staticmethod
    def user_removed(user, message):
        global_settings.core_callbacks.callback(PYMUMBLE_CLBK_USERREMOVED, user, message)
