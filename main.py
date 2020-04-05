import sys
from PyQt5 import QtWidgets
from main_window import MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    TTS_MainWindow = MainWindow()
    TTS_MainWindow.show()
    ##TODO
    ## kill docker when killing python kernel
    try:
        sys.exit(app.exec_())
    except:
        TTS_MainWindow.onExit()