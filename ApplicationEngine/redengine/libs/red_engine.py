import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qsci import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
import libs.widgets as w

class Browser(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('GitHub Page')
        self.setGeometry(100, 100, 1024, 768)

        layout = QVBoxLayout()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://github.com/RedEgs"))
        layout.addWidget(self.browser)

        self.setLayout(layout)
   
   
class ConsoleLog(QObject):
    console_log = pyqtSignal(str)
    
    
class ConsoleWrapper():
 
    def __init__(self, main):
        self.main = main
        self.signal = ConsoleLog()


    def write(self, text):
        if text != "\n":
            self.signal.console_log.emit(text)
            
    def flush(self):
        pass


