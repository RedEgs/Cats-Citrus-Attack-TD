# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designdjeesM.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from redegswidgets import PygameWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.start_button = QPushButton(self.centralwidget)
        self.start_button.setObjectName(u"start_button")

        self.horizontalLayout.addWidget(self.start_button)

        self.stop_button = QPushButton(self.centralwidget)
        self.stop_button.setObjectName(u"stop_button")

        self.horizontalLayout.addWidget(self.stop_button)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_frame = QFrame(self.centralwidget)
        self.widget_frame.setObjectName(u"widget_frame")
        self.widget_frame.setFrameShape(QFrame.StyledPanel)
        self.widget_frame.setFrameShadow(QFrame.Plain)
        self.verticalLayout_3 = QVBoxLayout(self.widget_frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.pygame_widget = PygameWidget(parent=self.widget_frame)
        self.pygame_widget.setObjectName(u"pygame_widget")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pygame_widget.sizePolicy().hasHeightForWidth())
        self.pygame_widget.setSizePolicy(sizePolicy)
        self.pygame_widget.setMinimumSize(QSize(760, 550))

        self.verticalLayout_3.addWidget(self.pygame_widget)


        self.verticalLayout.addWidget(self.widget_frame)


        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)

        #MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.start_button.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.stop_button.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
    # retranslateUi
