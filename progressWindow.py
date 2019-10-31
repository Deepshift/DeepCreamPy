# window for showing progress while decensoring
# spliting windows by main to check Censor Types, Variations, ect will be better for
# understanding flow of code

import sys
import PySide2
from PySide2.QtWidgets import (QApplication, QMainWindow, QDesktopWidget, QPushButton,
                             QToolTip, QLabel, QProgressBar, QAction, qApp)
# from PyQt5.QtCore import QThread
from signals import Signals
import threading
import time

class ProgressWindow(QMainWindow):
    # debug for setting UI
    def __init__(self, MainWindow, decensor, debug = False):
        super().__init__()
        self.width = 700
        self.height = 500
        self.resize(self.width, self.height)
        self.initUI()

        # signal class that could share update progress ui from decensor class (Decensor)
        self.setSignals()

        self.center()
        self.setWindowTitle("DeepCreamPy v2.2.0    Decensoring...")
        self.show()

        if not debug:
            print("not debug")
            # decensor class initialized with options selected from MainWindow
            self.decensor = decensor
            self.decensor.signals = self.signals

            # to go back to MainWindow after finshed decensoring
            self.mainWindow = MainWindow

            self.runDecensor()


    def initUI(self):
        '''
        Must Todo UI:
        1. add goto decensored file button
        2. Two progress bars
            2-1. total images to decenesor (images in ./decensor_input)
            2-2. current decensoring image's censored area (example marmaid image in DCPv2, 2 / 17)
        3. go back to main button

        Could Do UI:
        1. showing live image decensoring (decensored one by one)
        '''
        # progress bar showing images left to be decensored
        def setProgressBar():
            bar_X = 50
            bar_Y = 300
            bar_width = 600
            bar_height = 30

            # images waiting to be decensored
            self.total_images_ProgressBar = QProgressBar(self)
            # setGeometry(left top x cordinate, left top y cordinate, width, height)
            self.total_images_ProgressBar.setGeometry(bar_X, bar_Y, bar_width,bar_height )
            self.total_images_ProgressBar.setMaximum(100)
            self.total_images_ProgressBar.setValue(0)

            # showing progress of decensored area
            self.signal_image_decensor_ProgressBar = QProgressBar(self)
            self.signal_image_decensor_ProgressBar.setGeometry(bar_X, bar_Y+80, bar_width,bar_height )
            self.signal_image_decensor_ProgressBar.setMaximum(100)
            self.signal_image_decensor_ProgressBar.setValue(0)

        progress_Label_1 = QLabel(self)
        progress_Label_1.move(50, 270)
        progress_Label_1.setText("Decensor progress of all images")
        progress_Label_1.resize(progress_Label_1.sizeHint())

        progress_Label_2 = QLabel(self)
        progress_Label_2.move(50, 300 + 50)
        progress_Label_2.setText("Decensor progress of current image")
        progress_Label_2.resize(progress_Label_2.sizeHint())

        self.progress_status_LABEL = QLabel(self)
        self.progress_status_LABEL.move(100, 100)
        self.progress_status_LABEL.setText("Decensoring...")
        self.progress_status_LABEL.resize(self.progress_status_LABEL.sizeHint())

        setProgressBar()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setSignals(self):
        self.signals = Signals()
        # set signal variable name same as method name preventing confusion
        self.signals.total_ProgressBar_update_MAX_VALUE.connect(self.total_ProgressBar_update_MAX_VALUE)
        self.signals.total_ProgressBar_update_VALUE.connect(self.total_ProgressBar_update_VALUE)
        self.signals.signal_ProgressBar_update_MAX_VALUE.connect(self.signal_ProgressBar_update_MAX_VALUE)
        self.signals.signal_ProgressBar_update_VALUE.connect(self.signal_ProgressBar_update_VALUE)
        self.signals.update_progress_LABEL.connect(self.update_progress_LABEL)

    # total_images_to_decensor_ProgressBar
    def total_ProgressBar_update_MAX_VALUE(self, msg, max):
        # print msg for debugging
        print(msg)
        self.total_images_ProgressBar.setMaximum(max)

    def total_ProgressBar_update_VALUE(self, msg, val):
        # print msg for debugging
        print(msg)
        self.total_images_ProgressBar.setValue(val)

    def signal_ProgressBar_update_MAX_VALUE(self, msg, max):
        # print msg for debugging
        print(msg)
        self.signal_image_decensor_ProgressBar.setMaximum(max)

    def signal_ProgressBar_update_VALUE(self, msg, val):
        # print msg for debugging
        print(msg)
        self.signal_image_decensor_ProgressBar.setValue(val)

    def update_progress_LABEL(self, msg, status):
        print(msg)
        self.progress_status_LABEL.setText(status)
        self.progress_status_LABEL.resize(self.progress_status_LABEL.sizeHint())

    def runDecensor(self):
        # start decensor in other thread, preventing UI Freezing
        # print("start run")
        self.decensor.start()

if __name__ == "__main__":
    # only use for debuging window

    import os
    # you could remove this if statement if there's no error without this
    if os.name == 'nt':
        import PySide2
        pyqt = os.path.dirname(PySide2.__file__)
        QApplication.addLibraryPath(os.path.join(pyqt, "plugins"))
    app = QApplication(sys.argv)
    ex = ProgressWindow(1, 1, debug  = True)
    ex.show()
    sys.exit( app.exec_() )
