
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qsci import *
import typing


class QIdeTab(QWidget):
    def __init__(self, parent_tabs:QTabWidget, filepath, index):
        super(QWidget, self).__init__(parent_tabs)
        self._parent_tabs = parent_tabs
        self._saved = False
        self._filepath = filepath
        self.tab_title = f"Script IDE - {filepath[1]}"
        
        
        self.ide_tab = QWidget()
        self.ide_tab.setObjectName(f"ide_tab_{index}")
        
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
        self.script_edit.setAutoCompletionThreshold(3)
        self.script_edit.setAutoCompletionReplaceWord(True)
 
        self.script_edit.setLineWidth(0)
        self.script_edit.setUtf8(True) 
        self.script_edit.setTabWidth(4)
        self.script_edit.setIndentationGuides(True)  
        
        self.tab_index = parent_tabs.addTab(self.ide_tab, self.tab_title)
        self.load_file()
        
        self.script_edit.textChanged.connect(self.mark_as_unsaved)
        self._parent_tabs.setCurrentIndex(self.tab_index)
        
    
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