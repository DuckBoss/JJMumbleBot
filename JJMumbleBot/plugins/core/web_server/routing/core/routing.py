from pymumble_py3.constants import PYMUMBLE_CLBK_TEXTMESSAGERECEIVED
from JJMumbleBot.plugins.core.web_server import monitor_service
from JJMumbleBot.lib.utils.runtime_utils import get_bot_name, get_command_history, clear_command_history
from JJMumbleBot.plugins.core.web_server.utility.web_utils import ResponseModel, StdModel
from JJMumbleBot.lib.utils.remote_utils import RemoteTextMessage
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.settings import global_settings
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

router = InferringRouter()


@cbv(router)
class CoreRouter:
    #region CORE
    @router.get("/api/")
    async def main_api(self):
        return ResponseModel(200, "success").toDict()

    @router.get("/api/admin/")
    async def admin_api(self):
        return ResponseModel(200, "success").toDict()

    @router.get("/api/admin/plugins/")
    async def admin_plugin_api(self):
        return ResponseModel(200, "success").toDict()

    @router.post("/api/command")
    async def send_command(self, command: StdModel):
        if len(command.text) > 0:
            if command.text[0] == global_settings.cfg[C_MAIN_SETTINGS][P_CMD_TOKEN]:
                text = RemoteTextMessage(channel_id=global_settings.mumble_inst.users.myself['channel_id'],
                                         session=global_settings.mumble_inst.users.myself['session'],
                                         message=command.text,
                                         actor=global_settings.mumble_inst.users.myself['session'])
                global_settings.core_callbacks.callback(PYMUMBLE_CLBK_TEXTMESSAGERECEIVED, text, True)
                return ResponseModel(200, "success").toDict()
            return ResponseModel(400, "error", {"error_message": f"The provided command was invalid! Please be sure that your command starts with '{global_settings.cfg[C_MAIN_SETTINGS][P_CMD_TOKEN]}'.\n"
                                                                 f"For Additional assistance, try the {global_settings.cfg[C_MAIN_SETTINGS][P_CMD_TOKEN]}help command."}).toDict()
        return ResponseModel(500, "error", {"error_message": f"There was an error processing the provided command."}).toDict()

    @router.get("/api/lastcommand")
    async def last_command(self):
        last_cmd = monitor_service.get_last_command_output()
        if last_cmd:
            return ResponseModel(200, "success", last_cmd).toDict()
        return ResponseModel(500, "error", {"error_message": "There was an error retrieving the last command output."}).toDict()

    @router.post("/api/clearcmdhistory")
    async def clear_cmd_history(self):
        clear_command_history()
        return ResponseModel(200, "success").toDict()

    @router.get("/api/cmdhistory")
    async def cmd_history(self):
        cmd_strings = list(get_command_history())
        return ResponseModel(200, "success", {"cmd_history": cmd_strings}).toDict()

    @router.get("/api/plugins")
    async def get_plugins(self):
        all_plugins = list(global_settings.bot_plugins)
        return ResponseModel(200, "success", {"plugins": all_plugins}).toDict()

    @router.get("/api/channels")
    async def get_channels(self):
        all_channels = monitor_service.get_all_online()
        return ResponseModel(200, "success", all_channels).toDict()
    #endregion CORE

    #region GENERAL
    @router.get("/api/general/system")
    async def get_system_info(self):
        return ResponseModel(
            200, "success",
            {"system": monitor_service.get_system_info()}
        ).toDict()

    @router.get("/api/general/name")
    async def get_name(self):
        return ResponseModel(
            200, "success",
            {"name": get_bot_name()}
        ).toDict()

    @router.get("/api/general/token")
    async def get_token(self):
        return ResponseModel(
            200, "success",
            {"command_token": global_settings.cfg[C_MAIN_SETTINGS][P_CMD_TOKEN]}
        ).toDict()

    @router.get("/api/general")
    async def general_api(self):
        return ResponseModel(
            200, "success",
            {"name": get_bot_name(), "command_token": global_settings.cfg[C_MAIN_SETTINGS][P_CMD_TOKEN]}
        ).toDict()
    #endregion