from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import struct
import sys
import socket
import pickle
import queue
import time

ip_address = "127.0.0.1"
port = 12345
address = (ip_address, port)
image_queue = queue.Queue()
head_queue = queue.Queue()


class ClientThread(QThread):
    def __init__(self):
        super(ClientThread, self).__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.image_path = None
        self.draw_points = None
        self.scale = None

    def set(self, image_path, draw_points, scale):
        self.image_path = image_path
        self.draw_points = draw_points
        self.scale = scale

    def run(self):
        while True:
            time.sleep(0.01)
            if self.image_path is None:
                continue
            if not head_queue.empty():
                head = head_queue.get()
                self.socket.sendto(head, address)
            if not image_queue.empty():
                image = image_queue.get()
                self.socket.sendto(image, address)


class ClientApp(QWidget):
    def __init__(self):
        super().__init__()
        self.image_label = None
        self.upload_button = None
        self.send_button = None
        self.init_ui()
        self.client_thread = ClientThread()
        self.client_thread.start()

        self.draw_points = [(0, 0), (100, 100), (200, 200)]
        self.image_path = None
        self.scale = None

    def init_ui(self):
        self.setWindowTitle('Client')
        self.resize(420, 480)

        layout = QVBoxLayout()

        self.image_label = QLabel(self)
        self.image_label.resize(400, 400)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        self.upload_button = QPushButton('Upload Image', self)
        self.upload_button.clicked.connect(self.upload_image)
        layout.addWidget(self.upload_button)

        self.send_button = QPushButton('Send to Server', self)
        self.send_button.clicked.connect(self.send_to_server)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

    def upload_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.bmp)",
                                                   options=options)
        if file_name:
            # 消除之前标签的图片
            if self.image_path != file_name:
                self.image_label.clear()
            self.image_path = file_name

            # 显示图片
            self.show_image()

    def send_to_server(self):
        # 包装数据
        self.pack_image()

        # 线程传参
        self.client_thread.set(self.image_path, self.draw_points, self.scale)

    def show_image(self):
        # 缩放显示图片
        pixmap = QPixmap(self.image_path)
        pixmap = self.scale_pixmap(pixmap)
        self.image_label.setPixmap(pixmap)

    def scale_pixmap(self, pixmap):
        self.scale = self.calculate_scale_factors(pixmap.width(), pixmap.height(), 400, 400)
        width = int(pixmap.width() * self.scale)
        height = int(pixmap.height() * self.scale)
        scale_pixmap = pixmap.scaled(width, height)
        return scale_pixmap

    @staticmethod
    def calculate_scale_factors(raw_width, raw_height, target_width, target_height):
        width_ratio = target_width / raw_width
        height_ratio = target_height / raw_height
        return min(width_ratio, height_ratio)

    def pack_image(self):
        with open(self.image_path, 'rb') as f:
            image_data = f.read()

        # 缩放坐标点的比例
        draw_points = [(int(x * self.scale), int(y * self.scale)) for x, y in self.draw_points]
        data = {
            'image': image_data,
            'draw_points': draw_points
        }

        serialized_data = pickle.dumps(data)

        chunk_size = 2048 * 2
        chunks = [serialized_data[i:i + chunk_size] for i in range(0, len(serialized_data), chunk_size)]

        head = struct.pack("l", len(chunks))
        head_queue.put(head)
        for chunk in chunks:
            image_queue.put(chunk)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = ClientApp()
    client.show()
    sys.exit(app.exec_())
