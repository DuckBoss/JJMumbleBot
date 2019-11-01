from JJMumbleBot.lib.web.web_interface.utility import web_interface_utility as wiu
from JJMumbleBot.settings import runtime_settings
from flask import Flask, render_template
from flask_socketio import SocketIO
from os import urandom
from JJMumbleBot.settings import global_settings as GS

web_app = Flask(__name__)
web_app.config['SECRET_KEY'] = urandom(16)
GS.socket_service = SocketIO(web_app, cors_allowed_origins='*')


def start_server():
    GS.socket_service.run(
        web_app,
        host=runtime_settings.web_ip or '0.0.0.0',
        port=runtime_settings.web_port or 5000,
        debug=False,
        log_output=False
    )


def stop_server():
    from requests import post
    url = f'http://{runtime_settings.web_ip or "0.0.0.0"}:{runtime_settings.web_port or 5000}/exit'
    post(url)


@web_app.route('/')
def main_page():
    return render_template('index.html',
                           host=f'http://{runtime_settings.web_ip or "0.0.0.0"}',
                           port=runtime_settings.web_port or 5000)


@web_app.route('/exit', methods=['GET', 'POST'])
def exit_server():
    GS.socket_service.stop()
    GS.socket_service = None


@GS.socket_service.on('get-online-clients')
def send_active_clients():
    GS.socket_service.emit('get-online-clients', wiu.get_online_users(), broadcast=True)


@GS.socket_service.on('get-whisper-clients')
def send_active_clients():
    GS.socket_service.emit('get-whisper-clients', wiu.get_whisper_data_json(), broadcast=True)


@GS.socket_service.on('get-uptime')
def send_uptime():
    GS.socket_service.emit('get-uptime', wiu.get_uptime_json(), broadcast=True)


@GS.socket_service.on('get-cpu-info')
def send_bot_info():
    GS.socket_service.emit('get-cpu-info', wiu.get_cpu_percentage(), broadcast=True)


@GS.socket_service.on('get-ram-info')
def send_bot_info():
    GS.socket_service.emit('get-ram-info', wiu.get_ram_percentage(), broadcast=True)
