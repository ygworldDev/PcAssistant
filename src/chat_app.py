from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextBrowser, QLineEdit, QTextEdit, QComboBox, QCheckBox
from PyQt5.QtGui import QTextCursor, QTextBlockFormat, QColor
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from random import choice
from src.llm.prompt import WELCOME_MESSAGE, SYSTEM_MESSAGE
from src.llm.generator import Generator, Gpt4, Llama3, create_generator
from src.common.constants import LLMType, Role, CAPTURE_IMAGE_PATH
from src.utils.file_util import encode_image
from src.utils.image_util import ImageCapture
from src.thread.generate_thread import GenerateThread
from src.thread.capture_thread import CaptureThread
import time, json, markdown


class ChatApp(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize chat history
        self.chat_history = []
        self.image_capture = ImageCapture()

        # Layout setting
        self.init_layout()

    def init_layout(self):
        self.setWindowTitle("PC Assistant")

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.resize(400, 600)

        ### Top Layout
        self.top_layout = QHBoxLayout()
        self.llm_selection_button = QComboBox()
        self.llm_selection_button.addItem('GPT-4', LLMType.GPT_4)
        self.llm_selection_button.addItem('LLAMA3', LLMType.LLAMA3)
        self.top_layout.addWidget(self.llm_selection_button)

        self.new_session_button = QPushButton('New Session')
        self.new_session_button.setMaximumWidth(150)
        self.new_session_button.clicked.connect(self.new_session)
        self.top_layout.addStretch()
        self.top_layout.addWidget(self.new_session_button)
        self.layout.addLayout(self.top_layout)

        ### Main Layout
        self.chat_log = QTextEdit()
        self.chat_log.setReadOnly(True)
        self.layout.addWidget(self.chat_log)

        ### Bottom Layout
        self.bottom_layout = QHBoxLayout()
        self.message_entry = QLineEdit()
        self.message_entry.setPlaceholderText(' Type your message here...')
        self.message_entry.returnPressed.connect(self.send_message)
        self.bottom_layout.addWidget(self.message_entry)
        
        # Send Button
        self.send_button = QPushButton('Send')
        self.send_button.clicked.connect(self.send_message)
        self.bottom_layout.addWidget(self.send_button)

        self.with_screen = QCheckBox('Screen')
        self.with_screen .setChecked(False)
        self.bottom_layout.addWidget(self.with_screen)
        self.bottom_layout.setSpacing(5)

        # Capture Button
        # self.capture_button = QPushButton('Capture')
        # self.capture_button.clicked.connect(self.capture_image)
        # self.bottom_layout.addWidget(self.capture_button)

        self.layout.addLayout(self.bottom_layout)
        self.new_session()

    def new_session(self):
        self.chat_log.clear()
        self.chat_history.clear()

        self.set_chat_history(Role.SYSTEM, SYSTEM_MESSAGE)
        self.set_chat_history(Role.ASSISTANT, WELCOME_MESSAGE)
        self.chat_log.textCursor().insertText(WELCOME_MESSAGE)


    def send_message(self):
        user_message = self.message_entry.text()
        self.message_entry.clear()
        if user_message:
            cursor = self.chat_log.textCursor()
            cursor.movePosition(QTextCursor.End)

            # User message
            block_format = QTextBlockFormat()
            block_format.setAlignment(Qt.AlignRight)
            block_format.setLeftMargin(50)
            cursor.insertBlock(block_format)
            cursor.insertText(user_message)
            self.chat_log.ensureCursorVisible()
            self.set_chat_history(Role.USER, user_message)

            # Thinking message
            block_format = QTextBlockFormat()
            block_format.setRightMargin(50)
            block_format.setAlignment(Qt.AlignLeft)
            cursor.insertBlock(block_format)
            cursor.insertText("Thinking......")
            self.chat_log.ensureCursorVisible()

            if self.with_screen.isChecked():
                self.capture_image()
            else:
                self.generate_message(image=None)

    def capture_image(self):
        self.hide() # 메신저 창 숨기기 
        self.capture_thread = CaptureThread(self.image_capture)
        self.capture_thread.finished.connect(self.on_capture_finished)
        self.capture_thread.start()

    def on_capture_finished(self):
        self.show() # 메신저 창 나타내기 
        image = encode_image(CAPTURE_IMAGE_PATH) # base64_image
        self.generate_message(image=image)

    def generate_message(self, image: str=None):
            print(f"generate message...")
            llm_type = self.llm_selection_button.currentData()  
            generator = create_generator(llm_type)
            self.thread = GenerateThread(generator, self.chat_history, image)
            self.thread.signal.connect(self.ai_message)
            self.thread.start()     

    def ai_message(self, assistant_message: str=None):
        # 마지막 block 을 삭제 하고 ai message를 update 한다.
        cursor = self.chat_log.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.MoveAnchor)
        cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
        cursor.removeSelectedText()
        html_message = markdown.markdown(assistant_message)
        cursor.insertHtml(html_message)

        self.chat_log.ensureCursorVisible()
        self.set_chat_history(Role.ASSISTANT, assistant_message)
        print(f"chat_history: {self.chat_history}")

    def set_chat_history(self, role:str, message:str):
        history = {"role": role, "content": message}
        self.chat_history.append(history)



    def add_sample_message(self, assistant_message: str=None):
        if assistant_message is None:
            sample_messages = ["Hello! I'm listening.", "How can I assist you?", "I'm here to help.", "What can you tell me?"]
            assistant_message = choice(sample_messages)

        cursor = self.chat_log.textCursor()
        block_format = QTextBlockFormat()
        block_format.setRightMargin(50)
        block_format.setAlignment(Qt.AlignLeft)
        cursor.insertBlock(block_format)
        cursor.insertText(assistant_message)