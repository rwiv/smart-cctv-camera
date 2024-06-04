import subprocess
import platform
from os import path

from cam_server.configs import live_path


def find_command_path(command) -> str | None:
    try:
        if platform.system() == 'Windows':
            result = subprocess.check_output(['where', command], stderr=subprocess.STDOUT)
        else:
            result = subprocess.check_output(['which', command], stderr=subprocess.STDOUT)

        return result.decode('utf-8').strip()
    except subprocess.CalledProcessError:
        return None


def exec_camera() -> tuple[subprocess.Popen[bytes], subprocess.Popen[bytes]]:
    p1 = subprocess.Popen([
        'sudo', find_command_path("libcamera-vid"),
        '-t', '0', '-g', '8', '-n',
        '--bitrate', '8000000', '--inline',
        '--width', '1920', '--height', '1080',
        '--framerate', '30', '--rotation', '180',
        '--shutter', '20000',
        '--gain', '1.5',
        '--codec', 'h264', '-o', '-'
    ], stdout=subprocess.PIPE)

    m3u8_path = path.join(live_path, "index.m3u8")
    p2 = subprocess.Popen([
        'sudo', find_command_path("ffmpeg"),
        '-i', '-', '-vcodec', 'copy', '-g', '60',
        '-preset', 'fast', '-f', 'hls', '-hls_time', '2', '-hls_list_size', '4',
        '-hls_flags', 'append_list+independent_segments',
        '-y', m3u8_path,
    ], stdin=p1.stdout)

    return p1, p2


def write_thumbnail(src: str, dest: str):
    subprocess.run([
        "sudo", find_command_path("ffmpeg"),
        "-i", src, "-ss", "00:00:00.000", "-vframes", "1", dest
    ], stdout=subprocess.PIPE)
