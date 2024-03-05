    
    
    
    
    
    
# LOAD FILES PATH ====================================
# def load_project_structure(startpath, tree):
#     """
#     Load Project structure tree
#     :param startpath: 
#     :param tree: 
#     :return: 
#     """
#     import os
#     from PyQt5.QtWidgets import QTreeWidgetItem
#     from PyQt5.QtGui import QIcon
    
    
#     for element in os.listdir(startpath):
#         path_info = str(startpath) + "/" + element
#         parent_itm = QTreeWidgetItem(tree, [os.path.basename(element)])
#         file_type = element.split(".")
        
        
        
        
#         if os.path.isdir(path_info):
#             load_project_structure(path_info, parent_itm)
#             parent_itm.setIcon(0, QIcon('assets/folder.ico'))
            
#         else:
           
#             if len(file_type) >= 2 and os.path.isfile(f'assets/{file_type[len(file_type)-1]}.ico'):
#                 parent_itm.setIcon(0, QIcon(f'assets/{file_type[len(file_type)-1]}.ico'))
#             else:
#                 parent_itm.setIcon(0, QIcon('assets/file.ico'))
# ==================================================================              
                  
# Script EDIT -================================================
# self.script_edit = QsciScintilla(self.ide_tab)     
# self.script_edit.setObjectName(u"script_edit")
# self.script_edit.setGeometry(QRect(10, 10, 710, 560))
# self.script_edit.setFrameShape(QFrame.StyledPanel)
# self.script_edit.setFrameShadow(QFrame.Raised)

# self.lexer = QsciLexerPython(self.script_edit)

# self.script_edit.setMarginType(0, QsciScintilla.NumberMargin)
# self.script_edit.setMarginWidth(0, "0000")
# self.script_edit.setMarginsForegroundColor(QColor("#ff888888"))

# self.script_edit.setLexer(self.lexer)

# self.script_edit.setAutoCompletionSource(self.script_edit.AutoCompletionSource.AcsAll)
# self.script_edit.setAutoCompletionThreshold(3)
# self.script_edit.setAutoCompletionReplaceWord(True)

# self.script_edit.setLineWidth(0)
# self.script_edit.setUtf8(True) 
# self.script_edit.setTabWidth(4)
# self.script_edit.setIndentationGuides(True)       
#=======================================================================================