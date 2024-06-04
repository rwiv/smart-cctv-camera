import os

from cam_server.configs import live_path


def create_m3u8(filenames: list[str]):
    result = "#EXTM3U\n"
    result += "#EXT-X-VERSION:6\n"
    result += "#EXT-X-TARGETDURATION:2\n"
    result += "#EXT-X-MEDIA-SEQUENCE:0\n"
    result += "#EXT-X-INDEPENDENT-SEGMENTS\n"

    for filename in filenames:
        result += "#EXTINF:2,\n"
        result += filename + "\n"

    result += "#EXT-X-ENDLIST"
    return result


def write_m3u8(m3u8_path: str):
    entries = os.listdir(live_path)
    files = [entry for entry in entries if entry.endswith(".ts")]
    files.sort()
    m3u8 = create_m3u8(files)
    with open(m3u8_path, "w") as file:
        file.write(m3u8)

