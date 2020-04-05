from PyQt5.QtWidgets import QMainWindow,QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
from log_v import LogV
from trans_vc import TransVC
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("TTS_Window")
        self.setWindowTitle("TTS Window")
        self.resize(1150, 762)
        self.setupUi()
        
    def setupUi(self):
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        
        ## Trans Frame ##
        self.trans_frame = QtWidgets.QFrame(self.centralwidget)
        self.trans_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.trans_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.trans_frame.setObjectName("trans_frame")
        
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        
        self.trans_widget = TransVC()
        self.trans_widget.setObjectName("trans_widget")
        
        self.verticalLayout_2.addWidget(self.trans_widget)
        self.trans_frame.setLayout(self.verticalLayout_2)
        self.gridLayout.addWidget(self.trans_frame, 0, 0, 1, 1)
        
        
        ## TTS Frame ##
        self.tts_frame = QtWidgets.QFrame(self.centralwidget)
        self.tts_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tts_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tts_frame.setObjectName("tts_frame")
        
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tts_frame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        
        self.tts_widget = LogV()
        self.tts_widget.setObjectName("tts_widget")
        
        self.verticalLayout_3.addWidget(self.tts_widget)
        self.tts_frame.setLayout(self.verticalLayout_3)
        self.gridLayout.addWidget(self.tts_frame, 0, 1, 1, 1)
        
        
        ## Log Frame ##
        self.log_frame = QtWidgets.QFrame(self.centralwidget)
        self.log_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.log_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.log_frame.setObjectName("log_frame")
        
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        
        self.log_widget = LogV()
        self.log_widget.setObjectName("log_widget")
        
        self.verticalLayout.addWidget(self.log_widget)
        self.log_frame.setLayout(self.verticalLayout)
        self.gridLayout.addWidget(self.log_frame, 1, 0, 1, 2)
        
        ## Others ##
        # Stuff that i dont know!
        self.gridLayout.setRowStretch(0, 3)
        self.gridLayout.setRowStretch(1, 1)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1150, 20))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFile.menuAction())
        QtCore.QMetaObject.connectSlotsByName(self)
        
        ## Log ##    
        self.init_log()
    
    def init_log(self):
        self.log_widget.log_now()
        
    def onExit(self):
        self.trans_widget.removeDocker()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TTS_MainWindow = MainWindow()
    TTS_MainWindow.show()
    
    TTS_MainWindow.log_widget.log("Hello World!")
    
    sys.exit(app.exec_())
    

