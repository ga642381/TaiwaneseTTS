import os
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.斷詞.國教院斷詞用戶端 import 國教院斷詞用戶端
from 臺灣言語工具.翻譯.摩西工具.摩西服務端 import 摩西服務端
from 臺灣言語工具.翻譯.摩西工具.摩西用戶端 import 摩西用戶端
from 臺灣言語工具.翻譯.摩西工具.語句編碼器 import 語句編碼器
from 臺灣言語工具.語音合成 import 台灣話口語講法
import sys
sys.path.append("./translation")
from translation.train import Inference

class TransVC(QWidget):
    def __init__(self, bridge):
        super(QWidget, self).__init__()
        
        self.bridge = bridge
        
        _id = QtGui.QFontDatabase.addApplicationFont("NotoSans/NotoSansCJKtc-Light.otf")
        font = QtGui.QFont("NotoSans")

        self.Chinese_text = QtWidgets.QPlainTextEdit()
        self.Chinese_text.setFont(font)
        self.trans_button = QtWidgets.QPushButton()
        self.trans_button.clicked.connect(self.transOnClicked)
        self.Deep_台羅 = QtWidgets.QLineEdit()
        self.Deep_IPA = QtWidgets.QLineEdit()
        self.摩西_台羅 = QtWidgets.QLineEdit()
        self.摩西_IPA = QtWidgets.QLineEdit()        
        
        self.setupUi()
        self.setupDocker()
        
        os.chdir("translation")
        self.Seq2Seq = Inference()
        os.chdir("..")
        
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
    
    def translate_deep(self, text):
        拼音 = self.Seq2Seq.predict(text)
        句物件 = 拆文分析器.建立句物件(拼音, 拼音)
        口語講法 = 台灣話口語講法(句物件)
        return 拼音, 口語講法
    
    def translate(self, text):
        華語句物件 = 拆文分析器.建立句物件(text)
        華語斷詞句物件 = 國教院斷詞用戶端.斷詞(華語句物件)
        台語句物件, self.華語新結構句物件, 分數 = (摩西用戶端(位址='localhost', 編碼器=語句編碼器).翻譯分析(華語斷詞句物件))
        口語講法 = 台灣話口語講法(台語句物件)
        
        return 華語斷詞句物件, 台語句物件, 口語講法
    
    
    def transOnClicked(self):
        # translate
        Chinese_text = self.Chinese_text.toPlainText()
        self.華語斷詞句物件, self.台語句物件, self.口語講法 = self.translate(Chinese_text)
        self.台語Seq2Seq, self.台語IPA = self.translate_deep(Chinese_text)
        # setText
        # self.Deep_台羅.setText(self.華語斷詞句物件.看分詞())
        #print(self.台語Seq2Seq)
        self.Deep_台羅.setText(self.台語Seq2Seq)
        self.Deep_IPA.setText(self.台語IPA)
        
        self.摩西_台羅.setText(self.台語句物件.看音())
        self.摩西_IPA.setText(self.口語講法)
        
        self.bridge.sendSignal(Chinese_text, self.Deep_IPA.text())
        
        
    def setupUi(self):
        self.setObjectName("trans_vc")
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
        sizePolicy.setHeightForWidth(self.Deep_台羅.sizePolicy().hasHeightForWidth())
        self.Deep_台羅.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Deep_台羅.setFont(font)
        self.Deep_台羅.setObjectName("text_1")
        self.horizontalLayout_2.addWidget(self.Deep_台羅)
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
        sizePolicy.setHeightForWidth(self.Deep_IPA.sizePolicy().hasHeightForWidth())
        self.Deep_IPA.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Deep_IPA.setFont(font)
        self.Deep_IPA.setObjectName("text_2")
        self.horizontalLayout_3.addWidget(self.Deep_IPA)
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
        sizePolicy.setHeightForWidth(self.摩西_台羅.sizePolicy().hasHeightForWidth())
        self.摩西_台羅.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.摩西_台羅.setFont(font)
        self.摩西_台羅.setObjectName("text_3")
        self.horizontalLayout_4.addWidget(self.摩西_台羅)
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
        
        self.摩西_IPA.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.摩西_IPA.sizePolicy().hasHeightForWidth())
        self.摩西_IPA.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.摩西_IPA.setFont(font)
        self.摩西_IPA.setObjectName("IPA_text")
        self.horizontalLayout_5.addWidget(self.摩西_IPA)
        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 10)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 2)

        self.Chinese_text.setPlainText("最近肺炎很嚴重，記得戴口罩，常洗手。有病就要看醫生。")
        self.trans_button.setText("翻譯")
        self.label_1.setText("Seq")
        self.label_2.setText("IPA")
        self.label_3.setText("摩西")
        self.IPA_label.setText("IPA")
        
        QtCore.QMetaObject.connectSlotsByName(self)

