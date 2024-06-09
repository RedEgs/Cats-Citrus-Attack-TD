
import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qsci import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

import typing

class FileChangeMonitor(QThread):
    file_changed = pyqtSignal(bool)

    def __init__(self, main_file, parent=None) -> None:
        super().__init__(parent)
        self.main_file = main_file

    def run(self):
        from watchfiles import watch

        if self.main_file != None and os.path.isfile(self.main_file):
            for changes in watch(self.main_file):
                self.file_changed.emit(True)
    
  


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











def load_recent_projects_from_json():
    import json 
    
    file_path = 'recents.json'
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        print(f"No such file: {file_path}")
        return None

    return data

def add_to_recent_projects(project_name, project_json):
    import json
    file_path = 'recents.json'
    
    data = {}

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            # Read the existing file
            with open(file_path, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            # Handle case where the file is not a valid JSON
            print("Warning: The file is not a valid JSON. Starting with an empty dictionary.")
    
    
    
    
    # Check if the project already exists
    if project_name not in data:
        data[project_name] = {"json": project_json}
        
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Project '{project_name}' added.")
    else:
        print(f"Project '{project_name}' already exists.")
    
def check_recent_projects():
    import json
    file_path = 'recents.json'
    
    data = {}

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            # Read the existing file
            with open(file_path, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            # Handle case where the file is not a valid JSON
            print("Warning: The file is not a valid JSON. Starting with an empty dictionary.")

    if data != {}:
        deleted_entry = []
        for key, value in data.items():
            for x in value.items():
                project_path = x[1]["project_path"]
                project_name = x[1]["project_name"]
                if not os.path.exists(project_path):
                    with open(file_path, "w") as file:
                        remove_value = data.pop(project_name)
                        json.dump(data, file, indent=4  )                        

        
def generate_project_path(window, project_path, project_name, main_project_file = None):
    from datetime import date
    import json
    
    #print(project_path + "/project.json")
    project_file_gen = {
        "project_name": project_name,
        "project_path": project_path,
        "main_project_file": main_project_file, 
        "date_created": str(date.today()),
        "date_edited" : str(date.today())  
    }

    try:
        os.mkdir(project_path + "/.redengine") # Error Handling ehre
    except:
        QMessageBox.critical(window, "Error", f"Project already exists.", QMessageBox.Ok)
        return -1
    
    with open(project_path + "/.redengine/project.json", "w") as file:
        json.dump(project_file_gen, file)

    return project_path + "/.redengine/project.json"

def save_project_json(window, project_path, project_name, main_project_file):
    from datetime import date
    import json
    
    #print(project_path + "/project.json")
    project_file_gen = {
        "project_name": project_name,
        "project_path": project_path,
        "main_project_file": main_project_file, 
        "date_created": str(date.today()),
        "date_edited" : str(date.today())  
    }
    
    with open(project_path + "/.redengine/project.json", "w") as file:
        json.dump(project_file_gen, file)

        
class QIdeWindow(QWidget):
    def __init__(self, parent_tabs:QTabWidget, filepath = None, index = None):
        super(QWidget, self).__init__(parent_tabs)
        self._parent_tabs = parent_tabs
        self._filepath = filepath
        self._index = index
        
        if self._filepath == None:
            self._saved = False
            self.tab_title = f"Script IDE - Untitled"
        else:
            self._saved = False
            self.tab_title = f"Script IDE - {filepath[1]}"
        
        self.ide_tab = QWidget()
        self.ide_tab.setObjectName(f"ide_tab")
            
        self.horizontalLayout = QHBoxLayout(self.ide_tab)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        
        self.script_edit = QsciScintilla(self.ide_tab)
        self.script_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.script_edit.setObjectName(u"script_edit")
        self.script_edit.setGeometry(QRect(10, 9, 710, 611))
        self.script_edit.setFrameShape(QFrame.StyledPanel)
        self.script_edit.setFrameShadow(QFrame.Raised)

        self.lexer = QsciLexerPython(self.script_edit)

        self.script_edit.setMarginType(0, QsciScintilla.NumberMargin)
        self.script_edit.setMarginWidth(0, "0000")
        self.script_edit.setMarginsForegroundColor(QColor("#ff888888"))

        self.script_edit.setLexer(self.lexer)

        self.script_edit.setAutoCompletionSource(self.script_edit.AutoCompletionSource.AcsAll)
        self.script_edit.setAutoCompletionThreshold(2)
        self.script_edit.setAutoCompletionReplaceWord(True)
 
        self.script_edit.setLineWidth(0)
        self.script_edit.setUtf8(True) 
        self.script_edit.setTabWidth(4)
        self.script_edit.setIndentationsUseTabs(True)
        self.script_edit.setAutoIndent(True)
        self.script_edit.setIndentationGuides(True)  
        
        self.horizontalLayout.addWidget(self.script_edit)
        
        self.tab_index = parent_tabs.addTab(self.ide_tab, self.tab_title)
        self.load_file()
        
        self.script_edit.textChanged.connect(self.mark_as_unsaved)
        self._parent_tabs.setCurrentIndex(self.tab_index)
        
        self._parent_tabs.tabCloseRequested.connect(self.close_tab)
    
    def close_tab(self): 
        current_widget = self._parent_tabs.indexOf(self.ide_tab)
        if self._parent_tabs.currentIndex() == current_widget:
            self._parent_tabs.removeTab(current_widget)
    
    def mark_as_unsaved(self):
        self._saved = False
        self._parent_tabs.setTabText(self.tab_index, self.tab_title+"*")
    
    def load_file(self):
        # Load contents into file 
        contents = open_file(self, self._filepath[0])
        self.script_edit.setText(contents)
        
    def save_file(self):
        file = open(self._filepath[0], "w")
        file.write(self.script_edit.text())
        file.close()
        
        self._saved = True
        self._parent_tabs.setTabText(self.tab_index, self.tab_title)
    

def get_tree_parent_path(item):
    parent = item.parent()
    if parent is None:
        return ""
    else:
        return get_tree_parent_path(parent) + "/" + parent.data(0, 0)

def get_tree_item_path(working_dir, item):
    return working_dir + f"/{get_tree_parent_path(item)}" + f"/{item.data(0, 0)}"


def rename_file(parent, project_dir, split_name):
    import os.path, os

    file_name = split_name[0]
    file_extension = "." + split_name[1]
    working_dir = project_dir+f"/{file_name+file_extension}"

    new_name, done = QtWidgets.QInputDialog.getText(
        parent, 'Input Dialog', 'Rename to: ') 

    

    if done:
        if os.path.isfile(f"{working_dir}"):
            os.rename(f"{working_dir}", f"{project_dir}/{new_name+file_extension}")
        
        else:
            QMessageBox.critical(
                parent,
                "File cannot be renamed",
                f"{working_dir}",
                buttons=QMessageBox.Discard,
                defaultButton=QMessageBox.Discard,
        )    
            
    

def open_file(parent, selected_item):
    import os
    

    content = ""
    if os.path.isfile(selected_item):
        f = open(selected_item, "r")
        content = f.read()       
        f.close()
        
    return content 

def delete_file(parent, selected_item):
    import os, shutil
    
    if os.path.isfile(selected_item):
        os.remove(selected_item)
    elif os.path.exists(selected_item):
        shutil.rmtree(selected_item)

def create_file(parent, working_dir):
    import os.path

    
    filename, done = QtWidgets.QInputDialog.getText(
        parent, 'Input Dialog', 'Filename: ') 

    if done:
        if not os.path.isfile(f"{working_dir}/" + filename):
            file = open(f"{working_dir}/" + filename, "w")
            file.close()
        
        else:
            QMessageBox.critical(
                parent,
                "File already exists.",
                "File exists, try changing the name and try again.",
                buttons=QMessageBox.Discard,
                defaultButton=QMessageBox.Discard,
        )
  
def create_py_file(parent, working_dir, filename = None):
    import os.path

    # Logic here for filling project up with classes and shi
   
    if filename == None:
        filename, done = QtWidgets.QInputDialog.getText(
            parent, 'Input Dialog', 'Filename: ') 
    else:
        done = True

    if done:
        if not os.path.isfile(f"{working_dir}/" + filename+".py"):
            file = open(f"{working_dir}/" + filename+".py", "w")
            if filename == "main":
                file.write(get_example_main())
                file.close()
                
            file.close()
        
        else:
            QMessageBox.critical(
                parent,
                "File already exists.",
                "File exists, try changing the name and try again.",
                buttons=QMessageBox.Discard,
                defaultButton=QMessageBox.Discard,
        )
    
  
    
def create_folder(parent, working_dir):
    import os
    
    filename, done = QtWidgets.QInputDialog.getText(
        parent, 'Input Dialog', 'Filename: ') 

    if done:
        try: file = os.mkdir(f"{working_dir}/{filename}")
        except FileExistsError:
            QMessageBox.critical(
                parent,
                "File already exists.",
                "File exists, try changing the name and try again.",
                buttons=QMessageBox.Discard,
                defaultButton=QMessageBox.Discard,
        )
   
def get_file_from_path(path):
    try:
        return os.path.basename(path).split('/')[-1]   
    except:
        return None
      

      
      
#SECTION - Treeview functions    
            
def load_project_resources(startpath, tree, main_file_name = None):
    """
    Load Project structure tree
    :param startpath: 
    :param tree: 
    :return: 
    """
    import os
    from PyQt5.QtWidgets import QTreeWidgetItem
    from PyQt5.QtGui import QIcon
    
    
    resources_items = []
    for element in os.listdir(startpath):
        path_info = str(startpath) + "/" + element
        parent_itm = QTreeWidgetItem(tree, [os.path.basename(element)])
        file_type = element.split(".")
        
        
        
        resources_items.append(element)
        if os.path.isdir(path_info):
            load_project_resources(path_info, parent_itm)
            parent_itm.setIcon(0, QIcon('assets/folder.ico'))
            
        else:
            if element == main_file_name:
                #print(element)
                parent_itm.setIcon(0, QIcon('assets/icon32.png'))
            elif len(file_type) >= 2 and os.path.isfile(f'assets/{file_type[len(file_type)-1]}.ico'):
                parent_itm.setIcon(0, QIcon(f'assets/{file_type[len(file_type)-1]}.ico'))
            else:
                parent_itm.setIcon(0, QIcon('assets/file.ico'))
        
        
                
    return resources_items

def reload_project_resources(previous_files=None, startpath = None, tree = None, main_file_name = None):    
    tree.clear()
    files = load_project_resources(startpath, tree, main_file_name)
    return files
        
def search_tree_view(tree_widget, line_edit):
    search_query = line_edit.text().lower()
    for item in tree_widget.findItems("", QtCore.Qt.MatchContains):
        item.setHidden(search_query not in item.text(0).lower())
        
def get_example_main():
    file = """
import pygame, sys, os

class MainGame():
    def __init__(self) -> None:
        print("hi")
        pygame.init()
        
        print("hi")
        self._init_display()
        print("hello")
        self.clock = pygame.Clock()
        self.run = True
        print("finito")

    def _init_display(self):
        self._hwnd = None
        if len(sys.argv) > 1:
            self._hwnd = int(sys.argv[1])
            os.environ['SDL_WINDOWID'] = str(self._hwnd)
        
        self.display_width = 1280
        self.display_height = 720
        
        
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (-1000, -1000)
        self.display = pygame.display.set_mode((self.display_width, self.display_height), pygame.NOFRAME)
        pygame.display.set_caption("Pygame Window")
        
    def send_key(self, key):
        event = pygame.event.Event(pygame.KEYDOWN, key=key)
        pygame.event.post(event)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

    def update(self):
        # Input updating logic here
        pass
    
    def draw(self):
        # Input drawing logic here
        pygame.display.flip()
    
    def run_game(self):
        while self.run:
            self.clock.tick()
            self.handle_events()
            self.update()
            self.draw()
            
            yield self.display

        pygame.quit()
        sys.exit()
        
    def close_game(self):
        self.run = False
        pygame.quit()
    """
    
    return file

