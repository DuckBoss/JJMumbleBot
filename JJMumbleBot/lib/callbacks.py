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
        #if self[callback]:
        #    thr = Thread(target=self[callback], args=params)
        #    thr.start()


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
