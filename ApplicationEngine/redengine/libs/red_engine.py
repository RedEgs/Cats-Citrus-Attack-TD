import sys, os, io
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qsci import *
import libs.widgets as w

class ConsoleWrapper(io.StringIO):
    def __init__(self, parent, text_edit):
        super().__init__()
        self.text_edit = text_edit
        self.parent = parent

    def write(self, message):
        if "Traceback" in message:  # Check for an exception
            # Format exception message in red
            self.text_edit.append(f'<span style="color: red;">{message}</span>')
            self.parent._cError_count += 1
        elif "<<Warning>>" in message:
            message = message.replace("<<Warning>>", "")
            self.text_edit.append(f'<span style="color: yellow;">{message}</span>')
            self.parent._cWarning_count += 1
        else:
            if message != "" or message != "\n" or message != " ":
                self.text_edit.append(message)
                self.parent._cInfo_count += 1
            
        self.parent._update_console()

    def flush(self):  # Required method for file-like objects
        pass
    
    
class ProgressDialog(QDialog):
    def __init__(self, url, save_path, python_name):
        super().__init__()
        self.url = url
        self.save_path = save_path
        self.python_name = python_name

        self.initUI()

        

    def initUI(self):
        self.setWindowTitle("Download Progress")
        self.setGeometry(400, 400, 300, 100)
        
        # Layout for the progress bar
        layout = QVBoxLayout()

        self.label = QLabel(self)
        self.label.setText(f"Downloading {self.python_name}..")
        layout.addWidget(self.label)


        # Progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.progress_bar)

        # Set layout
        self.setLayout(layout)
        
    def Handle_Progress(self, blocknum, blocksize, totalsize):
 
        ## calculate the progress
        readed_data = blocknum * blocksize
 
        if totalsize > 0:
            download_percentage = readed_data * 100 / totalsize
            self.progress_bar.setValue(int(download_percentage))
            QApplication.processEvents()
            
    def download(self):
        from urllib.request import urlretrieve
        import webbrowser
        
        urlretrieve(self.url, self.save_path, self.Handle_Progress)
        webbrowser.open(self.save_path)
        self.close()
