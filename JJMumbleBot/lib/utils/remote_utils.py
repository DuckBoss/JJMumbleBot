from mumble.messages import Cmd as PyMessages
from mumble.constants import CMD


class RemoteTextMessage(PyMessages):
    def __init__(self, session, channel_id, message, actor):
        PyMessages.__init__(self)

        self.cmd = CMD.TEXT_MESSAGE
        self.actor = actor
        self.message = message
        self.parameters = {
            "session": session,
            "channel_id": channel_id,
            "message": message,
            "actor": actor,
        }
