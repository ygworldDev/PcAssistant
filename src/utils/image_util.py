import pyautogui
import time
from src.common.constants import CAPTURE_IMAGE_PATH

class ImageCapture:
    def __init__(self):
        pass

    def capture(self):
        print('Screen Capturing...')
        capture_screen = pyautogui.screenshot() 
        capture_screen.save(CAPTURE_IMAGE_PATH)

        return capture_screen

    def release(self):
        self.cap.release()