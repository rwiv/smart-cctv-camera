import subprocess
import time

from cam_server.exec import exec_camera
from fastapi import APIRouter, Query

router = APIRouter()

p1: subprocess.Popen[bytes] | None = None
p2: subprocess.Popen[bytes] | None = None


@router.get("/")
def index() -> str:
    return "hello"


@router.get("/start")
def index(t: int = Query(20)) -> str:
    global p1, p2
    p1, p2 = exec_camera()
    time.sleep(t)
    kill()
    return "end"


@router.get("/stop")
def index() -> str:
    kill()
    return "end"


def kill():
    global p1, p2
    if p2 is not None:
        p2.kill()

    if p1 is not None:
        p1.kill()
