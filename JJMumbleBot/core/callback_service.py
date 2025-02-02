from JJMumbleBot.settings import global_settings
from mumble.callbacks import CALLBACK


class CallbackService:
    def __init__(self):
        pass

    @staticmethod
    def message_received(text, remote_cmd=False):
        global_settings.core_callbacks.callback(
            CALLBACK.TEXT_MESSAGE_RECEIVED, text, remote_cmd
        )

    @staticmethod
    def sound_received(user, audio_chunk):
        global_settings.core_callbacks.callback(
            CALLBACK.SOUND_RECEIVED, user, audio_chunk
        )

    @staticmethod
    def connected():
        global_settings.core_callbacks.callback(CALLBACK.CONNECTED)

    @staticmethod
    def disconnected():
        global_settings.core_callbacks.callback(CALLBACK.DISCONNECTED)

    @staticmethod
    def channel_created(channel):
        global_settings.core_callbacks.callback(CALLBACK.CHANNEL_CREATED, channel)

    @staticmethod
    def channel_updated(channel, modified_params):
        global_settings.core_callbacks.callback(
            CALLBACK.CHANNEL_UPDATED, channel, modified_params
        )

    @staticmethod
    def channel_removed(channel):
        global_settings.core_callbacks.callback(CALLBACK.CHANNEL_REMOVED, channel)

    @staticmethod
    def user_created(user):
        global_settings.core_callbacks.callback(CALLBACK.USER_CREATED, user)

    @staticmethod
    def user_updated(user, modified_params):
        global_settings.core_callbacks.callback(
            CALLBACK.USER_UPDATED, user, modified_params
        )

    @staticmethod
    def user_removed(user, message):
        global_settings.core_callbacks.callback(CALLBACK.USER_REMOVED, user, message)

    @staticmethod
    def permission_denied(data):
        global_settings.core_callbacks.callback(CALLBACK.PERMISSION_DENIED, data)
