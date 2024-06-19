from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
    
class FileChangeMonitor(QThread):
    file_changed = pyqtSignal(bool)

    def __init__(self, main_file, project_dir, parent=None) -> None:
        super().__init__(parent)
        self.main_file = main_file
        self.project_dir = project_dir

        self.watched_paths = []
        
        if self.main_file != None and os.path.isfile(self.main_file):
            self.watched_paths.append(self.main_file)
        
        if self.


    def run(self):
        from watchfiles import watch
        for changes in watch(f"{self.project_dir}/scenes"):
            if self.main_file in changes:
                print("main file changed")
            self.file_changed.emit(True)
            
            





def rename_file(parent, project_dir, split_name):
    file_name = split_name[0]
    file_extension = "." + split_name[1]
    working_dir = project_dir+f"/{file_name+file_extension}"

    new_name, done = QInputDialog.getText(
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

    
    filename, done = QInputDialog.getText(
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
    import libs.script_generation as script_generation

    if filename == None:
        filename, done = QInputDialog.getText(
            parent, 'Input Dialog', 'Filename: ') 
    else:
        done = True

    if done:
        if not os.path.isfile(f"{working_dir}/" + filename+".py"):
            file = open(f"{working_dir}/" + filename+".py", "w")
            if filename == "main":
                template_dir = f"{os.getcwd()}/Libs/templates"
                template_file = "main.template"
                replacements = {}
                
                sgen = script_generation.ScriptGenerator(template_dir, template_file, replacements)
               
                
                file.write(sgen.get_generated_script())
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
    
    filename, done = QInputDialog.getText(
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
      
