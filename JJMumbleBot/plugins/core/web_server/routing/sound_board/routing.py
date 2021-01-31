from pymumble_py3.constants import PYMUMBLE_CLBK_TEXTMESSAGERECEIVED
from JJMumbleBot.plugins.core.web_server.utility.web_utils import ResponseModel, StdModel
from JJMumbleBot.lib.utils.remote_utils import RemoteTextMessage
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.settings import global_settings
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

router = InferringRouter()


@cbv(router)
class SoundBoardPluginAPI:
    @router.get("/api/sound_board/clips")
    async def get_soundboard_data(self):
        if "sound_board" in list(global_settings.bot_plugins):
            import JJMumbleBot.plugins.extensions.sound_board.utility.sound_board_utility as sbu
            clips_list = sbu.prepare_sb_list()
            return ResponseModel(200, "success", {"clips": clips_list}).toDict()
        return ResponseModel(500, "error",
                             {"error_message": "Encountered an error retrieving sound_board clips."}).toDict()

    @router.post("/api/sound_board/random")
    async def play_random_soundboard(self):
        if "sound_board" in list(global_settings.bot_plugins):
            text = RemoteTextMessage(channel_id=global_settings.mumble_inst.users.myself['channel_id'],
                                     session=global_settings.mumble_inst.users.myself['session'],
                                     message=f"{global_settings.cfg[C_MAIN_SETTINGS][P_CMD_TOKEN]}sbrandomquietnow",
                                     actor=global_settings.mumble_inst.users.myself['session'])
            global_settings.core_callbacks.callback(PYMUMBLE_CLBK_TEXTMESSAGERECEIVED, text, True)
            return ResponseModel(200, "success").toDict()
        return ResponseModel(400, "error", {
            "error_message": "Encountered an error while trying to play a random sound clip!"}).toDict()

    @router.post("/api/sound_board/play")
    async def play_soundboard_clip(self, request: StdModel):
        if len(request.text) > 0 and "sound_board" in list(global_settings.bot_plugins):
            text = RemoteTextMessage(channel_id=global_settings.mumble_inst.users.myself['channel_id'],
                                     session=global_settings.mumble_inst.users.myself['session'],
                                     message=f"{global_settings.cfg[C_MAIN_SETTINGS][P_CMD_TOKEN]}sbquietnow {request.text}",
                                     actor=global_settings.mumble_inst.users.myself['session'])
            global_settings.core_callbacks.callback(PYMUMBLE_CLBK_TEXTMESSAGERECEIVED, text, True)
            return ResponseModel(200, "success").toDict()
        return ResponseModel(400, "error", {"error_message": "The provided sound_board clip is invalid!"}).toDict()