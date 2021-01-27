from pymumble_py3.constants import PYMUMBLE_CLBK_TEXTMESSAGERECEIVED
from JJMumbleBot.plugins.core.web_server import monitor_service
from JJMumbleBot.lib.utils.runtime_utils import get_bot_name, get_command_history, clear_command_history
from JJMumbleBot.plugins.core.web_server.utility.web_utils import ResponseModel, StdModel
from JJMumbleBot.lib.utils.remote_utils import RemoteTextMessage
from fastapi import APIRouter
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.settings import global_settings

router = APIRouter()


@router.post("/api/command")
async def send_command(command: StdModel):
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
async def last_command():
    last_cmd = monitor_service.get_last_command_output()
    if last_cmd:
        return ResponseModel(200, "success", last_cmd).toDict()
    return ResponseModel(500, "error", {"error_message": "There was an error retrieving the last command output."}).toDict()


@router.post("/api/pause")
async def pause_audio():
    if global_settings.aud_interface.status.is_playing():
        global_settings.aud_interface.pause()
    return ResponseModel(200, "success").toDict()


@router.post("/api/resume")
async def resume_audio():
    if global_settings.aud_interface.status.is_paused():
        global_settings.aud_interface.resume()
    return ResponseModel(200, "success").toDict()


@router.post("/api/replay")
async def replay_audio():
    global_settings.aud_interface.replay()
    return ResponseModel(200, "success").toDict()


@router.post("/api/nexttrack")
async def next_audio():
    global_settings.aud_interface.skip(0)
    return ResponseModel(200, "success").toDict()


@router.post("/api/shuffle")
async def shuffle_audio():
    global_settings.aud_interface.shuffle()
    return ResponseModel(200, "success").toDict()


@router.post("/api/decreasevolume")
async def decrease_volume_audio():
    global_settings.aud_interface.audio_utilities.set_volume_fast(
        global_settings.aud_interface.status.get_volume() - 0.1, auto=False)
    return ResponseModel(200, "success").toDict()


@router.post("/api/increasevolume")
async def increase_volume_audio():
    global_settings.aud_interface.audio_utilities.set_volume_fast(
        global_settings.aud_interface.status.get_volume() + 0.1, auto=False)
    return ResponseModel(200, "success").toDict()


@router.post("/api/clearcmdhistory")
async def clear_cmd_history():
    clear_command_history()
    return ResponseModel(200, "success").toDict()


@router.get("/api/cmdhistory")
async def cmd_history():
    cmd_strings = list(get_command_history())
    return ResponseModel(200, "success", {"cmd_history": cmd_strings}).toDict()


@router.post("/api/loop")
async def loop_audio():
    global_settings.aud_interface.loop_track()
    return ResponseModel(200, "success").toDict()


@router.post("/api/skipto")
async def skip_to_track(request: StdModel):
    if len(request.text) > 0:
        global_settings.aud_interface.skip(int(request.text))
        return ResponseModel(200, "success").toDict()
    return ResponseModel(400, "error", {"error_message": "The provided track was invalid!"}).toDict()


@router.post("/api/removetrack")
async def remove_track(request: StdModel):
    if len(request.text) > 0:
        global_settings.aud_interface.remove_track(track_index=int(request.text))
        return ResponseModel(200, "success").toDict()
    return ResponseModel(400, "error", {"error_message": "The provided track was invalid!"}).toDict()


@router.post("/api/stop")
async def stop_audio():
    if not global_settings.aud_interface.status.is_stopped():
        global_settings.aud_interface.stop()
        global_settings.gui_service.quick_gui(
            f"Stopped audio interface.",
            text_type='header',
            box_align='left')
    return ResponseModel(200, "success").toDict()


@router.get("/api/plugins")
async def get_plugins():
    all_plugins = list(global_settings.bot_plugins)
    return ResponseModel(200, "success", {"plugins": all_plugins}).toDict()


@router.get("/api/channels")
async def get_channels():
    all_channels = monitor_service.get_all_online()
    return ResponseModel(200, "success", all_channels).toDict()


@router.get("/api/soundboardclips")
async def get_soundboard_data():
    if "sound_board" in list(global_settings.bot_plugins):
        import JJMumbleBot.plugins.extensions.sound_board.utility.sound_board_utility as sbu
        clips_list = sbu.prepare_sb_list()
        return ResponseModel(200, "success", {"clips": clips_list}).toDict()
    return ResponseModel(500, "error", {"error_message": "Encountered an error retrieving sound_board clips."}).toDict()


@router.post("/api/soundboard-random")
async def play_random_soundboard():
    if "sound_board" in list(global_settings.bot_plugins):
        text = RemoteTextMessage(channel_id=global_settings.mumble_inst.users.myself['channel_id'],
                                 session=global_settings.mumble_inst.users.myself['session'],
                                 message=f"{global_settings.cfg[C_MAIN_SETTINGS][P_CMD_TOKEN]}sbrandomquietnow",
                                 actor=global_settings.mumble_inst.users.myself['session'])
        global_settings.core_callbacks.callback(PYMUMBLE_CLBK_TEXTMESSAGERECEIVED, text, True)
        return ResponseModel(200, "success").toDict()
    return ResponseModel(400, "error", {"error_message": "Encountered an error while trying to play a random sound clip!"}).toDict()

@router.post("/api/soundboard-play")
async def play_soundboard_clip(request: StdModel):
    if len(request.text) > 0:
        text = RemoteTextMessage(channel_id=global_settings.mumble_inst.users.myself['channel_id'],
                                 session=global_settings.mumble_inst.users.myself['session'],
                                 message=f"{global_settings.cfg[C_MAIN_SETTINGS][P_CMD_TOKEN]}sbquietnow {request.text}",
                                 actor=global_settings.mumble_inst.users.myself['session'])
        global_settings.core_callbacks.callback(PYMUMBLE_CLBK_TEXTMESSAGERECEIVED, text, True)
        return ResponseModel(200, "success").toDict()
    return ResponseModel(400, "error", {"error_message": "The provided sound_board clip is invalid!"}).toDict()


@router.get("/api/system")
async def get_system_info():
    return ResponseModel(
        200, "success",
        {"system": monitor_service.get_system_info()}
    ).toDict()


@router.get("/api/general/name")
async def get_name():
    return ResponseModel(
        200, "success",
        {"name": get_bot_name()}
    ).toDict()


@router.get("/api/general/token")
async def get_token():
    return ResponseModel(
        200, "success",
        {"command_token": global_settings.cfg[C_MAIN_SETTINGS][P_CMD_TOKEN]}
    ).toDict()


@router.get("/api/general")
async def get_token():
    return ResponseModel(
        200, "success",
        {"name": get_bot_name(), "command_token": global_settings.cfg[C_MAIN_SETTINGS][P_CMD_TOKEN]}
    ).toDict()


@router.get("/api/")
async def main():
    return ResponseModel(200, "success").toDict()
