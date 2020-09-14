import asyncio
import websockets
from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.utils.print_utils import dprint, rprint
from JJMumbleBot.lib.utils.logging_utils import log
from datetime import datetime
from flask import Flask, request
from flask import render_template
from gevent.pywsgi import WSGIServer
from threading import Thread
from JJMumbleBot.lib import monitor_service
from JJMumbleBot.lib.utils.web_utils import RemoteTextMessage
from JJMumbleBot.lib.utils.runtime_utils import check_up_time, get_bot_name
from pymumble_py3.constants import PYMUMBLE_CLBK_TEXTMESSAGERECEIVED
import json
from os import urandom


web_app = Flask(__name__)
web_app.config['SECRET_KEY'] = urandom(16)


async def send_message(websocket, path):
    web_tick_rate = float(global_settings.cfg[C_WEB_SETTINGS][P_WEB_TICK_RATE])
    try:
        while True:
            web_data = {"cur_time": str(datetime.now()).split('.')[0]}
            web_data.update({"bot_uptime": f'{check_up_time()}'})
            web_data.update(monitor_service.get_last_command_output())
            web_data.update(monitor_service.get_all_online())
            web_data.update(monitor_service.get_audio_info())
            packed_data = json.dumps(web_data)
            await websocket.send(packed_data)
            await asyncio.sleep(web_tick_rate)
    except websockets.ConnectionClosed:
        return


@web_app.route("/command", methods=["POST"])
def post_message():
    content = request.form['commandInput']
    if len(content) > 0:
        if content[0] == global_settings.cfg[C_MAIN_SETTINGS][P_CMD_TOKEN]:
            text = RemoteTextMessage(channel_id=global_settings.mumble_inst.users.myself['channel_id'],
                                     session=global_settings.mumble_inst.users.myself['session'],
                                     message=content,
                                     actor=global_settings.mumble_inst.users.myself['session'])
            global_settings.core_callbacks.callback(PYMUMBLE_CLBK_TEXTMESSAGERECEIVED, text, True)
            # print(text.message)
    return content


@web_app.route("/pause", methods=["POST"])
def pause_audio():
    if global_settings.aud_interface.status.is_playing():
        global_settings.aud_interface.pause()
    return ''


@web_app.route("/resume", methods=["POST"])
def resume_audio():
    if global_settings.aud_interface.status.is_paused():
        global_settings.aud_interface.resume()
    return ''


@web_app.route("/nexttrack", methods=["POST"])
def next_audio():
    global_settings.aud_interface.skip(0)
    return ''


@web_app.route("/shuffle", methods=["POST"])
def shuffle_audio():
    global_settings.aud_interface.shuffle()
    return ''


@web_app.route("/decreasevolume", methods=["POST"])
def decrease_volume_audio():
    global_settings.aud_interface.audio_utilities.set_volume_fast(global_settings.aud_interface.status.get_volume() - 0.1, auto=False)
    return ''


@web_app.route("/increasevolume", methods=["POST"])
def increase_volume_audio():
    global_settings.aud_interface.audio_utilities.set_volume_fast(global_settings.aud_interface.status.get_volume() + 0.1, auto=False)
    return ''


@web_app.route("/loop", methods=["POST"])
def loop_audio():
    global_settings.aud_interface.loop_track()
    return ''


@web_app.route("/skipto", methods=["POST"])
def skip_to_track():
    if request.json:
        skip_to = request.json['data'].split('-', 1)[0]
        global_settings.aud_interface.skip(int(skip_to))
    return {}


@web_app.route("/removetrack", methods=["POST"])
def remove_track():
    if request.json:
        remove = request.json['data'].split('-', 1)[0]
        global_settings.aud_interface.remove_track(track_index=int(remove))
    return {}


@web_app.route("/stop", methods=["POST"])
def stop_audio():
    if not global_settings.aud_interface.status.is_stopped():
        global_settings.aud_interface.stop()
        global_settings.gui_service.quick_gui(
            f"Stopped audio interface.",
            text_type='header',
            box_align='left')
    return ''


@web_app.route("/plugins", methods=['GET'])
def get_plugins():
    cmd_strings = list(global_settings.bot_plugins)
    return json.dumps({"plugins": cmd_strings})


@web_app.route("/channels", methods=['GET'])
def get_channels():
    cmd_strings = monitor_service.get_all_online()
    return cmd_strings


@web_app.route("/system", methods=['GET'])
def get_system_info():
    return json.dumps(monitor_service.get_system_info())


@web_app.route("/", methods=['GET', 'POST'])
def main():
    return render_template(
        'index.html',
        server_ip=global_settings.cfg[C_WEB_SETTINGS][P_WEB_IP],
        server_port=int(global_settings.cfg[C_WEB_SETTINGS][P_WEB_PAGE_PORT]),
        socket_port=int(global_settings.cfg[C_WEB_SETTINGS][P_WEB_SOCK_PORT]),
        bot_name=get_bot_name(),
        command_token=global_settings.cfg[C_MAIN_SETTINGS][P_CMD_TOKEN],
        plugins=list(global_settings.bot_plugins)
    )


def start_flask_server():
    global_settings.flask_server = WSGIServer((global_settings.cfg[C_WEB_SETTINGS][P_WEB_IP], int(global_settings.cfg[C_WEB_SETTINGS][P_WEB_PAGE_PORT])),
                                              web_app, log=None)
    global_settings.flask_server.serve_forever()


def initialize_web():
    ws = websockets.serve(send_message, global_settings.cfg[C_WEB_SETTINGS][P_WEB_IP], int(global_settings.cfg[C_WEB_SETTINGS][P_WEB_SOCK_PORT]),
                          origins=None)
    asyncio.get_event_loop().run_until_complete(ws)
    global_settings.socket_server = Thread(target=asyncio.get_event_loop().run_forever, daemon=True)
    global_settings.socket_server.start()
    rprint("Initialized Socket Server.", origin=L_WEB_INTERFACE)
    log(INFO, "Initialized Socket Server", origin=L_WEB_INTERFACE)

    global_settings.flask_server = Thread(target=start_flask_server, daemon=True)
    global_settings.flask_server.start()
    rprint("Initialized Flask Server.", origin=L_WEB_INTERFACE)
    log(INFO, "Initialized Flask Server", origin=L_WEB_INTERFACE)
