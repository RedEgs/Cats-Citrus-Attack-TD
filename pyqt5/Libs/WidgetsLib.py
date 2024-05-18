
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qsci import *
import typing

class GameWidget(QWidget):
    def __init__(self,surface,parent=None):
        super(QtGui.ImageWidget,self).__init__(parent)
        w=surface.get_width()
        h=surface.get_height()
        self.data=surface.get_buffer().raw
        self.image=QtGui.QImage(self.data,w,h,QtGui.QImage.Format_RGB32)

    def paintEvent(self,event):
        qp=QtGui.QPainter()
        qp.begin(self)
        qp.drawImage(0,0,self.image)
        qp.end()

class QIdeTab(QWidget):
    def __init__(self, parent_tabs:QTabWidget, filepath, index):
        super(QWidget, self).__init__(parent_tabs)
        self._parent_tabs = parent_tabs
        self._saved = False
        self._filepath = filepath
        self.tab_title = f"Script IDE - {filepath[1]}"
        
        
        self.ide_tab = QWidget()
        self.ide_tab.setObjectName(f"ide_tab_{index}")
        
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
        self.script_edit.setAutoCompletionThreshold(3)
        self.script_edit.setAutoCompletionReplaceWord(True)
 
        self.script_edit.setLineWidth(0)
        self.script_edit.setUtf8(True) 
        self.script_edit.setTabWidth(4)
        self.script_edit.setIndentationGuides(True)  
        
        self.horizontalLayout.addWidget(self.script_edit)
        
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
      
      
#SECTION - Treeview functions    
            
def load_project_resources(startpath, tree):
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
           
            if len(file_type) >= 2 and os.path.isfile(f'assets/{file_type[len(file_type)-1]}.ico'):
                parent_itm.setIcon(0, QIcon(f'assets/{file_type[len(file_type)-1]}.ico'))
            else:
                parent_itm.setIcon(0, QIcon('assets/file.ico'))
                
    return resources_items

def reload_project_resources(previous_files=None, startpath = None, tree = None):    
    tree.clear()
    files = load_project_resources(startpath, tree)
    return files
 
       
def search_tree_view(tree_widget, line_edit):
    search_query = line_edit.text().lower()
    for item in tree_widget.findItems("", QtCore.Qt.MatchContains):
        item.setHidden(search_query not in item.text(0).lower())
        
#Se