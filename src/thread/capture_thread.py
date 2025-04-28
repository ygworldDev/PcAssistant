
from PyQt5.QtCore import QThread

class CaptureThread(QThread):
    def __init__(self, image_capture):
        QThread.__init__(self)
        self.image_capture = image_capture

    def run(self):
        self.image_capture.capture()