from pymumble_py3.messages import Cmd as PyMessages
from pymumble_py3.constants import *


class RemoteTextMessage(PyMessages):
    def __init__(self, session, channel_id, message, actor):
        PyMessages.__init__(self)

        self.cmd = PYMUMBLE_CMD_TEXTMESSAGE
        self.actor = actor
        self.message = message
        self.parameters = {"session": session,
                           "channel_id": channel_id,
                           "message": message,
                           "actor": actor}
