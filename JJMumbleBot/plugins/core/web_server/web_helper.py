import asyncio
import threading
from JJMumbleBot.lib.utils.dir_utils import get_core_plugin_dir
import uvicorn
from websockets.exceptions import ConnectionClosedOK
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

from JJMumbleBot.plugins.core.web_server import monitor_service
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.utils.print_utils import PrintMode
from JJMumbleBot.plugins.core.web_server.utility.web_utils import ResponseModel
from JJMumbleBot.plugins.core.web_server.resources.strings import *
from JJMumbleBot.settings import global_settings
from JJMumbleBot.plugins.core.web_server.routing.core import routing as core_routing
from JJMumbleBot.plugins.core.web_server.routing.audio import routing as audio_routing
from JJMumbleBot.plugins.core.web_server.routing.bot_commands import routing as bot_commands_routing
from JJMumbleBot.plugins.core.web_server.routing.core_commands import routing as core_commands_routing
from JJMumbleBot.plugins.core.web_server.routing.sound_board import routing as sound_board_routing

web_app = FastAPI(
    title="JJMumbleBot Web API",
    description="This is the REST API for JJMumbleBot built with FastAPI",
    version=META_VERSION,
    redoc_url=None
)
web_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)
web_app.mount("/static", StaticFiles(directory=f"{get_core_plugin_dir()}/web_server/static"), name="static")
web_app.include_router(core_routing.router)
web_app.include_router(audio_routing.router)
web_app.include_router(bot_commands_routing.router)
web_app.include_router(core_commands_routing.router)
web_app.include_router(sound_board_routing.router)


@web_app.exception_handler(StarletteHTTPException)
async def http_exception(request, exc):
    resp = ResponseModel(404, "error", {"error_message": "This path is invalid!"})
    return JSONResponse(resp.toDict(), media_type="application/json", status_code=404)


@web_app.get("/")
async def serve_app(request: Request):
    return Jinja2Templates(directory=f"{get_core_plugin_dir()}/web_server/templates").TemplateResponse("index.html", {"request": request})


@web_app.get("/favicon.ico")
async def serve_favicon(request: Request):
    favicon = open(f"{get_core_plugin_dir()}/web_server/static/favicon.ico", mode="rb")
    return StreamingResponse(favicon, media_type="image/x-icon")


@web_app.websocket("/ws")
async def socket_connection(websocket: WebSocket):
    await websocket.accept()
    web_tick_rate = float(global_settings.web_cfg[C_PLUGIN_SET][P_WEB_TICK_RATE])
    try:
        while True:
            await websocket.send_json(monitor_service.get_all_socket_data())
            await asyncio.sleep(web_tick_rate)
    except WebSocketDisconnect:
        await websocket.close()
    except ConnectionClosedOK:
        await websocket.close()


class UvicornServer(uvicorn.Server):
    def __init__(self, *args, **kwargs):
        super(UvicornServer, self).__init__(*args, **kwargs)


class ServerThreadWorker(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(ServerThreadWorker, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.ip = kwargs["kwargs"]["ip"]
        self.port = int(kwargs["kwargs"]["port"])
        self.server = UvicornServer(
            config=uvicorn.Config(
                web_app,
                host=self.ip,
                port=self.port,
                reload=False,
                log_level="info" if global_settings.verbose_mode else "critical",
                loop="asyncio",
                ws="websockets",
                ssl_certfile=kwargs["kwargs"].get("ssl_cert"),
                ssl_keyfile=kwargs["kwargs"].get("ssl_key"),
                timeout_keep_alive=99999
            )
        )

    def run(self):
        self.server.run()

    def stop(self):
        self.server.should_exit = True
        log(INFO,
            f"Stopping Web Application Server on: {self.ip}:{self.port}/",
            origin=L_WEB_INTERFACE, print_mode=PrintMode.REG_PRINT.value)


def initialize_web(ip, port, use_https=False, ssl_cert=None, ssl_key=None):
    global_settings.data_server = ServerThreadWorker(
        kwargs={
            "ip": ip, "port": port,
            "ssl_cert": ssl_cert if use_https else None,
            "ssl_key": ssl_key if use_https else None
            },
        daemon=True
    )
    global_settings.data_server.start()
    # start_rest_server()
    log(INFO, f"Initialized API Server on: {ip}:{port}/api/", origin=L_WEB_INTERFACE, print_mode=PrintMode.REG_PRINT.value)
    log(INFO, f"Server API documentation can be found on: {ip}:{port}/docs/", origin=L_WEB_INTERFACE, print_mode=PrintMode.REG_PRINT.value)
    log(INFO, f"Initialized Web Application on: {ip}:{port}/", origin=L_WEB_INTERFACE, print_mode=PrintMode.REG_PRINT.value)


def generate_cert():
    from os import path
    from subprocess import call
    from JJMumbleBot.lib.utils.dir_utils import get_plugin_data_dir
    import configparser
    if not path.exists(f'{get_plugin_data_dir()}/web_server/web_cert.pem') or not path.exists(f'{get_plugin_data_dir()}/web_server/web_key.pem'):
        call(['openssl', 'req', '-x509', '-nodes', '-days', '3650',
              '-newkey', 'rsa:2048', '-keyout', f'{get_plugin_data_dir()}/web_server/web_key.pem',
              '-out', f'{get_plugin_data_dir()}/web_server/web_cert.pem', '-subj',
              f'/CN={global_settings.cfg[C_CONNECTION_SETTINGS][P_USER_ID]}'])
        global_settings.web_cfg[C_PLUGIN_SET][P_SSL_CERT] = f'{get_plugin_data_dir()}/web_server/web_cert.pem'
        global_settings.web_cfg[C_PLUGIN_SET][P_SSL_KEY] = f'{get_plugin_data_dir()}/web_server/web_key.pem'

        cfg = configparser.ConfigParser()
        for key, values in global_settings.web_cfg.items():
            cfg[key] = {}
            for item, value in values.items():
                cfg[key][item] = value
        try:
            with open(f'{get_core_plugin_dir}/web_server/metadata.ini', 'w') as f:
                cfg.write(f)
            global_settings.web_cfg = configparser.ConfigParser()
            global_settings.web_cfg.read(f'{get_core_plugin_dir()}/web_server/metadata.ini')
        except IOError as e:
            log(ERROR, f"Encountered an error while updating the web_server metadata file: {e}",
                origin=L_GENERAL, error_type=GEN_PROCESS_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            return False
        return True
    return False
