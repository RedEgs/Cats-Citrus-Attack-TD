from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os, asyncio

class FileChangeMonitor(QThread):
    file_changed = pyqtSignal(bool, str)
    folder_changed = pyqtSignal(str)

    def __init__(self, main_file, project_dir, project_libraries, parent=None) -> None:
        super().__init__(parent)
        self.main_file = main_file
        self.project_dir = project_dir
        self.project_libraries = project_libraries

        self.watched_paths = []
        self.last_changed_file = None


        self.watched_paths.append(self.project_dir)
        for library in self.project_libraries:
            if os.path.isdir(library):
                self.watched_paths.append(library)

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
                    self.file_changed.emit(True, os.path.basename(change[1]))
                    break
                else:
                    self.folder_changed.emit(os.path.basename(change[1]))
                    try:
                        if os.path.basename(change[1]).split(".")[1] == "py":
                            self.file_changed.emit(True, os.path.basename(change[1]))
                    except: pass

                    break








def rename_file(parent, item_path, split_name):
    file_name = split_name[0]
    file_extension = f".{split_name[1]}"

    new_name, done = QInputDialog.getText(
        parent, 'Input Dialog', 'Rename to: ')



    if done:
        if os.path.isfile(item_path):
            os.rename(item_path, os.path.join(os.path.dirname(item_path), new_name+file_extension))

        else:
            QMessageBox.critical(
                parent,
                "File cannot be renamed",
                item_path,
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
                    _copy_main_template(working_dir)
        else:
                QMessageBox.critical(
                    parent,
                    "File already exists.",
                    "File exists, try changing the name and try again.",
                    buttons=QMessageBox.Discard,
                    defaultButton=QMessageBox.Discard,
            )

def _copy_main_template(destination):
    import shutil

    template_file = f"{os.getcwd()}/libs/templates/main.template"
    shutil.copyfile(template_file, f"{destination}/main.py")


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

def open_in_explorer(path):
    import os, subprocess, platform

    folder_path = os.path.realpath(path)
    if os.path.exists(folder_path):
        if platform.system() == "Windows":
            subprocess.run(["explorer", folder_path])
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", folder_path])
        else:  # Linux
            subprocess.run(["xdg-open", folder_path])

def is_image(path):
    if os.path.isfile(path):
        image = QImage()
        return image.load(path)

def is_text_based(path):
    """
    Checks if a file is a text-based file.

    :param file_path: Path to the file
    :return: True if the file is text-based, False otherwise
    """
    # Common text-based file extensions
    text_extensions = ['.txt', '.csv', '.md', '.json', '.xml', '.html', '.py', '.css', '.java']

    # Check file extension
    _, ext = os.path.splitext(path)
    if ext.lower() in text_extensions:
        return True

    # If extension is not enough, try opening the file and checking content
    try:
        with open(path, 'r', encoding='utf-8') as file:
            # Try reading the first few characters to check if it's text
            file.read(1024)  # Read a small portion to test
        return True
    except (UnicodeDecodeError, IOError):
        # If reading as text fails, it's likely a binary file
        return False
