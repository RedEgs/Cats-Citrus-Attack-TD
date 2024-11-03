from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os, asyncio
    
class FileChangeMonitor(QThread):
    file_changed = pyqtSignal(bool)
    folder_changed = pyqtSignal(str)

    def __init__(self, main_file, project_dir, scenes_dir, parent=None) -> None:
        super().__init__(parent)
        self.main_file = main_file
        self.project_dir = project_dir
        self.scenes_dir = scenes_dir

        self.watched_paths = []


        self.watched_paths.append(self.project_dir)
        if self.main_file is not None and os.path.isfile(self.main_file):
            self.watched_paths.append(self.main_file)
           

    def run(self):
        # Create an asyncio event loop in the new thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Run the asynchronous task in the new event loop
        loop.run_until_complete(self.async_run())
        loop.close()

    async def async_run(self):
        from watchfiles import awatch
        async for changes in awatch(*self.watched_paths):
            for change in changes:
                if os.path.basename(change[1]) == "main.py":
                    self.file_changed.emit(True)
                    break
                else:
                    self.folder_changed.emit(os.path.basename(change[1]))
                    break
                
            
                
            





def rename_file(parent, project_dir, split_name):
    file_name = split_name[0]
    file_extension = f".{split_name[1]}"
    working_dir = f"{project_dir}/{file_name + file_extension}"

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
        with open(selected_item, "r") as f:
            content = f.read()
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
        if not os.path.isfile(f"{working_dir}/{filename}"):
            file = open(f"{working_dir}/{filename}", "w")
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

    if filename is None:
        filename, done = QInputDialog.getText(
            parent, 'Input Dialog', 'Filename: ')
    else:
        done = True

    if done:
        if not os.path.isfile(f"{working_dir}/{filename}.py"):
            with open(f"{working_dir}/{filename}.py", "w") as file:
                if filename == "main":
                    _extracted_from_create_py_file_14(script_generation, file)
        else:
                QMessageBox.critical(
                    parent,
                    "File already exists.",
                    "File exists, try changing the name and try again.",
                    buttons=QMessageBox.Discard,
                    defaultButton=QMessageBox.Discard,
            )


# TODO Rename this here and in `create_py_file`
def _extracted_from_create_py_file_14(script_generation, file):
    template_dir = f"{os.getcwd()}/Libs/templates"
    template_file = "main.template"
    replacements = {}

    sgen = script_generation.ScriptGenerator(template_dir, template_file, replacements)


    file.write(sgen.get_generated_script())
    file.close()
      
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
      
