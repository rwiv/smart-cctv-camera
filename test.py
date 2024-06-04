import os
import re
from datetime import datetime

from cam_server.exec import exec_camera
import time

if __name__ == "__main__":
    # dir_path = os.getcwd()
    # entries = os.listdir(dir_path)
    # files = [entry for entry in entries if os.path.isdir(os.path.join(dir_path, entry))]
    # print(files)

    now = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    print(now)
    # p1, p2 = exec_camera()
    # time.sleep(20)
    # p2.kill()
    # p1.kill()
