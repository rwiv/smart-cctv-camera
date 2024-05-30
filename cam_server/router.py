import subprocess
import time

from cam_server.exec import exec_camera
from fastapi import APIRouter

router = APIRouter()

p1: subprocess.Popen[bytes] | None = None
p2: subprocess.Popen[bytes] | None = None


@router.get("/")
def index() -> str:
    return "hello"


@router.get("/start")
def index() -> str:
    p1, p2 = exec_camera()
    time.sleep(20)
    kill()
    return "end"


@router.get("/end")
def index() -> str:
    kill()
    return "end"


def kill():
    if p1 is not None:
        p1.kill()

    if p2 is not None:
        p2.kill()
