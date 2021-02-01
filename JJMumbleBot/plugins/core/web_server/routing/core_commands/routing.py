from pymumble_py3.constants import PYMUMBLE_CLBK_TEXTMESSAGERECEIVED
from JJMumbleBot.plugins.core.web_server import monitor_service
from JJMumbleBot.lib.utils.runtime_utils import get_bot_name, get_command_history, clear_command_history
from JJMumbleBot.plugins.core.web_server.utility.web_utils import ResponseModel, StdModel
from JJMumbleBot.plugins.core.core_commands.utility import core_commands_utility as cutils
from JJMumbleBot.lib.utils.remote_utils import RemoteTextMessage
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.utils import runtime_utils as rutils
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

router = InferringRouter()


@cbv(router)
class CoreCommandsPluginAPI:
    @router.get("/api/general/uptime")
    async def get_uptime(self):
        return ResponseModel(200, "success", rutils.check_up_time()).toDict()

    @router.get("/api/general/version")
    async def get_version(self):
        return ResponseModel(200, "success", f"{rutils.get_bot_name()} is on version {rutils.get_version()}").toDict()

    @router.get("/api/general/about")
    async def get_about(self):
        return ResponseModel(200, "success", f"{rutils.get_about()}<br>{rutils.get_bot_name()} is on version {rutils.get_version()}").toDict()

    @router.post("/api/admin/plugins/metadata")
    async def get_plugin_metadata(self, command: StdModel):
        if len(command.text.strip()) > 0:
            plugin_metadata = rutils.get_plugin_metadata(command.text.strip())
            if plugin_metadata:
                return ResponseModel(200, "success", {"metadata": plugin_metadata}).toDict()
        return ResponseModel(400, "error",
                             {"error_message": f"Please make sure you provide an existing plugin to retrieve metadata."}).toDict()

    @router.post("/api/admin/plugins/stop")
    async def stop_plugin(self, command: StdModel):
        if len(command.text.strip()) > 0:
            if cutils.turn_off_plugin(command.text.strip()):
                return ResponseModel(200, "success", {"message": f"Successfully stopped plugin: {command.text.strip()}"}).toDict()
        return ResponseModel(400, "error",
                             {"error_message": f"Please make sure you provide an existing, active plugin to stop."}).toDict()

    @router.post("/api/admin/plugins/start")
    async def start_plugin(self, command: StdModel):
        if len(command.text.strip()) > 0:
            if cutils.turn_on_plugin(command.text.strip()):
                return ResponseModel(200, "success", {"message": f"Successfully started plugin: {command.text.strip()}"}).toDict()
        return ResponseModel(400, "error",
                             {"error_message": f"Please make sure you provide an existing, stopped plugin to start."}).toDict()

    @router.post("/api/admin/plugins/restart")
    async def restart_plugin(self, command: StdModel):
        if len(command.text.strip()) > 0:
            if cutils.restart_plugin(command.text.strip()):
                return ResponseModel(200, "success",
                                     {"message": f"Successfully restarted plugin: {command.text.strip()}"}).toDict()
        return ResponseModel(400, "error",
                             {"error_message": f"Please make sure you provide an existing plugin to restart."}).toDict()

    @router.post("/api/admin/plugins/restart_all")
    async def restart_all_plugins(self):
        rutils.refresh_plugins()
        return ResponseModel(200, "success").toDict()
