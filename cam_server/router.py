import asyncio
import os
import shutil
import subprocess

from cam_server.exec import exec_camera
from fastapi import APIRouter, Query, HTTPException

router = APIRouter()

p1: subprocess.Popen[bytes] | None = None
p2: subprocess.Popen[bytes] | None = None


async def delay_kill(delay: int):
    await asyncio.sleep(delay)
    kill()


@router.get("/")
def index() -> str:
    return "hello"


@router.get("/start")
async def start(t: int = Query(20)) -> str:
    global p1, p2
    if p1 is not None or p2 is not None:
        raise HTTPException(status_code=400, detail="already started")

    p1, p2 = exec_camera()
    asyncio.create_task(delay_kill(t))
    return "end"


@router.get("/stop")
def stop() -> str:
    kill()
    return "end"


def kill():
    global p1, p2
    if p2 is not None:
        p2.kill()
        p2 = None

    if p1 is not None:
        p1.kill()
        p1 = None

    dir_path = "/usr/app/hls"
    if os.path.exists(dir_path):
        # sudo 권한으로 python을 실행시켜야 삭제 가능
        shutil.rmtree(dir_path)

    os.makedirs(dir_path)