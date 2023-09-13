"""采集图片"""

import cv2
import subprocess
import numpy as np
from datetime import datetime

# Loop over frames from the stream 1278/700
HEIGHT = 480
WIDTH = 640
CHANNELS = 3

def open_camera():
    # Open a MJPEG stream from a USB device
    cmd = 'ffmpeg -f v4l2 -input_format mjpeg -i /dev/video0 -filter:v fps=12 -f rawvideo -vf scale=640:480 -pix_fmt bgr24 -'
    # cmd = 'ffmpeg -f v4l2 -input_format mjpeg -i /dev/video4 -r 10 -f rawvideo -vf scale=640:480 -pix_fmt bgr24 -'
    pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    running = True
    while running:
        infrared_frame = pipe.stdout.read(HEIGHT * WIDTH * CHANNELS)
        #pipe.stdout.flush()
        if len(infrared_frame) != HEIGHT * WIDTH * CHANNELS:
            print("Wrong Frame!")
            break

        # 生成文件名
        system_start = datetime.now()
        date_time = str(system_start.year) + '-' + str(system_start.month) + '-' + str(system_start.day) + "-" + system_start.strftime("%H-%M-%S")
        file_name = "./picture/" + "td" + "_" + date_time + ".jpg"
    
        infrared_frame = np.fromstring(infrared_frame, dtype='uint8').reshape((HEIGHT, WIDTH, CHANNELS))
        
        cv2.imshow('infrared_frame', infrared_frame)

        c = cv2.waitKey(1) & 0xff
        if c == 27:
            running = False
        if c == ord('q'):
            running = False
        if c == ord('s'):
            cv2.imwrite('./picture/infrared_frame.jpg', infrared_frame)
            # cv2.imwrite('./picture/external_frame.jpg', external_frame)
            print("save picture\n")
        if c == ord(" "):
            cv2.imwrite(file_name, infrared_frame)
            print("save picture\n")

    # When everything done, release the capture

    pipe.stdout.close()
    # 等待子进程完成任务
    pipe.wait()
    # 正常关闭子进程
    pipe.terminate()
    cv2.destroyAllWindows()
    # local_camera.release()
    # external_camera.release()


if __name__ == "__main__":
    open_camera()
