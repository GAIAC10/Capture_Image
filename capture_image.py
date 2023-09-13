import sys
import cv2
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QDesktopWidget, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QDir, QTimer
from mywiget import Ui_Form
from PyCameraList.camera_device import list_video_devices, test_list_cameras, list_audio_devices
import datetime


class MyWin(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.cameras_index = {}
        self.setupUi(self)
        self.save_path = None
        self.image = None
        self.cap = None
        self.cap_status = False
        self.index = 0
        self.frame_count = 0
        self.image_name = 0
        self.count_cameras()
        self.curr_time = datetime.datetime.now()
        items = []
        for i in range(len(self.cameras_index)):
            items.append("摄像头" + str(i + 1) + " : " + self.cameras_index[i])
        self.select_box.addItems(items)
        self.my_timer = QTimer()
        self.my_timer.timeout.connect(self.cap_image)
        self.select_box.currentIndexChanged.connect(self.select_index)
        self.begin_btn.clicked.connect(self.begin_fun)
        self.pause_btn.clicked.connect(self.pause_fun)
        self.exit_btn.clicked.connect(self.exit_fun)
        self.save_btn.clicked.connect(self.save_path_fun)
        if len(self.cameras_index) != 0:
            self.msg_browser.append("选择摄像头1")
        else:
            self.msg_browser.append("没有摄像头")

    def select_index(self, i):
        self.index = i
        self.msg_browser.append("选择摄像头{}".format(self.index + 1))

    def count_cameras(self):
        cameras = dict(list_video_devices())
        self.cameras_index = cameras

    def begin_fun(self):
        if not self.save_path:
            self.critical()
        else:
            self.msg_browser.append("开启摄像头")
            # todo
            if not self.cap_status:
                self.cap_status = True
            if self.cap_status:
                self.my_timer.start(1)
                self.cap = cv2.VideoCapture(self.index)

    def pause_fun(self):
        if not self.save_path:
            self.critical()
        else:
            self.msg_browser.append("关闭摄像头")
            if self.cap_status:
                self.cap_status = False
            if not self.cap_status:
                self.cv_label.clear()
                text = "<html>" \
                       "<head/>" \
                       "<body>" \
                       "<p align='center'>" \
                       "<span style=' font-size:18pt; font-weight:600;'>" \
                       "摄像头" \
                       "</span>" \
                       "</p>" \
                       "</body>" \
                       "</html>"
                self.cv_label.setText(text)
                self.my_timer.stop()
                self.cap.release()

    def exit_fun(self):
        self.msg_browser.append("退出")
        window = QApplication.instance()
        window.quit()

    def save_path_fun(self):
        self.save_path = QFileDialog.getExistingDirectory(self, "选择保存文件夹", QDir.currentPath())
        if not self.save_path:
            self.critical()
        else:
            self.msg_browser.append("选择保存文件夹:{}".format(self.save_path))

    def critical(self):
        QMessageBox.warning(self, "警告", "请选择文件夹", QMessageBox.Ok)

    def cap_image(self):
        if self.cap:
            self.frame_count += 1
            ret, self.image = self.cap.read()
            image = cv2.resize(self.image, (780, 580))
            if self.frame_count % 10 == 0:
                self.image_name += 1
                date_str = str(self.curr_time.year)+"-"+str(self.curr_time.month)+"-"+str(self.curr_time.day)+"-"+ \
                           str(self.curr_time.hour)+"-"+str(self.curr_time.minute)+"-"+str(self.curr_time.second)
                save_path = self.save_path + "/" + date_str + "_" + str(self.image_name) + ".jpg"
                cv2.imwrite(save_path, image)
                self.msg_browser.append("{}保存成功".format(save_path))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            showImage = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
            self.cv_label.setPixmap(QPixmap.fromImage(showImage))

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        NewLeft = int((screen.width() - size.width()) / 2)
        NewTop = int((screen.height() - size.height()) / 2)
        self.move(NewLeft, NewTop)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyWin()
    w.center()
    w.show()
    sys.exit(app.exec_())
