from JJMumbleBot.plugins.core.web_server.utility.web_utils import ResponseModel, StdModel
from JJMumbleBot.settings import global_settings
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

router = InferringRouter()


@cbv(router)
class AudioRouter:
    @router.post("/api/audio/pause")
    async def pause_audio(self):
        if global_settings.aud_interface.status.is_playing():
            global_settings.aud_interface.pause()
        return ResponseModel(200, "success").toDict()

    @router.post("/api/audio/resume")
    async def resume_audio(self):
        if global_settings.aud_interface.status.is_paused():
            global_settings.aud_interface.resume()
        return ResponseModel(200, "success").toDict()

    @router.post("/api/audio/replay")
    async def replay_audio(self):
        global_settings.aud_interface.replay()
        return ResponseModel(200, "success").toDict()

    @router.post("/api/audio/nexttrack")
    async def next_audio(self):
        global_settings.aud_interface.skip(0)
        return ResponseModel(200, "success").toDict()

    @router.post("/api/audio/shuffle")
    async def shuffle_audio(self):
        global_settings.aud_interface.shuffle()
        return ResponseModel(200, "success").toDict()

    @router.post("/api/audio/decreasevolume")
    async def decrease_volume_audio(self):
        global_settings.aud_interface.audio_utilities.set_volume_fast(
            global_settings.aud_interface.status.get_volume() - 0.1, auto=False)
        return ResponseModel(200, "success").toDict()

    @router.post("/api/audio/increasevolume")
    async def increase_volume_audio(self):
        global_settings.aud_interface.audio_utilities.set_volume_fast(
            global_settings.aud_interface.status.get_volume() + 0.1, auto=False)
        return ResponseModel(200, "success").toDict()

    @router.post("/api/audio/loop")
    async def loop_audio(self):
        global_settings.aud_interface.loop_track()
        return ResponseModel(200, "success").toDict()

    @router.post("/api/audio/skipto")
    async def skip_to_track(self, request: StdModel):
        if len(request.text) > 0:
            global_settings.aud_interface.skip(int(request.text))
            return ResponseModel(200, "success").toDict()
        return ResponseModel(400, "error", {"error_message": "The provided track was invalid!"}).toDict()

    @router.post("/api/audio/removetrack")
    async def remove_track(self, request: StdModel):
        if len(request.text) > 0:
            global_settings.aud_interface.remove_track(track_index=int(request.text))
            return ResponseModel(200, "success").toDict()
        return ResponseModel(400, "error", {"error_message": "The provided track was invalid!"}).toDict()

    @router.post("/api/audio/stop")
    async def stop_audio(self):
        if not global_settings.aud_interface.status.is_stopped():
            global_settings.aud_interface.stop()
            global_settings.gui_service.quick_gui(
                f"Stopped audio interface.",
                text_type='header',
                box_align='left')
        return ResponseModel(200, "success").toDict()
