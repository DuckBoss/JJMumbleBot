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
import json
from os import urandom

web_app = Flask(__name__)
web_app.config['SECRET_KEY'] = urandom(16)


async def send_message(websocket, path):
    try:
        while True:
            web_data = monitor_service.get_all_plugins()
            web_data.update(monitor_service.get_hardware_info())
            web_data.update(monitor_service.get_system_info())
            web_data["cur_time"] = str(datetime.now()).split('.')[0]

            packed_data = json.dumps(web_data)
            await websocket.send(packed_data)
            await asyncio.sleep(1)
    except websockets.ConnectionClosed:
        return


@web_app.route("/command", methods=["GET", "POST"])
def get_message():
    content = request.form['commandInput']
    if len(content) > 0:
        if content[0] == global_settings.cfg[C_MAIN_SETTINGS][P_CMD_TOKEN]:
            text = RemoteTextMessage(channel_id=global_settings.mumble_inst.users.myself['channel_id'],
                                     session=global_settings.mumble_inst.users.myself['session'],
                                     message=content,
                                     actor=global_settings.mumble_inst.users.myself['session'])
            global_settings.bot_service.remote_message_received(text=text)
            print(text)
    return content


@web_app.route("/", methods=['GET', 'POST'])
def main():
    return render_template('index.html')


def start_flask_server():
    global_settings.flask_server = WSGIServer(("192.168.1.200", int(global_settings.cfg[C_WEB_SETTINGS][P_WEB_PAGE_PORT])), web_app, log=None)
    global_settings.flask_server.serve_forever()
    rprint("Initialized Flask Server.", origin=L_WEB_INTERFACE)
    log(INFO, "Initialized Flask Server", origin=L_WEB_INTERFACE)


def initialize_web():
    ws = websockets.serve(send_message, "192.168.1.200", int(global_settings.cfg[C_WEB_SETTINGS][P_WEB_SOCK_PORT]), origins=None)
    asyncio.get_event_loop().run_until_complete(ws)
    global_settings.socket_server = Thread(target=asyncio.get_event_loop().run_forever)
    global_settings.socket_server.start()
    rprint("Initialized Socket Server.", origin=L_WEB_INTERFACE)
    log(INFO, "Initialized Socket Server", origin=L_WEB_INTERFACE)

    global_settings.flask_server = Thread(target=start_flask_server)
    global_settings.flask_server.start()
    rprint("Initialized Flask Server.", origin=L_WEB_INTERFACE)
    log(INFO, "Initialized Flask Server", origin=L_WEB_INTERFACE)
