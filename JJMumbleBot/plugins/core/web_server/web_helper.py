import asyncio
import threading
import hashlib
from JJMumbleBot.lib.utils.dir_utils import get_main_dir
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
from JJMumbleBot.settings import global_settings
from JJMumbleBot.plugins.core.web_server.routing.api import routing

hasher = hashlib.md5()
web_app = FastAPI()
web_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)
web_app.mount("/static", StaticFiles(directory=f"{get_main_dir()}/plugins/core/web_server/static"), name="static")
web_app.include_router(routing.router)


@web_app.exception_handler(StarletteHTTPException)
async def http_exception(request, exc):
    resp = ResponseModel(404, "error", {"error_message": "This path is invalid!"})
    return JSONResponse(resp.toDict(), media_type="application/json", status_code=404)


@web_app.get("/")
async def serve_app(request: Request):
    return Jinja2Templates(directory=f"{get_main_dir()}/plugins/core/web_server/templates").TemplateResponse("index.html", {"request": request})


@web_app.get("/favicon.ico")
async def serve_favicon(request: Request):
    favicon = open(f"{get_main_dir()}/plugins/core/web_server/static/favicon.ico", mode="rb")
    return StreamingResponse(favicon, media_type="image/x-icon")


@web_app.websocket("/ws")
async def socket_connection(websocket: WebSocket):
    await websocket.accept()
    web_tick_rate = float(global_settings.cfg[C_WEB_SETTINGS][P_WEB_TICK_RATE])
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
        self.server = UvicornServer(
            config=uvicorn.Config(
                web_app,
                host=global_settings.cfg[C_WEB_SETTINGS][P_WEB_IP],
                port=int(global_settings.cfg[C_WEB_SETTINGS][P_WEB_PAGE_PORT]),
                reload=False,
                log_level="info" if global_settings.verbose_mode else "critical",
                loop="asyncio",
                ws="websockets",
                timeout_keep_alive=99999
            )
        )

    def run(self):
        self.server.run()

    def stop(self):
        self.server.should_exit = True
        log(INFO,
            f"Stopping Web Application Server on: {global_settings.cfg[C_WEB_SETTINGS][P_WEB_IP]}:{global_settings.cfg[C_WEB_SETTINGS][P_WEB_PAGE_PORT]}/",
            origin=L_WEB_INTERFACE, print_mode=PrintMode.REG_PRINT.value)


def initialize_web():
    global_settings.data_server = ServerThreadWorker(args=(web_app), daemon=True)
    global_settings.data_server.start()
    # start_rest_server()
    log(INFO, f"Initialized API Server on: {global_settings.cfg[C_WEB_SETTINGS][P_WEB_IP]}:{global_settings.cfg[C_WEB_SETTINGS][P_WEB_PAGE_PORT]}/api/", origin=L_WEB_INTERFACE, print_mode=PrintMode.REG_PRINT.value)
    log(INFO, f"Server API documentation can be found on: {global_settings.cfg[C_WEB_SETTINGS][P_WEB_IP]}:{global_settings.cfg[C_WEB_SETTINGS][P_WEB_PAGE_PORT]}/docs/", origin=L_WEB_INTERFACE, print_mode=PrintMode.REG_PRINT.value)
    log(INFO, f"Initialized Web Application on: {global_settings.cfg[C_WEB_SETTINGS][P_WEB_IP]}:{global_settings.cfg[C_WEB_SETTINGS][P_WEB_PAGE_PORT]}/", origin=L_WEB_INTERFACE, print_mode=PrintMode.REG_PRINT.value)
