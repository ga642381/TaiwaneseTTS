from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.斷詞.國教院斷詞用戶端 import 國教院斷詞用戶端
from 臺灣言語工具.翻譯.摩西工具.摩西服務端 import 摩西服務端
from 臺灣言語工具.翻譯.摩西工具.摩西用戶端 import 摩西用戶端
from 臺灣言語工具.翻譯.摩西工具.語句編碼器 import 語句編碼器
from 臺灣言語工具.語音合成 import 台灣話口語講法

class TransVC(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.Chinese_text = QtWidgets.QPlainTextEdit()
        self.trans_button = QtWidgets.QPushButton()
        self.trans_button.clicked.connect(self.trans_button_onclicked)
        self.text_1 = QtWidgets.QLineEdit()
        self.text_2 = QtWidgets.QLineEdit()
        self.text_3 = QtWidgets.QLineEdit()
        self.IPA_text = QtWidgets.QLineEdit()        
        
        self.setupUi()
        self.setupDocker()
        
    def setupDocker(self):
        #TODO log
        '''
        cmd = "docker run --name huatai -p 8080:8080 -d --rm i3thuan5/hokbu-le:huatai"
        '''
        import docker
        self.client = docker.from_env()
        if not (self.client.containers.list(filters={"name":"huatai"})):
            self.client.containers.run("i3thuan5/hokbu-le:huatai", 
                                  name="huatai",
                                  ports={'8080/tcp': 8080},
                                  detach=True,
                                  auto_remove=True)
        
    def removeDocker(self):
        self.client.containers.get("huatai").stop()
        
    def trans_button_onclicked(self):
        Chinese_text = self.Chinese_text.toPlainText()
        print(Chinese_text)
        self.華語句物件 = 拆文分析器.建立句物件(Chinese_text)
        # send the text to 
        self.華語斷詞句物件 = 國教院斷詞用戶端.斷詞(self.華語句物件)
        self.text_1.setText(self.華語斷詞句物件.看分詞())
        # send the text to docker "huatai"
        self.台語句物件, self.華語新結構句物件, 分數 = (摩西用戶端(位址='localhost', 編碼器=語句編碼器).翻譯分析(self.華語斷詞句物件))
        self.text_2.setText(self.台語句物件.看型())
        self.text_3.setText(self.台語句物件.看音())
        self.口語講法 = 台灣話口語講法(self.台語句物件)
        self.IPA_text.setText(self.口語講法)
        
        
    def setupUi(self):
        self.setObjectName("trans_vc")
        self.setObjectName("widget")
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
        sizePolicy.setHeightForWidth(self.Chinese_text.sizePolicy().hasHeightForWidth())
        self.Chinese_text.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Chinese_text.setFont(font)
        self.Chinese_text.setObjectName("Chinese_text")
        self.horizontalLayout.addWidget(self.Chinese_text)
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trans_button.sizePolicy().hasHeightForWidth())
        self.trans_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.trans_button.setFont(font)
        self.trans_button.setObjectName("trans_button")
        self.horizontalLayout.addWidget(self.trans_button)
        self.horizontalLayout.setStretch(0, 10)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 10, -1, 10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_1 = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_1.setFont(font)
        self.label_1.setObjectName("label_1")
        self.horizontalLayout_2.addWidget(self.label_1)
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_1.sizePolicy().hasHeightForWidth())
        self.text_1.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.text_1.setFont(font)
        self.text_1.setObjectName("text_1")
        self.horizontalLayout_2.addWidget(self.text_1)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 10)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, 10, -1, 10)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_2.sizePolicy().hasHeightForWidth())
        self.text_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.text_2.setFont(font)
        self.text_2.setObjectName("text_2")
        self.horizontalLayout_3.addWidget(self.text_2)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 10)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, 10, -1, 10)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_3.sizePolicy().hasHeightForWidth())
        self.text_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.text_3.setFont(font)
        self.text_3.setObjectName("text_3")
        self.horizontalLayout_4.addWidget(self.text_3)
        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 10)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, 10, -1, 10)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.IPA_label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.IPA_label.setFont(font)
        self.IPA_label.setObjectName("IPA_label")
        self.horizontalLayout_5.addWidget(self.IPA_label)
        
        self.IPA_text.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.IPA_text.sizePolicy().hasHeightForWidth())
        self.IPA_text.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.IPA_text.setFont(font)
        self.IPA_text.setObjectName("IPA_text")
        self.horizontalLayout_5.addWidget(self.IPA_text)
        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 10)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 2)
        
        
        self.Chinese_text.setPlainText("今天天氣好嗎\n")
        self.trans_button.setText("翻譯")
        self.label_1.setText("斷詞")
        self.label_2.setText("臺語")
        self.label_3.setText("拼音")
        self.IPA_label.setText("IPA")
        
        QtCore.QMetaObject.connectSlotsByName(self)

