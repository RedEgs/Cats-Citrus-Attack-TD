from engine_design import Ui_main_window
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

import os, json, sys, importlib, platform, traceback


class Pyredengine(QMainWindow):
    def __init__(self, project_json_data = None, *args, **kwargs) -> None:
        import libs.project_management as pm
        import libs.widgets as w
        import libs.compiler as cmp
        
        super().__init__(*args, **kwargs)
        self.project_json_data = project_json_data
        self.project_loaded = False    
        self.project_dir = None    
        

        
        self.ui = Ui_main_window()
        self.ui.setupUi(self)
        
        pm.check_recent_projects()
        
        self._support_message()
        if self.project_json_data != None:
            self._load_project(self.project_json_data)   
            
            
        
    
        else:
            self.save_default_settings()
        
        self._load_menu_bar_actions()
        self._create_recent_projects_context_menu()

    def _load_menu_bar_actions(self):
        import libs.project_management as pm
        
        self.ui.actionNew_Project.triggered.connect(self._save_project_as)    
        self.ui.actionOpen_Project.triggered.connect(self._load_project_from_folder)
        self.ui.actionSave_as.triggered.connect(self._save_project_as)
        self.ui.actionSave.triggered.connect(self._save_project)
        self.ui.actionClear_All_Recent_Projects.triggered.connect(self._clear_recent_projects)
        
        if self.project_loaded:
            self.ui.actionDelete_Resource.triggered.connect(self._delete_file_resources_tree)
            self.ui.actionNew_File.triggered.connect(self._create_file_resources_tree)
            self.ui.actionNew_Folder.triggered.connect(self._create_folder_resources_tree)
            self.ui.actionRename.triggered.connect(self._rename_item_resources_tree)
            
            self.ui.actionSet_as_Main_py.triggered.connect(self.set_main_project_file)
            self.ui.actionSet_as_Main_Scenes.triggered.connect(self.set_scenes_dir)
            self.ui.actionGenerate_Script.triggered.connect(self._generate_script_py)
            self.ui.actionGenerate_Main_py.triggered.connect(self._generate_main_py)
            self.ui.actionOpen_in_File_Explorer.triggered.connect(self._open_file_explorer)
            self.ui.actionReload.triggered.connect(self._reload_project)
            
            self.ui.resources_tree.itemClicked.connect(self._select_item_resources_tree)
            self.ui.resources_tree.itemDoubleClicked.connect(self.open_file_in_editor)

            self.ui.actionSave_Layout.triggered.connect(self.save_layout_settings)
            self.ui.actionLoad_Layout.triggered.connect(self.load_layout_settings)
            self.ui.actionRevert_Layout.triggered.connect(self.revert_layout_settings)
            
            self.ui.actionResources.triggered.connect(self.ui.resources_dock.show)     
            self.ui.actionConsole.triggered.connect(self.ui.console_dock.show)
            self.ui.actionAssets_Library.triggered.connect(self.ui.debug_menu_dock.show)

            self.ui.actionCompile_Project.triggered.connect(self._compile_game)

            self.ui.actionDocumentation.triggered.connect(self._open_online_docs)

            self.ui.start_button.pressed.connect(self._run_game)
            
            self.ui.clearLogBtn.pressed.connect(self._clear_log)
 
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
        import libs.project_management as pm
        import libs.resource_management as rm
        import libs.widgets as w
        import libs.red_engine as red_engine
        
        project_json = json.loads(data)
        
        # ---
        self.project_loaded = True
        self.project_dir = project_json["project_path"]
        self.project_name = project_json["project_name"]
        self.project_main_file = project_json["main_project_file"]
        self.project_main_file_name = rm.get_file_from_path(self.project_main_file)

        self.project_scenes_dir = project_json["project_scenes"]

        
        pm.add_to_recent_projects(project_json["project_name"], project_json)

        self.ide_tabs = []
        # ---
        self.setWindowTitle(QCoreApplication.translate("main_window", u"Red Engine - "+ project_json["project_name"], None))
        
        self.resources_tree_files = w.load_project_resources(self.project_dir, self.ui.resources_tree, self.project_main_file_name, self.project_scenes_dir)
        self.ui.resources_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.resources_tree.customContextMenuRequested.connect(self._create_resources_context_menu)
        self.ui.resource_search_bar.textChanged.connect(lambda: w.search_tree_view(self.ui.resources_tree, self.ui.resource_search_bar))

        self.load_layout_settings()

        self._process_running = False
      
        self.monitor_thread = QThread()
        self.monitor_worker = rm.FileChangeMonitor(self.project_main_file, self.project_dir, self.project_scenes_dir)
        self.monitor_worker.moveToThread(self.monitor_thread)
        self.monitor_thread.started.connect(self.monitor_worker.run)
        self.monitor_worker.file_changed.connect(self.hot_reload_viewport)
        self.monitor_worker.start()
      
        self.console_output_stream = red_engine.ConsoleWrapper(self)
        #sys.stderr = self.console_output_stream
        #sys.stdout = self.console_output_stream  
      
        #self.console_output_stream.signal.console_log.connect(self._print_to_log)

      
      

    def _load_project_folder(self, folder_path):
        try:
            if os.path.exists(f"{folder_path}/.redengine"):
                path = f"{folder_path}/.redengine"
                self._load_project_file(f"{path}/project.json")

            else: # Add the option to create project here
                response = QMessageBox.critical(
                    self,
                    f"Not valid project directory",
                    "Not a valid project, would you like to make it one instead?",
                    QMessageBox.Save | QMessageBox.Discard,
                )   

                if response:
                    self._prompt_project_name(folder_path)



        except (Exception, Exception) as e:
            print(f"failed to load folder {e}")
            QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}", QMessageBox.Ok)

    def _load_project_file(self, fileName):
        try:
            print(fileName)
            with open(fileName, 'r') as file:
                data = file.read()
                self._relaunch_window(data)
                
                QMessageBox.information(self, "File Loaded", f"File {fileName} loaded successfully!", QMessageBox.Ok)
        except Exception as e:
            print(f"failed to load file, {e}")
            print(fileName)
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
        if folder_path := QFileDialog.getExistingDirectory(
            self, "Select Folder", QDir.homePath(), options=options
        ):
            self._prompt_project_name(folder_path)
        else:
           QMessageBox.information(self, "No Folder Selected", "No folder was selected.", QMessageBox.Ok)

    def _save_project_as_nodialog(self, folder_path):
        self.prompt_project_name(folder_path)

    def _prompt_project_name(self, folder_path):
        import libs.project_management as pm

        project_name, ok = QInputDialog.getText(self, "Project Name", "Enter the project name:")
        if ok and project_name:
            json_path = pm.generate_project_path(self, folder_path, project_name)

            if json_path == -1:
                self._load_project_file(f"{folder_path}/.redengine/project.json")

            else:     
                with open(json_path) as file:
                    self._relaunch_window(file.read())


        else:
            QMessageBox.information(self, "No Project Name", "No project name was   provided.", QMessageBox.Ok)


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
        self.hot_reload_viewport()


       
    def _clear_recent_projects(self):
        import libs.project_management as pm
        
        pm.clear_recent_projects()
        self._create_recent_projects_context_menu()
            
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
        import libs.widgets as w
        
        path = w.get_tree_item_path(self.project_dir, item).replace("//", "/")
        self.resources_tree_dselected_item = [path , item.data(0,0)]


        if os.path.isfile(self.resources_tree_dselected_item[0]):
            self.ide_index =+ 1
            new_ide_tab = w.QIdeWindow(self.ui.scripting_tab, self.resources_tree_dselected_item, self.ide_index)
            text_edit = new_ide_tab.script_edit
            self.ide_tabs.append(new_ide_tab)

            text_edit.setFocus()
       
    def check_unsaved_tabs(self):
        for tab in self.ide_tabs:
            if tab._saved == False:
                response = QMessageBox.critical(
                    self,
                    f"Theres unsaved progress in {tab._filepath[1]}",
                    "Your changes will be lost if you don't save them.",
                    QMessageBox.Save | QMessageBox.Cancel,
                )   

                if response == QMessageBox.Save:
                    tab.save_file()     
      
      
      
      
      
      
      
      
      
    def _select_item_resources_tree(self, item:QTreeWidgetItem):
        self.resources_tree_selected_item = f"{self.project_dir}/{item.data(0, 0)}"

    def _rename_item_resources_tree(self, event):
        import libs.widgets as w
        import libs.resource_management as rm
        
        item = self.resources_tree_selected_item_from_context
        self._save_project()
        
        if item:
            path = w.get_tree_item_path(self.project_dir, item)
            cur_name = item.text(0).split(".")
            rm.rename_file(self, self.project_dir, cur_name)
            self._reload_file_tree()

    def _delete_file_resources_tree(self, event):
        import libs.widgets as w
        import libs.resource_management as rm

        if item := self.resources_tree_selected_item_from_context:
            path = w.get_tree_item_path(self.project_dir, item)

            rm.delete_file(self, path)
            self._reload_file_tree()
        
    def _create_file_resources_tree(self, event=None):
        import libs.widgets as w
        import libs.resource_management as rm

        item = self.resources_tree_selected_item_from_context
        path = self.project_dir

        if item != None:
            if not os.path.isfile(f"{self.project_dir}/{item.data(0, 0)}"):
                path = w.get_tree_item_path(self.project_dir, item)

        rm.create_file(self, path)
        self._reload_file_tree()
      
    def _create_folder_resources_tree(self, event):
        import libs.widgets as w
        import libs.resource_management as rm
                
        item = self.resources_tree_selected_item_from_context
        path = self.project_dir
        
        if item != None:
            path = w.get_tree_item_path(self.project_dir, item) #self.project_dir + f"/{get_tree_parent_path(item)}" + f"/{item.data(0, 0)}"
            self.resources_tree.expandItem(item)
      
        
        rm.create_folder(self, self.project_dir)
        self._reload_file_tree()
   
    def _reload_file_tree(self):
        import libs.widgets as w
                
        self.resources_tree_files = w.reload_project_resources(self.resources_tree_files, self.project_dir, self.ui.resources_tree, self.project_main_file_name)

    def set_main_project_file(self):  # sourcery skip: use-contextlib-suppress
        import libs.widgets as w
        import libs.project_management as pm

        if project_main_dir := self.resources_tree_selected_item_from_context:
            try:
                if project_main_dir.data(0, 5) == "py":
                    pm.generate_project_path(self, self.project_dir, self.project_name, w.get_tree_item_path(self.project_dir, project_main_dir).replace("//", "/"))
                    self._reload_file_tree()
            except Exception:
                pass    
    
    def set_scenes_dir(self):
        import libs.widgets as w
        import libs.project_management as pm

        if project_scenes_dir := self.resources_tree_selected_item_from_context:
            try:
                if project_scenes_dir.data(0, 5) == "Folder":
                    pm.generate_project_path(self, self.project_dir, self.project_name, project_scenes= w.get_tree_item_path(self.project_dir, project_scenes_dir).replace("//", "/"))
                    self._reload_file_tree()
            except Exception:
                pass        

                    

   
    def _generate_main_py(self):
        import libs.widgets as w
        import libs.resource_management as rm

        item = self.resources_tree_selected_item_from_context
        path = self.project_dir

        if item != None:
            if not os.path.isfile(f"{self.project_dir}/{item.data(0, 0)}"):
                path = w.get_tree_item_path(self.project_dir, item)

        rm.create_py_file(self, path, "main")
        self._reload_file_tree()   
    
    def _generate_script_py(self):
        import libs.widgets as w
        import libs.resource_management as rm

        item = self.resources_tree_selected_item_from_context
        path = self.project_dir

        if item != None:
            if not os.path.isfile(f"{self.project_dir}/{item.data(0, 0)}"):
                path = w.get_tree_item_path(self.project_dir, item)

        rm.create_py_file(self, path)
        self._reload_file_tree()     
    
    def _compile_game(self):
        import libs.compiler as cmplr
        import libs.widgets as widgets

        widgets.info_box(self, "Compilation Started", "Compilation has started")

        comp_dialogue = cmplr.CompileDialog(self._get_main_file(), self.project_dir)
        comp_dialogue.exec_()

    def _open_file_explorer(self):
        import webbrowser, os
        webbrowser.open(os.path.realpath(self.project_dir))       
   
   
    def _run_game(self):
        import libs.process_wrapper as pw

        if self.project_main_file != None:
            if self.ui.pygame_widget.can_run:
                self.ui.pygame_widget.close_process()
                self.ui.start_button.setText("Start")
            else:
                self.ui.pygame_widget.set_process(self.project_main_file, self.project_dir)
                self.ui.start_button.setText("Stop")
    
    def hot_reload_viewport(self):
        if self.project_main_file != None and self.ui.pygame_widget.can_run:
            self.ui.pygame_widget.reload_process() 

    def _print_to_log(self, text: str):
        import libs.widgets as w
        if bool(text.strip()):
            obj = w.QLogItem(self.ui.scrollAreaWidgetContents, self.ui.verticalLayout, text)
            self.console_output_stream.append_object(obj)
            self._autoscroll_console()
   
    def _autoscroll_console(self):
        scroll_bar = self.ui.consoleScrollArea.verticalScrollBar()
        #scroll_bar.setValue(scroll_bar.maximum())

    def _clear_log(self):
        self.console_output_stream.empty_objects()
   
    def _support_message(self):
        if platform.system() != "Windows":
            QMessageBox.information(self, "Partially Unsupported", "Linux support is partial, Program may behave unexpectedly.", QMessageBox.Ok)

       
   
   
    def _open_online_docs(self):
        import libs.red_engine as red_engine
        
        self.window = red_engine.Browser()
        self.window.exec_()

        
        
        
    def _create_creation_context_menu(self, menu):   
        creation_context_menu = QMenu(menu)
        creation_context_menu.setTitle("Create")
        menu.addMenu(creation_context_menu)
        
        creation_context_menu.addActions([self.ui.actionNew_File, self.ui.actionNew_Folder])
        creation_context_menu.addSeparator()
        creation_context_menu.addActions([self.ui.actionEmpty_App, self.ui.actionEmpty_Main, self.ui.actionEmpty_Scene, self.ui.actionEmpty_Script])
        creation_context_menu.addSeparator()
        creation_context_menu.addActions([self.ui.actionExample_App, self.ui.actionExample_Main, self.ui.actionExample_Scene, self.ui.actionExample_Script])
        
        return creation_context_menu
        
        
        
           
    def _create_resources_context_menu(self, event):
        menu= QMenu(self.ui.resources_tree)
        
        self.resources_tree_selected_item_from_context = self.ui.resources_tree.itemAt(event)
        item = self.resources_tree_selected_item_from_context
        
        

        menu.addAction(self.ui.actionOpen_in_File_Explorer)
        menu.addAction(self.ui.actionCopy_Path)
        menu.addSeparator()
        menu.addAction(self.ui.actionReload)
        menu.addSeparator()
        

        if item:
            
                        
            if item.data(0, 5) == "py":
                menu.addAction(self.ui.actionSet_as_Main_py)
                menu.addSeparator()
            if item.data(0, 5) == "Folder":
                menu.addAction(self.ui.actionSet_as_Main_Scenes)
                menu.addSeparator()
                self._create_creation_context_menu(menu)
                
            menu.addAction(self.ui.actionDelete_Resource)
            menu.addAction(self.ui.actionRename)
            menu.addSeparator()
        else:
            cc_menu = self._create_creation_context_menu(menu)


        # copy directory on context menu

        menu.exec_(self.ui.resources_tree.mapToGlobal(event))
    
    def _create_recent_projects_context_menu(self):
        import libs.project_management as pm
        
        r_projs = pm.load_recent_projects_from_json()

        if r_projs is not None:
            for project_name, project_details in r_projs.items():
                action = self.ui.menuRecent_Projects.addAction(project_name)

                proj_json = project_details["json"]
                action.triggered.connect(lambda: self._load_project_folder(proj_json["project_path"]))

    def closeEvent(self, event):
        if self.project_loaded:
            self.save_layout_settings()
            self.check_unsaved_tabs()
            
        super().closeEvent(event)
    
    def _get_main_file(self):
        return self.project_main_file
        
        
        
        
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    print("Unhandled exception:", exc_value)
    traceback.print_exception(exc_type, exc_value, exc_traceback)




if __name__ == "__main__":
    os.chdir(os.getcwd())
    sys.excepthook = handle_exception

    app = QApplication([])
    widget = Pyredengine()
    widget.show()
    
    app.exec_() 
