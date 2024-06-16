import sys
import socket
import pickle
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage
from PyQt5.QtCore import Qt, QByteArray, QThread, pyqtSignal
import struct

ip_address = "127.0.0.1"
port = 12345


class ServerThread(QThread):
    update_image_signal = pyqtSignal(bytes, list)

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((ip_address, port))

        current_size = 0
        frame_size = 0
        chunks = []
        while True:
            if current_size == 0:
                pkg_size = struct.calcsize("l")
                buffer, _ = server_socket.recvfrom(pkg_size)
                if buffer:
                    frame_size = struct.unpack("l", buffer)[0]
            packet, _ = server_socket.recvfrom(4096)
            chunks.append(packet)
            current_size += 1
            if current_size == frame_size:
                data = b''.join(chunks)
                current_size = 0
                frame_size = 0
                chunks.clear()
                try:
                    received_data = pickle.loads(data)
                    image_data = received_data['image']
                    draw_points = received_data['draw_points']
                    self.update_image_signal.emit(image_data, draw_points)
                except Exception as e:
                    print(f"Failed to unpack data: {e}")


class ServerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Server')
        self.image_label = None
        self.init_ui()
        self.server_thread = ServerThread()
        self.server_thread.update_image_signal.connect(self.update_image)
        self.server_thread.start()

    def init_ui(self):
        layout = QVBoxLayout()

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        self.setLayout(layout)

    def update_image(self, image_data, draw_points):
        try:
            image = QImage.fromData(QByteArray(image_data))
            if image.isNull():
                print("Failed to load image.")
                return
            pixmap = QPixmap.fromImage(image)

            painter = QPainter(pixmap)
            pen = QPen(Qt.red)
            pen.setWidth(5)
            painter.setPen(pen)
            for point in draw_points:
                painter.drawPoint(point[0], point[1])
            painter.end()

            self.image_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))
        except Exception as e:
            print(f"Failed to update image: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    server = ServerApp()
    server.show()
    sys.exit(app.exec_())
