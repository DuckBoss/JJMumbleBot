from JJMumbleBot.lib.utils.print_utils import dprint
from mumble.callbacks import CALLBACK


class Callbacks(dict):
    def __init__(self):
        super().__init__()

    def register_callback(self, callback, dest):
        self[callback] = dest

    def remove_callback(self, callback):
        try:
            del self[callback]
            return True
        except KeyError:
            return False

    def get_callback(self, callback):
        try:
            return self[callback]
        except KeyError:
            return None

    def callback(self, callback, *params):
        self[callback](params)
        # if self[callback]:
        #    thr = Thread(target=self[callback], args=params)
        #    thr.start()


class CoreCallbacks(Callbacks):
    def __init__(self):
        super().__init__()
        self.update(
            {
                CALLBACK.USER_CREATED: [],
                CALLBACK.TEXT_MESSAGE_RECEIVED: [],
                CALLBACK.SOUND_RECEIVED: [],
                CALLBACK.CONNECTED: [],
                CALLBACK.CHANNEL_CREATED: [],
                CALLBACK.CHANNEL_REMOVED: [],
                CALLBACK.CHANNEL_UPDATED: [],
                CALLBACK.USER_REMOVED: [],
                CALLBACK.USER_UPDATED: [],
                CALLBACK.DISCONNECTED: [],
                CALLBACK.PERMISSION_DENIED: [],
            }
        )

    def register_callback(self, callback, dest: list):
        self[callback] = dest

    def append_to_callback(self, callback, method):
        self[callback].append(method)

    def callback(self, callback, *params):
        for clbk in self[callback]:
            try:
                clbk(params)
            except Exception as e:
                dprint(e)


class CommandCallbacks(dict):
    def __init__(self):
        super().__init__()

    def register_command(self, command, plugin, callback_name):
        if command in self:
            return False
        self[command] = (plugin, callback_name)
        return True

    def remove_command(self, command):
        try:
            del self[command]
            return True
        except KeyError:
            return False

    def get_command(self, command):
        try:
            return self[command]
        except KeyError:
            return None
