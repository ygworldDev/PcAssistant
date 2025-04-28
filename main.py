from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextBrowser, QLineEdit, QTextEdit
from PyQt5.QtGui import QTextCursor, QTextBlockFormat
from PyQt5.QtCore import Qt
from random import choice

from PyQt5.QtWidgets import QApplication
from src.chat_app import ChatApp

app = QApplication([])
window = ChatApp()
window.show()
app.exec_()