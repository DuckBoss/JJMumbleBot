from JJMumbleBot.lib.utils import runtime_utils as rutils
from JJMumbleBot.plugins.core.web_server.utility.web_utils import ResponseModel, StdModel
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

router = InferringRouter()


@cbv(router)
class BotCommandsPluginAPI:
    #region CHANNELS
    @router.get("/api/admin/channels")
    async def channels_section(self):
        return ResponseModel(200, "success").toDict()

    @router.post("/api/admin/channels/leave")
    async def leave_channel(self):
        rutils.leave_channel()
        return ResponseModel(200, "success").toDict()

    @router.post("/api/admin/channels/make_temporary")
    async def make_temporary_channel(self, command: StdModel):
        if len(command.text) > 0:
            rutils.make_channel(rutils.get_my_channel(), command.text.strip(), temporary=True)
            return ResponseModel(200, "success").toDict()
        return ResponseModel(400, "error",
                             {"error_message": f"Please be sure to provide a valid temporary channel name!"})

    @router.post("/api/admin/channels/make_permanent")
    async def make_temporary_channel(self, command: StdModel):
        if len(command.text) > 0:
            rutils.make_channel(rutils.get_my_channel(), command.text.strip(), temporary=False)
            return ResponseModel(200, "success").toDict()
        return ResponseModel(400, "error",
                             {"error_message": f"Please be sure to provide a valid permanent channel name!"})

    @router.post("/api/admin/channels/move")
    async def move_to_channel(self, command: StdModel):
        if len(command.text) > 0:
            rutils.move_to_channel(command.text.strip())
            return ResponseModel(200, "success").toDict()
        return ResponseModel(400, "error",
                             {"error_message": f"Please be sure to provide a valid channel name that exists!"})

    @router.post("/api/admin/channels/remove")
    async def remove_channel(self, command: StdModel):
        if len(command.text) > 0:
            rutils.remove_channel(command.text.strip())
            return ResponseModel(200, "success").toDict()
        return ResponseModel(400, "error",
                             {"error_message": f"Please be sure to provide a valid channel name that exists!"})

    @router.post("/api/admin/channels/rename")
    async def rename_channel(self, command: StdModel):
        if len(command.text) > 0:
            split_data = command.text.strip().split(' ', 1)
            if len(split_data) == 2:
                rutils.rename_channel(split_data[0], split_data[1])
                return ResponseModel(200, "success").toDict()
        return ResponseModel(400, "error",
                             {"error_message": f"Please be sure to provide a valid channel name that exists and a "
                                               f"new valid channel name!"})
    #endregion

    #region USERS
    @router.get("/api/admin/users")
    async def users_section(self):
        return ResponseModel(200, "success").toDict()

    @router.post("/api/admin/users/join")
    async def join_user(self, command: StdModel):
        if len(command.text) > 0:
            user_channel = rutils.get_user_channel(command.text.strip())
            if user_channel:
                user_channel.move_in()
                return ResponseModel(200, "success").toDict()
        return ResponseModel(400, "error",
                             {"error_message": f"Please be sure to provide the username of a valid user in the "
                                               f"server!"})

    @router.post("/api/admin/users/move")
    async def move_user(self, command: StdModel):
        if len(command.text) > 0:
            split_data = command.text.strip().split(' ', 1)
            if len(split_data) == 2:
                rutils.move_user(split_data[0], split_data[1])
                return ResponseModel(200, "success").toDict()
        return ResponseModel(400, "error",
                             {"error_message": f"Please be sure to provide the username of a valid user"
                                               f" and a valid channel name. Please make sure the bot has"
                                               f"adequate permissions."})

    @router.post("/api/admin/users/kick")
    async def kick_user(self, command: StdModel):
        if len(command.text) > 0:
            split_data = command.text.strip().split(' ', 1)
            if len(split_data) == 2:
                rutils.kick_user(split_data[0], split_data[1])
            else:
                rutils.kick_user(command.text.strip(), reason='N/A')
            return ResponseModel(200, "success").toDict()
        return ResponseModel(400, "error",
                             {"error_message": f"Please be sure to provide the username of a valid user in the "
                                               f"server and make sure the bot has adequate permissions."})

    @router.post("/api/admin/users/mute")
    async def mute_user(self, command: StdModel):
        if len(command.text) > 0:
            if not rutils.mute(username=command.text.strip()):
                rutils.unmute(username=command.text.strip())
            return ResponseModel(200, "success").toDict()
        return ResponseModel(400, "error",
                             {"error_message": f"Please be sure to provide the username of a valid user in the "
                                               f"server and make sure the bot has adequate permissions."})

    @router.post("/api/admin/users/deafen")
    async def deafen_user(self, command: StdModel):
        if len(command.text) > 0:
            if not rutils.deafen(username=command.text.strip()):
                rutils.undeafen(username=command.text.strip())
            return ResponseModel(200, "success").toDict()
        return ResponseModel(400, "error",
                             {"error_message": f"Please be sure to provide the username of a valid user in the "
                                               f"server and make sure the bot has adequate permissions."})

    @router.post("/api/admin/users/ban")
    async def ban_user(self, command: StdModel):
        if len(command.text) > 0:
            split_data = command.text.strip().split(' ', 1)
            if len(split_data) == 2:
                rutils.ban_user(split_data[0], split_data[1])
            else:
                rutils.ban_user(command.text.strip(), reason='N/A')
            return ResponseModel(200, "success").toDict()
        return ResponseModel(400, "error",
                             {"error_message": f"Please be sure to provide the username of a valid user in the "
                                               f"server and make sure the bot has adequate permissions."})
    #endregion