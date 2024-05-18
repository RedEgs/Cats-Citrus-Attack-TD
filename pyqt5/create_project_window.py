from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_new_project_dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(240, 120)
        
        font = QFont()
        font.setPointSize(8)
        font1 = QFont()
        font1.setPointSize(10)
        
        Dialog.setFont(font)
        self.project_name_entry = QLineEdit(Dialog)
        self.project_name_entry.setObjectName(u"project_name_entry")
        self.project_name_entry.setGeometry(QRect(110, 40, 113, 22))
        
        self.project_name_label = QLabel(Dialog)
        self.project_name_label.setObjectName(u"project_name_label")
        self.project_name_label.setGeometry(QRect(10, 40, 91, 16))
        
        self.title_label = QLabel(Dialog)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setGeometry(QRect(0, 0, 240, 30))

        
        self.title_label.setFont(font1)
        self.title_label.setFrameShape(QFrame.NoFrame)
        self.title_label.setFrameShadow(QFrame.Raised)
        self.title_label.setAlignment(Qt.AlignCenter)
        
        self.choose_dir_button = QPushButton(Dialog)
        self.choose_dir_button.setObjectName(u"choose_dir_button")
        self.choose_dir_button.setGeometry(QRect(10, 80, 101, 28))
        self.choose_dir_button.clicked.connect(self.choose_directory)

        self.create_proj_button = QPushButton(Dialog)
        self.create_proj_button.setObjectName(u"create_proj_button")
        self.create_proj_button.setGeometry(QRect(120, 80, 111, 28))
        self.create_proj_button.clicked.connect(self.create_project)

        self.chosen_filepath = False

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def choose_directory(self):
        self.filepath = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
        self.chosen_filepath = True


    def create_project(self):
        import json, datetime
        
        if self.chosen_filepath:
            os.mkdir(self.filepath + f"/{self.project_name_entry.text()}")
            
            with open(f"{self.filepath}/{self.project_name_entry.text()}/project.json", "w") as file:
                settings = {
                    "project_name": f"{self.project_name_entry.text()}",
                    "date_created": f"{datetime.date.today()}",
                }    
            
                json.dump(settings, file)
                #file.close()                    
            self.save_previous_project(f"{self.filepath}/{self.project_name_entry.text()}")
            
            os.system(f'python engine_main.py')# Open new file
            sys.exit() # Make sure to open project first
                #print("need to choose a file")
        else:
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setText("Must Select Filepath Before Creating.")
            error_msg.setWindowTitle("No filepath chosen.")
            error_msg.setStandardButtons(QMessageBox.Ok)
            error_msg.exec_()        



    def save_previous_project(self, proj_dir):
        with open(f"recent", "a") as f:
            f.write(f"{proj_dir}\n")    
            f.close()
        
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"New Project", None))
        self.project_name_label.setText(QCoreApplication.translate("Dialog", u"Project Name:", None))
        self.title_label.setText(QCoreApplication.translate("Dialog", u"New Project", None))
        self.choose_dir_button.setText(QCoreApplication.translate("Dialog", u"Choose directory", None))
        self.create_proj_button.setText(QCoreApplication.translate("Dialog", u"Create Project", None))
    # retranslateUi

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
        self.central_widget = QWidget(main_window)
        self.central_widget.setObjectName(u"central_widget")
        
        self.new_proj_button = QPushButton(self.central_widget)
        self.new_proj_button.setObjectName(u"new_proj_button")
        self.new_proj_button.setGeometry(QRect(20, 250, 111, 40))
        self.new_proj_button.clicked.connect(self.new_proj_dialog)
        
        self.open_proj_button = QPushButton(self.central_widget)
        self.open_proj_button.setObjectName(u"open_proj_button")
        self.open_proj_button.setGeometry(QRect(139, 250, 101, 40))
        
        self.proj_list_view = QTreeView(self.central_widget)
        self.proj_list_view.setObjectName(u"proj_list_view")
        self.proj_list_view.setGeometry(QRect(20, 90, 220, 150))
        self.proj_list_view_model = QStandardItemModel(0, 2)
        self.proj_list_view_model.setHorizontalHeaderLabels(["Project Name", "Date Created"])
        self.proj_list_view.setModel(self.proj_list_view_model)

        self.load_previous_projects()
        
        self.subtitle = QLabel(self.central_widget)
        self.subtitle.setObjectName(u"subtitle")
        self.subtitle.setGeometry(QRect(20, 60, 150, 30))
        self.subtitle.setFont(font)
        



        self.title_label = QLabel(self.central_widget)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setGeometry(QRect(0, 0, 261, 61))
        self.title_label.setFont(font1)
        self.title_label.setAlignment(Qt.AlignCenter)
        
        self.line = QFrame(self.central_widget)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(30, 50, 200, 10))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        
        main_window.setCentralWidget(self.central_widget)
        self.retranslateUi(main_window)
        QMetaObject.connectSlotsByName(main_window)
    # setup_ui

                
    def load_previous_projects(self):
        import json 
        
        print("loading")
        with open(f"recent", "r") as f:
            for line in f.readlines():
                
                with open(str(line).strip("\n")+"/project.json", "r") as g:
                    j = json.load(g)
                    item_name = QStandardItem(j["project_name"])
                    item_date = QStandardItem(j["date_created"]) 
                
                    item_name.setData(str(line).strip("\n")+"/project.json", 1)

                    self.proj_list_view_model.appendRow([item_name, item_date])

                    
                    g.close()
            f.close()
                
        selection_model = self.proj_list_view.selectionModel()
        selection_model.selectionChanged.connect(self.set_selection)

    def set_selection(self, selected: QtCore.QItemSelection, deselected):
        self.selected_project_path = selected.indexes()[0].data(1)
        
    def open_project(self):
        pass
        
        #need to implement projectd and shi first
        # try:
        #     os.system(f'python engine_main.py')# Open new file
        # except:
        #     pass

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(QCoreApplication.translate("main_window", u"Project Manager", None))
        self.new_proj_button.setText(QCoreApplication.translate("main_window", u"New Project", None))
        self.open_proj_button.setText(QCoreApplication.translate("main_window", u"Open Project", None))
        self.subtitle.setText(QCoreApplication.translate("main_window", u"Existing Projects", None))
        self.title_label.setText(QCoreApplication.translate("main_window", u"Red Engine", None))
    # retranslateUi

    def new_proj_dialog(self):
        dialog = QtWidgets.QDialog()
        window = Ui_new_project_dialog()
        window.setupUi(dialog)
        dialog.show()    
        dialog.exec()
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
 
    
    main_window = QtWidgets.QMainWindow()
    ui = Ui_main_window()

    ui.setup_ui(main_window)
    main_window.show()

    sys.exit(app.exec_())