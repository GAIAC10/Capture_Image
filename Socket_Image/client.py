import sys
import socket
import pickle
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import struct

ip_address = "127.0.0.1"
port = 12345


class ClientApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Client')
        self.image_path = ""
        self.draw_points = []
        self.image_label = None
        self.upload_button = None
        self.send_button = None
        self.init_ui()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def init_ui(self):
        layout = QVBoxLayout()

        self.image_label = QLabel(self)
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
            self.image_path = file_name
            pixmap = QPixmap(file_name)
            self.image_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))
            self.draw_points = [(50, 50), (100, 100), (150, 150)]

    def send_to_server(self):
        client_thread = ClientThread(self.image_path, self.draw_points)
        client_thread.send_head_signal.connect(self.send_msg)
        client_thread.send_image_signal.connect(self.send_msg)
        client_thread.start()
        client_thread.wait()

    def send_msg(self, msg):
        self.client_socket.sendto(msg, (ip_address, port))


class ClientThread(QThread):
    send_image_signal = pyqtSignal(bytes)
    send_head_signal = pyqtSignal(bytes)

    def __init__(self, image_path, draw_points):
        super(ClientThread, self).__init__()
        self.image_path = image_path
        self.draw_points = draw_points

    def run(self) -> None:
        if not self.image_path:
            print("No image selected.")
            return

        with open(self.image_path, 'rb') as f:
            image_data = f.read()

        data = {
            'image': image_data,
            'draw_points': self.draw_points
        }

        serialized_data = pickle.dumps(data)

        chunk_size = 4096
        chunks = [serialized_data[i:i + chunk_size] for i in range(0, len(serialized_data), chunk_size)]

        num_chunks = len(chunks)

        pkg_head = struct.pack("l", num_chunks)
        self.send_head_signal.emit(pkg_head)
        for chunk in chunks:
            print(chunk)
            self.send_image_signal.emit(chunk)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = ClientApp()
    client.show()
    sys.exit(app.exec_())
