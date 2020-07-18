from threading import Thread


class Callbacks(dict):
    def __init__(self):
        super().__init__()
        '''
        self.update({
            'on_client_connect': None,
            'on_client_disconnect': None,
            'on_server_start': None,
        })
        '''

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
            self[callback]
        except KeyError:
            return None

    def callback(self, callback, *params):
        if self[callback]:
            thr = Thread(target=self[callback], args=params)
            thr.start()


class CommandCallbacks(dict):
    def __init__(self):
        super().__init__()

    def register_command(self, command, callback_name):
        self[command] = callback_name

    def remove_command(self, command):
        try:
            del self[command]
            return True
        except KeyError:
            return False

    def get_command(self, get_command):
        try:
            self[get_command]
        except KeyError:
            return None