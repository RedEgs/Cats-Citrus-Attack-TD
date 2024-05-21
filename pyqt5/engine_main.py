from PyQt5.QtCore import Qt, QDir
from PyQt5.QtWidgets import QWidget, QMainWindow, QFileDialog, QMessageBox
from engine_design import Ui_main_window

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import os, json

class Pyredengine(QMainWindow):
    def __init__(self, project_json_data = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.project_json_data = project_json_data
        

            
        
        # # Load from project file here
        # self.project_working_path = project_path
        # self.project_json = json.load(open(f"{project_path}/project.json"))
        # self.project_name = self.project_json["project_name"]
        # print(self.project_name)
        # self.project_window_title = f"Red Engine - {self.project_name}"
        
        # self.ide_tabs = []
        
        self.ui = Ui_main_window()
        self.ui.setupUi(self)
        
        if self.project_json_data != None:
            self._load_project(self.project_json_data)
            
            
        self.ui.actionOpen_Project.triggered.connect(self._load_project_from_file)
        self.ui.actionSave_as.triggered.connect(self._save_project_as)
        
        
        
        
    def _relaunch_window(self, data):
        self.close()
        
        self.newWindow = Pyredengine(data)
        self.newWindow.show()
    
    def _load_project(self, data):
        project_json = json.loads(data)
        self.setWindowTitle(QCoreApplication.translate("main_window", u"Red Engine - "+ project_json["project_name"], None))





    def _load_project_file(self, fileName):
        try:
            with open(fileName, 'r') as file:
                data = file.read()
                self._relaunch_window(data)
                
            
                
                QMessageBox.information(self, "File Loaded", f"File {fileName} loaded successfully!", QMessageBox.Ok)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}", QMessageBox.Ok)

    def _load_project_from_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "Open JSON File",
            QDir.homePath(),
            "JSON Files (*.json);;All Files (*)",
            options=options
        )
        if fileName:
            self._load_project_file(fileName)
        else:
            QMessageBox.information(self, "No File Selected", "No file was selected.", QMessageBox.Ok)

    def _load_project_from_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        if folder_path := QFileDialog.getExistingDirectory(
            self, "Select Folder", QDir.homePath(), options=options
        ):
            self.loadFolder(folder_path)
        else:
            QMessageBox.information(self, "No Folder Selected", "No folder was selected.", QMessageBox.Ok)

    def _save_project_as(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Select Folder",
            QDir.homePath(),
            options=options
        )
        if folder_path:
            self.saveToFolder(folder_path)
        else:
            QMessageBox.information(self, "No Folder Selected", "No folder was selected.", QMessageBox.Ok)

    def saveToFolder(self, folder_path):
        try:
            file_path = os.path.join(folder_path, "example.json")
            with open(file_path, 'w') as file:
                file.write('{"example": "This is a test"}')
                self.reopenWindow(folder_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}", QMessageBox.Ok)


    
    def _save_project(self):
        pass
     
    # def _close_ide_tab(self, index):
    #     self.script_tabs.removeTab(index)
        
    #     try: self.ide_tabs.pop(index-2)
    #     except IndexError:pass

    # def _open_in_editor(self, item):
    #     path = get_tree_item_path(self.project_working_path, item).replace("//", "/")
    #     self.resources_tree_dselected_item = [path , item.data(0,0)]

    #     if os.path.isfile(self.resources_tree_dselected_item[0]):
    #         self.ide_index = 0 + 1
    #         new_ide_tab = QIdeTab(self.script_tabs, self.resources_tree_dselected_item, self.ide_index)
    #         text_edit = new_ide_tab.script_edit
    #         self.ide_tabs.append(new_ide_tab)
    #         text_edit.setFocus()
       
            
    # def _select_item_resources_tree(self, item:QTreeWidgetItem):
    #     self.resources_tree_selected_item = self.project_working_path + "/" + item.data(0,0)

    # def _delete_file_resources_tree(self, event):
    #     item = self.resources_tree_selected_item_from_context
    #     path = get_tree_item_path(self.project_working_path, item)

    #     delete_file(self, path)
    #     self.resources_tree_files = reload_project_resources(self.resources_tree_files, self.project_working_path, self.resources_tree)
      
    # def _create_file_resources_tree(self, event):
    #     item = self.resources_tree_selected_item_from_context
    #     path = self.project_working_path
        
    #     if item != None:
    #         if not os.path.isfile(self.project_working_path + f"/{item.data(0, 0)}"):
    #             path = get_tree_item_path(self.project_working_path, item)
                
    #     create_file(main_window, path)
    #     self.resources_tree_files = reload_project_resources(self.resources_tree_files, self.project_working_path, self.resources_tree)
      
    # def _create_folder_resources_tree(self, event):
    #     item = self.resources_tree_selected_item_from_context
    #     path = self.project_working_path
        
    #     print(path)
        
    #     if item != None:
    #         path = get_tree_item_path(self.project_working_path, item) #self.project_working_path + f"/{get_tree_parent_path(item)}" + f"/{item.data(0, 0)}"
    #         self.resources_tree.expandItem(item)
      
        
    #     create_folder(main_window, path)
    #     self.resources_tree_files = reload_project_resources(self.resources_tree_files, self.project_working_path, self.resources_tree)
           
    # def _save_file_in_editor(self):
    #     import PyQt5.QtWidgets
    #     import PyQt5.Qsci

    #     focused = QtWidgets.QApplication.focusWidget()

    #     if focused.__class__ in [
    #         PyQt5.QtWidgets.QPlainTextEdit,
    #         PyQt5.Qsci.QsciScintilla,
    #     ]:
    #         for tab in self.ide_tabs:
    #             tab.save_file()


    #     print(focused.__class__)
           
           
           
           
            
    def create_resources_context_menu(self, event):
        menu = QMenu(self.resources_tree)
        
        menu.addAction(self.actionNew_File)
        menu.addAction(self.actionNew_Folder)
        menu.addAction(self.actionDelete_Resource)
        # copy directory on context menu

        self.resources_tree_selected_item_from_context = self.resources_tree.itemAt(event)


        menu.exec_(self.resources_tree.mapToGlobal(event))
    
    
        
if __name__ == "__main__":
   app = QApplication([])
   widget = Pyredengine()
   widget.show()
   
   app.exec_() 