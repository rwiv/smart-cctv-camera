from datetime import datetime

from cam_server.exec import exec_camera
import time


if __name__ == "__main__":
    now = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    print(now)
    # p1, p2 = exec_camera()
    # time.sleep(20)
    # p2.kill()
    # p1.kill()
