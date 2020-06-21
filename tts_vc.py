from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sys

import pygame
pygame.init()
pygame.mixer.init()

sys.path.append("./tts")
from tts.gen_tacotron import TaiwaneseTacotron

class TTSVC(QWidget):
    def __init__(self, bridge):
        super(QWidget, self).__init__()
        
        self.bridge = bridge
        self.bridge.valueUpdated.connect(self.getIPAtext)
        
        self.IPA_text = QtWidgets.QPlainTextEdit()
        self.syns_button = QtWidgets.QPushButton()
        self.syns_button.clicked.connect(self.synsOnClicked)
        
        self.listView = QtWidgets.QListView()
        self.output_dir = "./output"
        
        self.setupFileListView()
        self.setupUi()
        os.chdir("tts")
        self.TTS = TaiwaneseTacotron()
        os.chdir("..")
    def setupFileListView(self):
        self.fileModel = QFileSystemModel()
        self.fileModel.setFilter(QDir.NoDotAndDotDot |  QDir.Files) 
        self.listView.setModel(self.fileModel)
        #self.listView.setRootIndex(self.fileModel.index(self.output_dir))
        self.listView.setRootIndex(self.fileModel.setRootPath(self.output_dir))
        
        self.listView.doubleClicked.connect(self.onListViewClicked)
    
    def onListViewClicked(self):
        selected_model_index = self.listView.selectedIndexes()[0]
        wav_name = self.fileModel.fileName(selected_model_index)
        soundwav = pygame.mixer.Sound("./output/{}".format(wav_name))
        print(wav_name)
        soundwav.play()
        
    def getIPAtext(self):
        self.IPA_text.setPlainText(self.bridge.IPA_text)
        
    def synsOnClicked(self):
        IPA = self.IPA_text.toPlainText()
        華 = self.bridge.華_text
        print(華)
        print(IPA)
        self.TTS.generate(華, IPA)
        
    def setupUi(self):
        self.setObjectName("tts_vc")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setSizePolicy(sizePolicy)
        
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 20, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.IPA_text.sizePolicy().hasHeightForWidth())
        self.IPA_text.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.IPA_text.setFont(font)
        self.IPA_text.setObjectName("IPA_text")
        self.horizontalLayout.addWidget(self.IPA_text)
              
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.syns_button.sizePolicy().hasHeightForWidth())
        self.syns_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.syns_button.setFont(font)
        self.syns_button.setObjectName("syns_button")
        self.horizontalLayout.addWidget(self.syns_button)
        self.horizontalLayout.setStretch(0, 10)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        
        
        self.listView.setObjectName("listView")
        self.verticalLayout_2.addWidget(self.listView)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 2)
        
        
        self.IPA_text.setPlainText("拼音...")
        self.syns_button.setText("合成")
        QtCore.QMetaObject.connectSlotsByName(self)
