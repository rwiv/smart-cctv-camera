import asyncio
import os
import stat
import subprocess
from datetime import datetime
from os import path

from fastapi import APIRouter, Query, HTTPException

from cam_server.configs import hls_path, live_path
from cam_server.exec import exec_camera, write_thumbnail
from cam_server.hls import write_m3u8

router = APIRouter()

p1: subprocess.Popen[bytes] | None = None
p2: subprocess.Popen[bytes] | None = None


async def delay_kill(delay: int):
    await asyncio.sleep(delay)
    kill()


@router.get("/")
def index() -> str:
    return "hello"


@router.get("/records")
def records() -> list[str]:
    entries = os.listdir(hls_path)
    files = [entry for entry in entries if os.path.isdir(path.join(hls_path, entry))]
    return files


@router.get("/start")
async def start(t: int = Query(20)) -> str:
    # sudo 권한 필요
    os.makedirs(live_path, exist_ok=True)
    os.chmod(live_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

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

    # sudo 권한 필요
    if os.path.exists(live_path):
        m3u8_path = path.join(live_path, "index.m3u8")
        os.remove(m3u8_path)
        write_m3u8(m3u8_path)

        src_path = path.join(live_path, "index0.ts")
        dest_path = path.join(live_path, "thumb.jpg")
        write_thumbnail(src_path, dest_path)

        now = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        os.rename(live_path, path.join(hls_path, now))
