import subprocess
import platform


def find_command_path(command):
    try:
        if platform.system() == 'Windows':
            result = subprocess.check_output(['where', command], stderr=subprocess.STDOUT)
        else:
            result = subprocess.check_output(['which', command], stderr=subprocess.STDOUT)

        return result.decode('utf-8').strip()
    except subprocess.CalledProcessError:
        return None


def main():
    ffmpeg_path = find_command_path("ffmpeg")
    process = subprocess.Popen(
        [ffmpeg_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        # 시간이 초과되면 프로세스 강제 종료
        process.kill()
        stdout, stderr = process.communicate()
        print(f"Process terminated due to timeout. Output: {stdout}, Error: {stderr}")
    else:
        # 정상적으로 종료된 경우 출력 결과 얻기
        stdout, stderr = process.communicate()
        print(f"Process completed. Output: {stdout}, Error: {stderr}")


def main2():
    # 파이프라인을 사용하여 명령어 실행
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

    p2 = subprocess.Popen([
        'sudo', find_command_path("ffmpeg"),
        '-i', '-', '-vcodec', 'copy', '-g', '60',
        '-preset', 'fast', '-f', 'hls', '-hls_time', '2', '-hls_list_size', '4',
        '-hls_flags', 'delete_segments+append_list+independent_segments',
        '-y', '/usr/app/hls/index.m3u8'
    ], stdin=p1.stdout)

    # p1.wait(timeout=5)
    # p1의 stdout을 닫아 p2가 종료되도록 함
    # p1.stdout.close()


if __name__ == "__main__":
    main2()
