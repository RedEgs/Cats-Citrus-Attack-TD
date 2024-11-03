from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(545, 344)
        icon = QIcon()
        icon.addFile(u"../redengine/assets/icons/red-python.png", QSize(), QIcon.Normal, QIcon.Off)
        Form.setWindowIcon(icon)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setTabBarAutoHide(False)
        self.projectstab = QWidget()
        self.projectstab.setObjectName(u"projectstab")
        self.verticalLayout = QVBoxLayout(self.projectstab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.projects_table = QTableWidget(self.projectstab)
        if (self.projects_table.columnCount() < 4):
            self.projects_table.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.projects_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.projects_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.projects_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.projects_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.projects_table.setObjectName(u"projects_table")
        self.projects_table.setAlternatingRowColors(True)
        self.projects_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.projects_table.setShowGrid(False)
        self.projects_table.setGridStyle(Qt.NoPen)
        self.projects_table.setSortingEnabled(False)
        self.projects_table.horizontalHeader().setVisible(True)
        self.projects_table.horizontalHeader().setCascadingSectionResizes(False)
        self.projects_table.horizontalHeader().setDefaultSectionSize(120)
        self.projects_table.verticalHeader().setVisible(False)
        self.projects_table.verticalHeader().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.projects_table)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.look_button = QPushButton(self.projectstab)
        self.look_button.setObjectName(u"look_button")
        self.look_button.setEnabled(False)
        self.look_button.setMinimumSize(QSize(120, 0))
        icon1 = QIcon()
        icon1.addFile(u"../redengine/assets/icons/magnifier.png", QSize(), QIcon.Normal, QIcon.Off)
        self.look_button.setIcon(icon1)

        self.horizontalLayout_2.addWidget(self.look_button)

        self.launch_button = QPushButton(self.projectstab)
        self.launch_button.setObjectName(u"launch_button")
        self.launch_button.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.launch_button.sizePolicy().hasHeightForWidth())
        self.launch_button.setSizePolicy(sizePolicy)
        icon2 = QIcon()
        icon2.addFile(u"../redengine/assets/icons/rocket-fly.png", QSize(), QIcon.Normal, QIcon.Off)
        self.launch_button.setIcon(icon2)
        self.launch_button.setAutoDefault(True)

        self.horizontalLayout_2.addWidget(self.launch_button)

        self.create_button = QPushButton(self.projectstab)
        self.create_button.setObjectName(u"create_button")
        self.create_button.setEnabled(False)
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.create_button.sizePolicy().hasHeightForWidth())
        self.create_button.setSizePolicy(sizePolicy1)
        self.create_button.setMinimumSize(QSize(120, 0))
        self.create_button.setBaseSize(QSize(0, 0))
        icon3 = QIcon()
        icon3.addFile(u"../redengine/assets/icons/folder-horizontal.png", QSize(), QIcon.Normal, QIcon.Off)
        self.create_button.setIcon(icon3)

        self.horizontalLayout_2.addWidget(self.create_button)

        self.delete_button = QPushButton(self.projectstab)
        self.delete_button.setObjectName(u"delete_button")
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.delete_button.sizePolicy().hasHeightForWidth())
        self.delete_button.setSizePolicy(sizePolicy2)
        icon4 = QIcon()
        icon4.addFile(u"../redengine/assets/icons/cross.png", QSize(), QIcon.Normal, QIcon.Off)
        self.delete_button.setIcon(icon4)

        self.horizontalLayout_2.addWidget(self.delete_button)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        icon5 = QIcon()
        icon5.addFile(u"../redengine/assets/icons/folder-open.png", QSize(), QIcon.Normal, QIcon.Off)
        self.tabWidget.addTab(self.projectstab, icon5, "")
        self.settingstab = QWidget()
        self.settingstab.setObjectName(u"settingstab")
        self.verticalLayout_3 = QVBoxLayout(self.settingstab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.option_rich_presence = QRadioButton(self.settingstab)
        self.option_rich_presence.setObjectName(u"option_rich_presence")

        self.verticalLayout_3.addWidget(self.option_rich_presence)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        icon6 = QIcon()
        icon6.addFile(u"../redengine/assets/icons-shadowless/gear.png", QSize(), QIcon.Normal, QIcon.Off)
        self.tabWidget.addTab(self.settingstab, icon6, "")
        self.pythontab = QWidget()
        self.pythontab.setObjectName(u"pythontab")
        self.verticalLayout_2 = QVBoxLayout(self.pythontab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.python_versions_table = QTableWidget(self.pythontab)
        if (self.python_versions_table.columnCount() < 3):
            self.python_versions_table.setColumnCount(3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.python_versions_table.setHorizontalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.python_versions_table.setHorizontalHeaderItem(1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.python_versions_table.setHorizontalHeaderItem(2, __qtablewidgetitem6)
        self.python_versions_table.setObjectName(u"python_versions_table")
        self.python_versions_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.python_versions_table.setShowGrid(False)
        self.python_versions_table.horizontalHeader().setCascadingSectionResizes(False)
        self.python_versions_table.horizontalHeader().setProperty("showSortIndicator", False)
        self.python_versions_table.horizontalHeader().setStretchLastSection(True)
        self.python_versions_table.verticalHeader().setVisible(False)
        self.python_versions_table.verticalHeader().setCascadingSectionResizes(False)
        self.python_versions_table.verticalHeader().setProperty("showSortIndicator", False)
        self.python_versions_table.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_2.addWidget(self.python_versions_table)

        self.install_button = QPushButton(self.pythontab)
        self.install_button.setObjectName(u"install_button")
        icon7 = QIcon()
        icon7.addFile(u"../redengine/assets/icons/download-cloud.png", QSize(), QIcon.Normal, QIcon.Off)
        self.install_button.setIcon(icon7)

        self.verticalLayout_2.addWidget(self.install_button)

        icon8 = QIcon()
        icon8.addFile(u"../redengine/assets/icons-shadowless/application-plus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.tabWidget.addTab(self.pythontab, icon8, "")

        self.horizontalLayout.addWidget(self.tabWidget)


        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(1)
        self.launch_button.setDefault(True)
        self.delete_button.setDefault(False)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"RedEngine Launcher", None))
        ___qtablewidgetitem = self.projects_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"Project", None));
        ___qtablewidgetitem1 = self.projects_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"Version", None));
        ___qtablewidgetitem2 = self.projects_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"Path", None));
        ___qtablewidgetitem3 = self.projects_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"Author", None));
        self.look_button.setText("")
        self.launch_button.setText(QCoreApplication.translate("Form", u"Launch Project", None))
        self.create_button.setText(QCoreApplication.translate("Form", u"Create Project", None))
        self.delete_button.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.projectstab), QCoreApplication.translate("Form", u"Projects", None))
        self.option_rich_presence.setText(QCoreApplication.translate("Form", u"Enable Discord Rich Presence", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settingstab), QCoreApplication.translate("Form", u"Settings", None))
        ___qtablewidgetitem4 = self.python_versions_table.horizontalHeaderItem(0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"Version", None));
        ___qtablewidgetitem5 = self.python_versions_table.horizontalHeaderItem(1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Form", u"Date", None));
        ___qtablewidgetitem6 = self.python_versions_table.horizontalHeaderItem(2)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Form", u"Download Link", None));
        self.install_button.setText(QCoreApplication.translate("Form", u"Install Version", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.pythontab), QCoreApplication.translate("Form", u"Python Installations", None))
    # retranslateUi

