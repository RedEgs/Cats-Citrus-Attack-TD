from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys
from PyQt5 import QtCore, QtGui, QtWidgets




class Ui_main_window(object):
    def setup_ui(self, main_window):
        
        if not main_window.objectName():
            main_window.setObjectName(u"main_window")
        main_window.resize(260, 306)
        
        font = QFont()
        font.setPointSize(10)
        font.setUnderline(True)
        
        font1 = QFont()
        font1.setPointSize(13)
        font1.setUnderline(True)
        
        # Cental Widget
        self.centralwidget = QWidget(main_window)
        self.centralwidget.setObjectName(u"centralwidget")
        
        self.new_proj_button = QPushButton(self.centralwidget)
        self.new_proj_button.setObjectName(u"new_proj_button")
        self.new_proj_button.setGeometry(QRect(20, 250, 111, 40))
        self.new_proj_button.clicked.connect(self.choose_directory)
        
        self.open_proj_button = QPushButton(self.centralwidget)
        self.open_proj_button.setObjectName(u"open_proj_button")
        self.open_proj_button.setGeometry(QRect(139, 250, 101, 40))
        
        self.proj_list_view = QListView(self.centralwidget)
        self.proj_list_view.setObjectName(u"proj_list_view")
        self.proj_list_view.setGeometry(QRect(20, 90, 220, 150))
        
        self.subtitle = QLabel(self.centralwidget)
        self.subtitle.setObjectName(u"subtitle")
        self.subtitle.setGeometry(QRect(20, 60, 150, 30))
        self.subtitle.setFont(font)
        



        self.title_label = QLabel(self.centralwidget)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setGeometry(QRect(0, 0, 261, 61))
        self.title_label.setFont(font1)
        self.title_label.setAlignment(Qt.AlignCenter)
        
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(30, 50, 200, 10))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        
        
        main_window.setCentralWidget(self.centralwidget)
        self.retranslateUi(main_window)
        QMetaObject.connectSlotsByName(main_window)
    # setup_ui

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(QCoreApplication.translate("main_window", u"Project Manager", None))
        self.new_proj_button.setText(QCoreApplication.translate("main_window", u"New Project", None))
        self.open_proj_button.setText(QCoreApplication.translate("main_window", u"Open Project", None))
        self.subtitle.setText(QCoreApplication.translate("main_window", u"Existing Projects", None))
        self.title_label.setText(QCoreApplication.translate("main_window", u"Red Engine", None))
    # retranslateUi

    def choose_directory(self):
        dialog = str(QFileDialog.getExistingDirectory(self.centralwidget, "Select Directory"))

    def create_project(self):
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
 
    
    main_window = QtWidgets.QMainWindow()
    ui = Ui_main_window()

    ui.setup_ui(main_window)
    main_window.show()

    sys.exit(app.exec_())