from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5.QtWidgets import *
from datetime import datetime


class LogV(QWidget):
    def __init__(self, bridge):
        super(QWidget, self).__init__()
        
        self.bridge = bridge
        
        self.log_box = QPlainTextEdit()
        self.log_box.setReadOnly(True)
        
        # font
        font=self.log_box.font()
        font.setFamily("Courier")
        font.setPointSize(10)       
        
        # layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.log_box)
        self.setLayout(self.layout)
        

    def log(self, text):
        text = str(text)
        self.log_box.appendPlainText(text + "\n")
        
    def log_now(self):
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        self.log(dt_string)