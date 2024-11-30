import engine_design, launcher_design
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from functools import partial
import os, json, sys, importlib, platform, traceback, asyncio
import concurrent.futures
# Find out how to include images

class Pyredengine(QMainWindow):
    def __init__(self, project_json_data = None, launcher = None, *args, **kwargs) -> None:
        import libs.project_management as pm
        import libs.widgets as w
        import libs.compiler as cmp
        
        super().__init__(*args, **kwargs)
        self.project_json_data = project_json_data
        self.project_loaded = False    
        self.project_dir = None    
        self._app_launcher = launcher
        
        self.application_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(self.application_path)
        
        self.ui = engine_design.Ui_main_window()
        self.ui.setupUi(self)
        
        
        pm.check_recent_projects()
        self._load_console()
        self._support_message()
        if self.project_json_data != None:
            self._load_icons()
            self._load_project(self.project_json_data)   
            
            
        
    
        else:
            self.save_default_settings()
        
        self._load_menu_bar_actions()
        self._create_recent_projects_context_menu()

    def _load_menu_bar_actions(self):
        import libs.project_management as pm
        
        self.ui.pause_button.setDisabled(True)  
        self._populate_platform_debug_table()      

        
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
            self.ui.actionExample_Script.triggered.connect(self._generate_script_py)
            self.ui.actionExample_Main.triggered.connect(self._generate_main_py)
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
            self.ui.actionPropertiesWindow.triggered.connect(self.ui.Properties_dock.show)

            self.ui.actionCompile_Project.triggered.connect(self._compile_game)
            
            self.ui.start_button.pressed.connect(self._run_game)
            self.ui.actionRun_Project.triggered.connect(self._run_game)
            self.ui.actionRun_In_Fullscreen.triggered.connect(self._run_game_fullscreen)
            self.ui.pause_button.pressed.connect(self._pause_game)
            self.ui.actionPause_Project.triggered.connect(self._pause_game)
            self.ui.reload_button.pressed.connect(self.hot_reload)

            self.ui.actionPopout_Viewport.triggered.connect(self._popout_viewport)
            self.ui.actionReturnLauncher.triggered.connect(self._return_to_launcher)
    
            self.ui.actionRevert_Themes.triggered.connect(self._reset_theme)
    
            self.ui.console_command_line.returnPressed.connect(self._send_console_command)
            self.ui.clear_log_button.pressed.connect(self._clear_log)

            self.ui.actionDocumentation.triggered.connect(self._open_online_docs)

           

 
    def _load_shortcuts(self):
        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.activated.connect(self._save_project) 
        
        reload_shortcut = QShortcut(QKeySequence("Ctrl+5"), self)
        reload_shortcut.activated.connect(self._reload_project) 
        
        launch_shortcut = QShortcut(QKeySequence(Qt.Key.Key_F5), self)
        launch_shortcut.activated.connect(self._run_game)
        
        
          
    def _load_icons(self):
        self.iconControlSquare = QIcon()
        self.iconControlSquare.addFile(u"../redengine/assets/icons-shadowless/control-stop-square.png", QSize(), QIcon.Normal, QIcon.Off)
          
        self.iconControl = QIcon()
        self.iconControl.addFile(u"../redengine/assets/icons/control.png", QSize(), QIcon.Normal, QIcon.Off)
          
        self.iconControlPause = QIcon()
        self.iconControlPause.addFile(u"../redengine/assets/icons/control-pause.png", QSize(), QIcon.Normal, QIcon.Off)
          
        self.iconGameMonitor = QIcon()
        self.iconGameMonitor.addFile(u"../redengine/assets/icons/game-monitor.png", QSize(), QIcon.Normal, QIcon.Off)
          
        self.iconColorSwatch = QIcon()
        self.iconColorSwatch.addFile(u"../redengine/assets/icons/color-swatch.png", QSize(), QIcon.Normal, QIcon.Off)

        self.iconPlus = QIcon()
        self.iconPlus.addFile(u"../redengine/assets/icons/plus.png", QSize(), QIcon.Normal, QIcon.Off)

          
    def _relaunch_window(self, data):
        self.newWindow = Pyredengine(data)
        self.newWindow.show()
        self.close()
    
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
        
        try:
            self.resources_tree_files = w.load_project_resources(self.project_dir, self.ui.resources_tree, self.project_main_file_name, self.application_path)
        except Exception as e:
            pass
        
        self.ui.resources_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.resources_tree.customContextMenuRequested.connect(self._create_resources_context_menu)
        self.ui.resource_search_bar.textChanged.connect(lambda: w.search_tree_view(self.ui.resources_tree, self.ui.resource_search_bar))

        self.load_layout_settings()
        
        self._initialise_themes()

        self._process_running = False
        self.__game_process = None
      
        self.monitor_thread = QThread()
        self.monitor_worker = rm.FileChangeMonitor(self.project_main_file, self.project_dir, self.project_scenes_dir)
        self.monitor_worker.moveToThread(self.monitor_thread)
        self.monitor_thread.started.connect(self.monitor_worker.run)
        self.monitor_worker.file_changed.connect(self.hot_reload)
        self.monitor_worker.folder_changed.connect(self._reload_project)
        self.monitor_worker.start()
      
        #sys.stderr = self.console_output_stream
        sys.stdout = red_engine.ConsoleWrapper(self, self.ui.console)
      


    def _load_project_folder(self, folder_path):  
        try:
            if os.path.exists(f"{folder_path}/.redengine"):
                path = f"{folder_path}/.redengine"
                self._load_project_file(f"{path}/project.json")

            elif response := QMessageBox.critical(
                self,
                "Not valid project directory",
                "Not a valid project, would you like to make it one instead?",
                QMessageBox.Save | QMessageBox.Discard,
            ):
                self._prompt_project_name(folder_path)



        except (Exception, Exception) as e:
            print(f"failed to load folder {e}")
            QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}", QMessageBox.Ok)

    def _load_project_file(self, fileName):
        try:
            with open(fileName, 'r') as file:
                data = file.read()
                self._relaunch_window(data)
                
                QMessageBox.information(self, "File Loaded", f"File {fileName} loaded successfully!", QMessageBox.Ok)
        except Exception as e:
            print(f"failed to load file, {e}")
            QMessageBox.critical(self, "Error", f"Failed to project.json load file: {str(e)}", QMessageBox.Ok)

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
                
        
    def _reload_file_tree(self):
        import libs.widgets as w
    
        self.resources_tree_files = w.reload_project_resources(self.project_dir, self.ui.resources_tree, self.project_main_file_name, os.path.dirname(os.path.abspath(__file__)))
    
    def _reload_project(self):
        self._reload_file_tree()


       
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
   
    def set_main_project_file(self, path = None):  # sourcery skip: use-contextlib-suppress
        print("firing project main file setting")
        import libs.widgets as w
        import libs.project_management as pm

        print("setting main file")

        if path is not None:
            print(f"settings project main file as: {path}")
            pm.generate_project_path(self, self.project_dir, self.project_name, path)
            self._relaunch_window(self.project_json_data)
        elif project_main_dir := self.resources_tree_selected_item_from_context:
            print(f"setting project path as {w.get_tree_item_path(self.project_dir, project_main_dir).replace("//", "/")}")
            try:
                if project_main_dir.data(0, 5) == "py":
                    pm.generate_project_path(self, self.project_dir, self.project_name, w.get_tree_item_path(self.project_dir, project_main_dir).replace("//", "/"))
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

        comp_dialogue = cmplr.CompileDialog(self._get_main_file(), self.project_dir, parent=self)
        comp_dialogue.exec_()
        


    def _open_file_explorer(self):       
        import os, subprocess

        folder_path = os.path.realpath(self.project_dir)

        if platform.system() == "Windows":
            os.startfile(folder_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", folder_path])
        else:  # Linux
            subprocess.run(["xdg-open", folder_path])
   
    def _main_file_disclaimer(self):
        import libs.resource_management as rm
        
        response = QMessageBox.critical(self, "No Main file assigned or created.", "No main file was found, please assign one if already created or click save to have one generated for you. ",
                   QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Ok)
        if response == QMessageBox.StandardButton.Save:
            rm.create_py_file(self, self.project_dir, "main")
            self._reload_file_tree()
   
    def _run_game(self):
        import libs.process_wrapper as pw
        import libs.widgets as w

        if self.project_main_file != None:
            if self.ui.pygame_widget.can_run:
                self.__game_process = None
                self.ui.pygame_widget.close_process()
                self._reset_play_button(True)

                self._stop_pygame_debug_values()
                self._stop_properties_manager()

            else:
                self._start_game(False)
        else:
            self._main_file_disclaimer()

            
    
    def _run_game_fullscreen(self):
        import libs.compiler as cmplr

        if self.project_main_file != None:
            if self.ui.pygame_widget.can_run:
                self.__game_process = None
                self.ui.pygame_widget.close_process()
                self._reset_play_button(True)


                self._stop_pygame_debug_values()

            else:
                self._start_game(True)
                
    def _start_game(self, fullscreen = False):
        self.ui.pygame_widget.set_process(self.project_main_file, self.project_dir, fullscreen)
        self.__game_process = self.ui.pygame_widget.get_process()
        self._reset_play_button(False)

        self._populate_pygame_debug_table()
        self. _start_pygame_debug_values()
        self._start_properties_manager()


    def _pause_game(self):
        if self.project_main_file != None and self.ui.pygame_widget.can_run:
            self.ui.pygame_widget.paused = not self.ui.pygame_widget.paused

            if self.ui.pygame_widget.paused:
                self.ui.reload_button.setDisabled(True)
                self.ui.stop_button.setDisabled(True)

                self.ui.pause_button.setIcon(self.iconControl)
            else:
                self.ui.reload_button.setDisabled(False)
                self.ui.stop_button.setDisabled(False)

                self.ui.pause_button.setIcon(self.iconControlPause)

            self.ui.mainScriptPropertiesGroup.setEnabled(True)
         
         
         
            
    def hot_reload(self):
        import libs.widgets as w
        
        if self.project_main_file != None and self.ui.pygame_widget.can_run:
            self.ui.pygame_widget.reload_process() 

    def _load_console(self):
        self._cError_count = 0
        self._cWarning_count = 0
        self._cInfo_count = 0
    
        self.ui.error_count_label.setText("0")
        self.ui.warning_count_label.setText("0")
        self.ui.log_count_label.setText("0")
        
        self.ui.console_command_line._import_game_var = False
        self.ui.console_command_line._import_eng_var = False
        

    def _update_console(self):
        self.ui.error_count_label.setText(str(self._cError_count))
        self.ui.warning_count_label.setText(str(self._cWarning_count))
        self.ui.log_count_label.setText(str(self._cInfo_count))
        
    def _send_console_command(self):
        # allow importing of engine vars and game vars
        # allow commands

        
        cli = self.ui.console_command_line

        command = cli.text()
        print(f">> {command}")
        
        cli.clear()
        
        if command == "reload":
            self._reload_project()
            self.hot_reload()
        elif command == "scope: game":
            print("Imported game variables")
            cli._import_game_var = True
            cli._import_eng_var = False
        elif command == "scope: eng":
            print("Imported engine variables")
            cli._import_game_var = False
            cli._import_eng_var = True
        elif command == "scope: none":
            print("Unimported all variables")
            cli._import_game_var = False
            cli._import_eng_var = False
        elif command == "popout":
            self._popout_viewport()
            
        else:
            try:
                if cli._import_game_var == True:
                    if self.__game_process is not None:
                        exec(command, vars(self.__game_process))
                    else:
                        print("<<Warning>> Game Process does not exist")
                elif cli._import_eng_var:
                    exec(command, globals()) 
            except Exception as e:
                print(f"<<Warning>>{e}")

    def _copy_error_message(self):
        pass
        
        
    def _clear_log(self):
        self.ui.console.clear()
        self._load_console()
   
    def _support_message(self):
        if platform.system() != "Windows":
            QMessageBox.information(self, "Partially Unsupported", "Linux support is partial, Program may behave unexpectedly.", QMessageBox.Ok)


    def _open_online_docs(self):
        import webbrowser
        
        webbrowser.open("https://github.com/RedEgs")
        
    def _initialise_themes(self):        
        for theme in os.listdir(self.application_path+"/assets/themes"):
            if not (".qss" in theme or ".css" in theme):
                return
        
            action: QAction = self.ui.menuLoad_Themes.addAction(theme)
            action.setIcon(self.iconColorSwatch)
            action.setText(theme.split(".")[0])
            action.triggered.connect(partial(self._load_theme, self.application_path+"/assets/themes/" + theme))
            
    def _load_theme(self, path):
        with open(path, "r") as f:
            content = f.read()
            self.setStyleSheet(content)
        
    def _reset_theme(self):
        self.setStyleSheet(" ")
        


    def _reset_play_button(self, Playing):
        Playing = not Playing
        
        if Playing:
            self.ui.start_button.setIcon(self.iconControlSquare)
            self.ui.pause_button.setEnabled(True)
        else:
            self.ui.start_button.setIcon(self.iconControl)
            self.ui.pause_button.setEnabled(False)
            self.ui.reload_button.setEnabled(False)
        
    def _start_properties_manager(self):
        import libs.process_wrapper as pw
        
       
        # self.PropertiesManager.started.connect(self.PropertiesManager.run)
        # self.PropertiesManager.start()
        
        self.PropertiesTimer = QTimer()
        self.PropertiesManager = pw.PropertiesThread(self.ui.pygame_widget.game, self.ui.PropertiesTable, self.PropertiesTimer, self.ui.pygame_widget, self.ui)
        self.PropertiesTimer.timeout.connect(self.PropertiesManager.run)
        self.PropertiesTimer.start(10)
        
        if self.ui.pygame_widget.paused:
            self.ui.mainScriptPropertiesGroup.setEnabled(False)
        
    def _stop_properties_manager(self):
        self.ui.PropertiesTable.clear()
        self.PropertiesTimer.stop()
        
    
        
        
    def _populate_platform_debug_table(self):
        listWidget = self.ui.platform_debug_list
        
        ListItems = [
            QListWidgetItem(f"Operating System: {platform.system()} {platform.release()}"),
            QListWidgetItem(f"Operating System Version: {platform.version()}"),
            QListWidgetItem(f"Machine: {platform.machine()}"), 
            QListWidgetItem(f"Processor: {platform.processor()}"), 
            QListWidgetItem(f"Architecture: {platform.architecture()}"), 
            QListWidgetItem(f"Platform: {platform.platform()}"), 
            QListWidgetItem(f"Python Build: {platform.python_build()}"), 
            QListWidgetItem(f"Python Version: {platform.python_version()}"), 
        ]
        for i in ListItems:
            listWidget.addItem(i)
            
    def _populate_pygame_debug_table(self):
        import pygame 

        display: pygame.display = self.ui.pygame_widget.game.get_main_display()
        listWidget = self.ui.pygame_debug_list
        listWidget.clear()


        ListItems = [
            QListWidgetItem(f"SDL Version: {pygame.get_sdl_version(True)[0]}.{pygame.get_sdl_version(True)[1]}.{pygame.get_sdl_version(True)[2]}"), 
            QListWidgetItem(f"Pygame Display Size: {pygame.display.get_window_size()} "),
            QListWidgetItem(f"Pygame Display Backend Driver: {pygame.display.get_driver()} "), 

        ]


        if pygame.IS_CE:
            ListItems.insert(0, (QListWidgetItem(f"Pygame-CE Version: {pygame.version.ver}")))
        else:
            ListItems.insert(0, (QListWidgetItem(f"Pygame Version: {pygame.version.ver}")))       

        if "dev" in pygame.version.ver:
            ListItems.insert(1, QListWidgetItem("Is Pre-Release?: Yes"))       
            print('<<Warning>> You are using a pygame pre-release, use "at your own risk".')
                           

        for i in ListItems:
            listWidget.addItem(i)

    def _start_pygame_debug_values(self):
        import psutil as psu

        self._debug_timer = QTimer()

        self._fps_high = 0
        self._fps_low = float("inf")

        gamehandler = self.ui.pygame_widget.game

        def get_debug_info(parent):
            info = gamehandler.debug_info()
            if not info:
                return

            try:
                dt = info[0]
            except Exception as e:
                pass
            
            fps = round(info[1], 0)
            blit_count = info[2]
            current_tick = info[3]
            bps = info[4]
            draw_count = info[5]
            dps = info[6]

            self.ui.delta_time_label.setText(f"Delta Time: {dt}ms")

            # Update FPS stats
            parent._fps_high = max(fps, parent._fps_high)
            parent._fps_low = min(fps, parent._fps_low)

            def get_fps_text(label, value, red_cond, green_cond):
                if value < red_cond:
                    return f'<span style="color: red;">{label}: {value}</span>'
                elif value > green_cond:
                    return f'<span style="color: green;">{label}: {value}</span>'
                else:
                    return f'<span style="color: yellow;">{label}: {value}</span>'

            # Set text for high, average, and low FPS
            self.ui.fps_high_label.setText(get_fps_text("High", parent._fps_high, 60, 120))
            self.ui.fps_average_label.setText(get_fps_text("Avg", fps, 30, 100))
            self.ui.fps_low_label.setText(get_fps_text("Low", parent._fps_low, 10, 60))

            self.ui.blit_calls_label.setText(f"Blit Calls (Per Tick): {-bps}")
            self.ui.draw_calls_label.setText(f"Draw Calls (Per Tick): {-dps}")

            if self.ui.resource_monitor_group.isChecked():
                vmem = psu.virtual_memory()
                process = psu.Process(os.getpid())
                
                with process.oneshot():
                    cpu_pusage = process.cpu_percent(0)
                    mem_pusage = process.memory_info().rss / (1024 * 1024) 
                
                cpu_usage = psu.cpu_percent(interval=0)
                mem_usage = round(vmem.used / (1024 * 1024), 0)
                mem_total = round(vmem.total / (1024 * 1024), 0)
                ram_usage = vmem.percent
                
                self.ui.cpu_usage_label.setText(f"CPU Usage: {cpu_usage}%")
                self.ui.cpu_usage_label_2.setText(f"CPU Usage (Process): {cpu_pusage}%")
                self.ui.ram_usage_label.setText(f"RAM Usage: {ram_usage}%")
                self.ui.memory_usage_label.setText(f"Memory Usage: {mem_usage}MB / {mem_total}MB")
                self.ui.memory_pusage_label.setText(f"Memory Usage (Process): {mem_pusage}MB")

                




        self._debug_timer.timeout.connect(lambda: get_debug_info(self))
        self._debug_timer.start(100)

    def _stop_pygame_debug_values(self):
        self._debug_timer.stop()
        
        
    def _create_creation_context_menu(self, menu):   
        creation_context_menu = QMenu(menu)
        creation_context_menu.setTitle("Create")
        creation_context_menu.setIcon(self.iconPlus)
        menu.addMenu(creation_context_menu)
        
        creation_context_menu.addActions([self.ui.actionNew_File, self.ui.actionNew_Folder])
        creation_context_menu.addSeparator()
        creation_context_menu.addActions([self.ui.actionExample_Main, self.ui.actionExample_Script])
        
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
                #menu.addAction(self.ui.actionSet_as_Main_Scenes)
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
        
        self._r_projs = pm.load_recent_projects_from_json(self.application_path)

        if self._r_projs is not None:
            for project_name, project_details in self._r_projs.items():
                action: QAction = self.ui.menuRecent_Projects.addAction(project_name)
                
                folder_path = project_details["json"]["project_path"]
                action.triggered.connect(partial(self._load_project_folder, folder_path))

    
    
  
    def _popout_viewport(self):
        class PopOutWindow(QMainWindow):
            def __init__(self, widget, main_window):
                super().__init__()
                self.setWindowTitle("Popped Out Widget")
                self.setCentralWidget(widget)  # Place the widget in the new window
                
                self.main_window = main_window
                
                self.setWindowIcon(self.main_window.iconGameMonitor)
                self.setWindowTitle("Pygame Preview") # Add pygame caption
                self.setWindowFlags(Qt.WindowStaysOnTopHint)
                
                #self.setWindowModality(Qt.WindowModality.ApplicationModal)
                self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
                
                
            def closeEvent(self, event):
                self.main_window._popout_closed()
                super().closeEvent(event)
                
                
        
        if not hasattr(self, "_viewport_popped") or not self._viewport_popped:
            self.popped_window = PopOutWindow(self.ui.frame_6, self)
            self.popped_window.show()
            
            self._viewport_popped = True
        
    def _popout_closed(self):
        self._viewport_popped = False
        self.ui.verticalLayout_8.addWidget(self.ui.frame_6)

    def _return_to_launcher(self):
        self._app_launcher.show()
        self.close()

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


class Launcher(QWidget):
    def __init__(self):
        super().__init__()

        import threading
        self.ui = launcher_design.Ui_Form()
        self.ui.setupUi(self)
        self.application_path = os.path.dirname(os.path.abspath(__file__))
        
        self.ui.projects_table.itemClicked.connect(self._select_project)
        self.ui.projects_table.itemDoubleClicked.connect(self._load_project)
        self.ui.look_button.pressed.connect(self._look_project)
        self.ui.create_button.pressed.connect(self._save_project_as)
        self.ui.delete_button.pressed.connect(self._delete_project)
        self.ui.install_button.pressed.connect(self._download_python_version)
        
        self.launch_connection = self.ui.launch_button.pressed.connect(self._load_project)
        
        
        self.ui.create_button.setEnabled(True)
        self.ui.install_button.setEnabled(False)
        
        self.populate_projects_table()
        #self._get_python_versions()
        self._versions_tab_loaded = False
        threading.Thread(target=lambda: self._get_python_versions()).start()
        


    def _enable_project_buttons(self):
        self.ui.launch_button.setEnabled(True)
        self.ui.look_button.setEnabled(True)
        self.ui.delete_button.setEnabled(True)
        
    def _disable_project_buttons(self):
        self.ui.launch_button.setEnabled(False)
        self.ui.look_button.setEnabled(False)
        self.ui.delete_button.setEnabled(False)
            
    def _select_project(self, item):
        project_data = self.ui.projects_table.item(item.row(), 0)._project_data
        self._project_path = project_data["project_path"]
        self._project_name = project_data["project_name"]
        
        with open(project_data["project_path"]+"/.redengine/project.json", 'r') as file:
            self.project_data = file.read()
                
        self._enable_project_buttons()
         
    def _load_project(self):
        engine = Pyredengine(self.project_data, launcher)
        #self.ui.launch_button.disconnect(self.launch_connection)
        engine.show()
        launcher.hide()
        
    def _look_project(self):
        import webbrowser
        
        webbrowser.open(self._project_path)
    
    def _delete_project(self):
        import libs.project_management as pm
        import shutil
        
                
        response = QMessageBox.critical(self, "Confirm", "Are you sure you want to delete this project, the changes are irreversible", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
        if response == QMessageBox.StandardButton.Yes:
            path = self._project_path
            shutil.rmtree(path)
            
            pm.remove_from_recent_projects(self.application_path, self._project_name)
            self.regenerate_table()
            
        else:
            print("cancelled deletion")
            return False
            

    def populate_projects_table(self):
        import libs.project_management as pm
        
        table = self.ui.projects_table
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_items = 0
        projs = pm.load_recent_projects_from_json(self.application_path)



        if projs is not None:
            table.setRowCount(10)
            table.setSelectionBehavior(QAbstractItemView.SelectRows)
            for project_name, project_details in projs.items():
                _project_data = project_details["json"]

                if not os.path.exists(_project_data["project_path"]+"/.redengine/project.json"):
                    print(f"file does not exist at {_project_data["project_path"]}")
                    continue
                print(f"file does exist at {_project_data["project_path"]}")

                main_item = QTableWidgetItem(project_name)
                main_item._project_data = project_details["json"]


                table.setItem(self.table_items, 0, main_item)
                table.setItem(self.table_items, 1, QTableWidgetItem("0.0.0"))
                table.setItem(self.table_items, 2, QTableWidgetItem(project_details["json"]["project_path"]))
            
                try:
                    table.setItem(self.table_items, 3, QTableWidgetItem(project_details["json"]["user"]))
                except Exception as e:
                    table.setItem(self.table_items, 3, QTableWidgetItem("Unknown Author"))
            
                self.table_items +=1
            table.setRowCount(self.table_items)

  
    def regenerate_table(self):                    
        for i in range(self.table_items):
            self.ui.projects_table.removeRow(i)
        
        
        self.populate_projects_table()

    def _prompt_project_name(self, folder_path):
        import libs.project_management as pm

        project_name, ok = QInputDialog.getText(self, "Project Name", "Enter the project name:")
        if ok and project_name:
            json_path = pm.generate_project_path(self, folder_path, project_name)

            if json_path == -1:
                self._load_project_file(f"{folder_path}/.redengine/project.json")

            else:     
                with open(json_path, "r") as file:
                    
                    self._project_data = json.load(file)
                    pm.add_to_recent_projects(self._project_data["project_name"], self._project_data)
                    
                    print("added to recents")
                    for i in range(self.table_items):
                        self.ui.projects_table.removeRow(i)
                    
                    
                    self.populate_projects_table()
                    


        else:
            QMessageBox.information(self, "No Project Name", "No project name was   provided.", QMessageBox.Ok)

    def _save_project_as(self):        
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        if folder_path := QFileDialog.getExistingDirectory(
            self, "Select Folder", QDir.homePath(), options=options
        ):
            self._prompt_project_name(folder_path)
        else:
            QMessageBox.information(self, "No Folder Selected", "No folder was selected.", QMessageBox.Ok)
            
    def _download_python_version(self):
        import libs.red_engine as re
        import webbrowser
        
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        if folder_path := QFileDialog.getExistingDirectory(
            self, "Select Folder", QDir.homePath(), options=options
        ):

                    
            self.progress_dialog = re.ProgressDialog(self.py_dl_link, folder_path+"/installer.exe", self.py_name[0])
            self.progress_dialog.show()
            self.progress_dialog.download()


            
    def _select_python_version(self, item):
        self.ui.install_button.setEnabled(True)
        self.py_dl_link = self.ui.python_versions_table.item(item.row(), 0)._dl_link
        self.py_name = self.ui.python_versions_table.item(item.row(), 0)._py_name

    def _get_python_versions(self):
        import requests
        from bs4 import BeautifulSoup

        if self._versions_tab_loaded == True:
            return
        

        # URL for the Python downloads page
        url = 'https://www.python.org/downloads/windows/'

        # Send a GET request to the URL
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the Python version links
        table = self.ui.python_versions_table
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.itemClicked.connect(self._select_python_version)
        
        
        versions = soup.find_all('a')
        
        items_counter = 0
        table.setRowCount(15)
        for index, version in enumerate(versions):
            text = version.text.strip().split("-")
            dl_link = version["href"]
            version_num = text[0].replace("Python ", "").replace(" ", "")
            generated_link = f"https://www.python.org/ftp/python/{version_num}/python-{version_num}-amd64.exe"
            if "/downloads/release/python-" in dl_link:
                if "Latest Python 3" in text[0]:
                    continue
                if int(version_num[0]) < 3 or int(version_num[2:4].replace(".", "")) <= 10:
                    continue
                if items_counter >= 15:
                    break
                if requests.head(generated_link, allow_redirects=True).status_code != 200:
                    continue
       
                i1 = QTableWidgetItem(text[0])
                i1.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                i1._dl_link = generated_link
                i1._py_name = text
                
                i2 = QTableWidgetItem(text[1])
                i2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                
                i3 = QTableWidgetItem("python.org" + dl_link)
                i3.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                
                
                table.setItem(items_counter, 0, i1)
                table.setItem(items_counter, 1, i2)
                table.setItem(items_counter, 2, i3)
                
                items_counter += 1

        
        
        
        self._versions_tab_loaded = True








if __name__ == "__main__":
    os.chdir(os.getcwd())
    sys.excepthook = handle_exception
    
    app = QApplication([])
    

    launcher = Launcher()
    launcher.show()
    


    
    app.exec_() 
