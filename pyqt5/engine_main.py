import importlib

from engine_design import Ui_main_window
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import os, json
import Libs.WidgetsLib as wl

class Pyredengine(QMainWindow):
    def __init__(self, project_json_data = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.project_json_data = project_json_data
        self.project_loaded = False    
        self.project_dir = None    
        

        
        self.ui = Ui_main_window()
        self.ui.setupUi(self)
        
        wl.check_recent_projects()
        
        
        if self.project_json_data != None:
            self._load_project(self.project_json_data)
        else:
            self.save_default_settings()
            
        self._load_menu_bar_actions()
        self._create_recent_projects_context_menu()

    def _load_menu_bar_actions(self):
        self.ui.actionNew_Project.triggered.connect(self._save_project_as)    
        self.ui.actionOpen_Project.triggered.connect(self._load_project_from_folder)
        self.ui.actionSave_as.triggered.connect(self._save_project_as)
        self.ui.actionSave.triggered.connect(self._save_project)
        
        if self.project_loaded:
            self.ui.actionDelete_Resource.triggered.connect(self._delete_file_resources_tree)
            self.ui.actionNew_File.triggered.connect(self._create_file_resources_tree)
            self.ui.actionNew_Folder.triggered.connect(self._create_folder_resources_tree)
            self.ui.actionRename.triggered.connect(self._rename_item_resources_tree)
            
            self.ui.actionSet_as_Main_py.triggered.connect(self.set_main_project_file)
            self.ui.actionGenerate_Script.triggered.connect(self._generate_script_py)
            self.ui.actionGenerate_Main_py.triggered.connect(self._generate_main_py)
            self.ui.actionOpen_in_File_Explorer.triggered.connect(self._open_file_explorer)
            
            
            self.ui.resources_tree.itemClicked.connect(self._select_item_resources_tree)
            self.ui.resources_tree.itemDoubleClicked.connect(self.open_file_in_editor)

            self.ui.actionSave_Layout.triggered.connect(self.save_layout_settings)
            self.ui.actionLoad_Layout.triggered.connect(self.load_layout_settings)
            self.ui.actionRevert_Layout.triggered.connect(self.revert_layout_settings)
            
            self.ui.actionResources.triggered.connect(self.ui.resources_dock.show)     
            self.ui.actionConsole.triggered.connect(self.ui.console_dock.show)
            self.ui.actionAssets_Library.triggered.connect(self.ui.inspector_dock.show)

            self.ui.actionDocumentation.triggered.connect(self._open_online_docs)

            self.ui.start_button.pressed.connect(self._run_game)


       
       
    def _load_shortcuts(self):
        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.activated.connect(self._save_project) 
        
        reload_shortcut = QShortcut(QKeySequence("Ctrl+5"), self)
        reload_shortcut.activated.connect(self._reload_project) 
        
        
    def _relaunch_window(self, data):
        self.close()
        self.newWindow = Pyredengine(data)
        self.newWindow.show()
    
    def _load_project(self, data):
        import Libs.WidgetsLib as wl
        
        project_json = json.loads(data)
        
        # ---
        self.project_loaded = True
        self.project_dir = project_json["project_path"]
        self.project_name = project_json["project_name"]
        self.project_main_file = project_json["main_project_file"]
        self.project_main_file_name = wl.get_file_from_path(self.project_main_file)
        
        wl.add_to_recent_projects(project_json["project_name"], project_json)

        self.ide_tabs = []
        # ---
        self.setWindowTitle(QCoreApplication.translate("main_window", u"Red Engine - "+ project_json["project_name"], None))
        
        self.resources_tree_files = wl.load_project_resources(self.project_dir, self.ui.resources_tree, self.project_main_file_name)
        self.ui.resources_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.resources_tree.customContextMenuRequested.connect(self._create_resources_context_menu)
        self.ui.resource_search_bar.textChanged.connect(lambda: wl.search_tree_view(self.ui.resources_tree, self.ui.resource_search_bar))

        self.load_layout_settings()
        
        self._process_running = False
      
        self.monitor_thread = QThread()
        self.monitor_worker = wl.FileChangeMonitor(self.project_main_file)
        self.monitor_worker.moveToThread(self.monitor_thread)
        self.monitor_thread.started.connect(self.monitor_worker.run)
        self.monitor_worker.file_changed.connect(self.hot_reload_viewport)
        self.monitor_worker.start()
      
      
      
      
      
      
      

    def _load_project_folder(self, folder_path):
        try:
            if os.path.exists(folder_path + "/.redengine"):
                path = folder_path + "/.redengine"
                self._load_project_file(path + "/project.json")
                
            else: 
                QMessageBox.critical(self, "Error", f"Not a valid project directory", QMessageBox.Ok)    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}", QMessageBox.Ok)

    def _load_project_file(self, fileName):
        try:
            print(fileName)
            with open(fileName, 'r') as file:
                data = file.read()
                self._relaunch_window(data)
                
                QMessageBox.information(self, "File Loaded", f"File {fileName} loaded successfully!", QMessageBox.Ok)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}", QMessageBox.Ok)

    def _load_project_from_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        if folder_path := QFileDialog.getExistingDirectory(
            self, "Select Folder", QDir.homePath(), options=options
        ):
            self._load_project_folder(folder_path)
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
            self._prompt_project_name(folder_path)
        else:
            QMessageBox.information(self, "No Folder Selected", "No folder was selected.", QMessageBox.Ok)

    def _prompt_project_name(self, folder_path):
        import Libs.WidgetsLib as wl
                
        project_name, ok = QInputDialog.getText(self, "Project Name", "Enter the project name:")
        if ok and project_name:
            json_path = wl.generate_project_path(self, folder_path, project_name)
            
            if json_path == -1:
                self._load_project_file(folder_path + "/.redengine/project.json")
                
            else:     
                with open(json_path) as file:
                    self._relaunch_window(file.read())
                
                
        else:
            QMessageBox.information(self, "No Project Name", "No project name was provided.", QMessageBox.Ok)

    def _save_project(self):
        if not self.project_loaded:
            self._save_project_as()
        else: 
            for tab in self.ide_tabs:
                tab.save_file()
                
        
        self._reload_file_tree()
            # Implement logic for saving files and shi
       
    def _reload_project(self):
        self._reload_file_tree()
        if self.ui.pygame_widget.can_run:
            self.hot_reload_viewport()
    

       
            
    def save_layout_settings(self):      
        settings = QSettings(self.project_name, "RedEngine")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
        
    def save_default_settings(self):
        settings = QSettings("default", "RedEngine")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
        
    def load_layout_settings(self):
        settings = QSettings(self.project_name, "RedEngine")
        geometry = settings.value("geometry")
        window_state = settings.value("windowState")
        
        if geometry:
            self.restoreGeometry(geometry)
        if window_state:
            self.restoreState(window_state)
        
    def revert_layout_settings(self):
        response = QMessageBox.question(
            self, "Revert to Default", "Are you sure you want to revert to the default layout?",
            QMessageBox.Yes | QMessageBox.No
        )
        if response == QMessageBox.Yes:
            settings = QSettings("default", "RedEngine")
            geometry = settings.value("geometry")
            window_state = settings.value("windowState")
            
            if geometry:
                self.restoreGeometry(geometry)
            if window_state:
                self.restoreState(window_state)
    
    
    
                      
    def open_file_in_editor(self, item):
        import Libs.WidgetsLib as wl
        
        path = wl.get_tree_item_path(self.project_dir, item).replace("//", "/")
        self.resources_tree_dselected_item = [path , item.data(0,0)]


        if os.path.isfile(self.resources_tree_dselected_item[0]):
            self.ide_index =+ 1
            new_ide_tab = wl.QIdeWindow(self.ui.scripting_tab, self.resources_tree_dselected_item, self.ide_index)
            text_edit = new_ide_tab.script_edit
            self.ide_tabs.append(new_ide_tab)

            text_edit.setFocus()
       
    def check_unsaved_tabs(self):
        for tab in self.ide_tabs:
            if tab._saved == False:
                response = QMessageBox.critical(self, f"Theres unsaved progress in {tab._filepath[1]}", f"Your changes will be lost if you don't save them.", QMessageBox.Save |  QMessageBox.Cancel)   
                
                if response == QMessageBox.Save:
                    tab.save_file() 
                else:
                    pass     
      
      
      
      
      
      
      
      
      
    def _select_item_resources_tree(self, item:QTreeWidgetItem):
        self.resources_tree_selected_item = self.project_dir + "/" + item.data(0,0)

    def _rename_item_resources_tree(self, event):
        import Libs.WidgetsLib as wl
        
        item = self.resources_tree_selected_item_from_context
        self._save_project()
        
        if item:
            path = wl.get_tree_item_path(self.project_dir, item)
            cur_name = item.text(0).split(".")
            wl.rename_file(self, self.project_dir, cur_name)
            self._reload_file_tree()

    def _delete_file_resources_tree(self, event):
        import Libs.WidgetsLib as wl
        
        item = self.resources_tree_selected_item_from_context
        
        if item:
            path = wl.get_tree_item_path(self.project_dir, item)

            wl.delete_file(self, path)
            self._reload_file_tree()
        
    def _create_file_resources_tree(self, event=None):
        import Libs.WidgetsLib as wl
                
        item = self.resources_tree_selected_item_from_context
        path = self.project_dir
        
        if item != None:
            if not os.path.isfile(self.project_dir + f"/{item.data(0, 0)}"):
                path = wl.get_tree_item_path(self.project_dir, item)
                
        wl.create_file(self, path)
        self._reload_file_tree()
      
    def _create_folder_resources_tree(self, event):
        import Libs.WidgetsLib as wl
        
        item = self.resources_tree_selected_item_from_context
        path = self.project_dir
        
        if item != None:
            path = wl.get_tree_item_path(self.project_dir, item) #self.project_dir + f"/{get_tree_parent_path(item)}" + f"/{item.data(0, 0)}"
            self.resources_tree.expandItem(item)
      
        
        wl.create_folder(self, self.project_dir)
        self._reload_file_tree()
   
    def _reload_file_tree(self):
        import Libs.WidgetsLib as wl
        
        self.resources_tree_files = wl.reload_project_resources(self.resources_tree_files, self.project_dir, self.ui.resources_tree, self.project_main_file_name)

    def set_main_project_file(self):
        import Libs.WidgetsLib as wl
        
        self.project_main_file = self.resources_tree_selected_item
        
        wl.save_project_json(self, self.project_dir, self.project_name, self.project_main_file)
         
   
    def _generate_main_py(self):
        import Libs.WidgetsLib as wl
                
        item = self.resources_tree_selected_item_from_context
        path = self.project_dir
        
        if item != None:
            if not os.path.isfile(self.project_dir + f"/{item.data(0, 0)}"):
                path = wl.get_tree_item_path(self.project_dir, item)
                
        wl.create_py_file(self, path, "main")
        self._reload_file_tree()   
    
    def _generate_script_py(self):
        import Libs.WidgetsLib as wl
                
        item = self.resources_tree_selected_item_from_context
        path = self.project_dir
        
        if item != None:
            if not os.path.isfile(self.project_dir + f"/{item.data(0, 0)}"):
                path = wl.get_tree_item_path(self.project_dir, item)
                
        wl.create_py_file(self, path)
        self._reload_file_tree()     
        
    def _open_file_explorer(self):
        import Libs.WidgetsLib as wl
        import webbrowser, os
    
        webbrowser.open(os.path.realpath(self.project_dir))       
   
   
   
    def _run_game(self):
        import Libs.WidgetsLib as wl
        
        
        if self.project_main_file != None:
            if not self.ui.pygame_widget.can_run:
                import sys  

                sys.path.insert(0, self.project_dir)
                import main
                
                game = main.MainGame()
                
                self.ui.pygame_widget.set_process(game.run_game(), game, self.project_main_file)
                self.ui.start_button.setText("Stop")
            else:
                
                self.ui.pygame_widget.close_process()
                
                self.ui.start_button.setText("Start")
      
    def hot_reload_viewport(self):
        if self.project_main_file != None:
            if self.ui.pygame_widget.can_run:
                import sys 
                sys.path.insert(0, self.project_dir)
                import main

                self.ui.pygame_widget.save_process_state()

                
                importlib.reload(main)

                game = main.MainGame()

                self.ui.pygame_widget.close_process()
                
                self.ui.pygame_widget.set_process(game.run_game(), game, self.project_main_file)
                self.ui.pygame_widget.load_process_state()
   
   
   
   
   
   
   
   
    def _open_online_docs(self):
        import Libs.WidgetsLib as wl
        
        self.window = wl.Browser()
        self.window.exec_()
    
        
        
      
        
        
        
        
        
        
        
   
           
    def _create_resources_context_menu(self, event):
        menu = QMenu(self.ui.resources_tree)
        
        
        
        self.resources_tree_selected_item_from_context = self.ui.resources_tree.itemAt(event)
        item = self.resources_tree_selected_item_from_context
        
        if item:
            try:
                if item.text(0).split(".")[1] == "py":
                    menu.addAction(self.ui.actionSet_as_Main_py)
            except: pass
               
                
            menu.addAction(self.ui.actionDelete_Resource)
            menu.addAction(self.ui.actionRename)
            #menu.addAction(self.ui.acren)
        else:
            menu.addAction(self.ui.actionGenerate_Main_py)
            menu.addAction(self.ui.actionGenerate_Script)
            menu.addSeparator()
            menu.addAction(self.ui.actionNew_File)
            menu.addAction(self.ui.actionNew_Folder)
            menu.addSeparator()
            menu.addAction(self.ui.actionOpen_in_File_Explorer)

        # copy directory on context menu

        menu.exec_(self.ui.resources_tree.mapToGlobal(event))
    
    def _create_recent_projects_context_menu(self):
        import Libs.WidgetsLib as wl
        import json
        
        r_projs = wl.load_recent_projects_from_json()
        for project_name, project_details in r_projs.items():
            action = self.ui.menuRecent_Projects.addAction(project_name)
            
            proj_json = project_details["json"]
            action.triggered.connect(lambda: self._load_project_folder(proj_json["project_path"]))
        
    def closeEvent(self, event):
        if self.project_loaded:
            self.save_layout_settings()
            self.check_unsaved_tabs()
            
            
            
        super().closeEvent(event)
        
if __name__ == "__main__":
   app = QApplication([])
   widget = Pyredengine()
   widget.show()
   
   app.exec_() 