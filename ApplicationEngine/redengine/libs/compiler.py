import threading, subprocess, sys, os
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class CompilerWorker(QThread):
    signalCompileStarted = pyqtSignal(bool)
    signalCompileFinished = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)


             


    def compile_to_exe(self):
        self.signalCompileStarted.emit(True)

        # Function to handle the subprocess
        def run_compilation():
            try:
                subprocess.run([sys.executable, "-m", "PyInstaller", "--onefile", self.parent.main_project_file], 
                               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print("Compilation successful.")
                self.signalCompileFinished.emit(True)
            except subprocess.CalledProcessError as e:
                QMessageBox.information(self.parent, "Compilation Failed", f"{e}", QMessageBox.Ok)
            finally:
                print("Compilation process has closed.")

        # Create a thread for the subprocess
        compile_thread = threading.Thread(target=run_compilation)
        compile_thread.start()
        self.signalCompileFinished.emit(True)


     



