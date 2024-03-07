# SEARCHING ITEMS IN A FILE TREE===============================
# def search_tree_view(tree_widget, line_edit):
#     search_query = line_edit.text().lower()
#     for item in tree_widget.findItems("", QtCore.Qt.MatchContains):
#         item.setHidden(search_query not in item.text(0).lower())
# ==============================================================================  


    
# INIT FOR CLASS =============================================================================
#  def __init__(self, project_path):
#         import json
#         # Load from project file here
#         self.project_working_path = project_path
#         self.project_json = json.load(open(f"{project_path}/project.json"))
#         self.project_name = self.project_json["project_name"]
#         print(self.project_name)
#         self.project_window_title = f"Red Engine - {self.project_name}"
# ============================================================================================   
        
    
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

# RESOURCE TREE ============================
# self.resources_tree = QTreeWidget(self.resources_dock_contents)
# __qtreewidgetitem = QTreeWidgetItem()
# __qtreewidgetitem.setText(0, u"1");
# self.resources_tree.setHeaderItem(__qtreewidgetitem)
# self.resources_tree.setObjectName(u"resources_tree")
# self.resources_tree.setGeometry(QRect(10, 30, 230, 251))
# sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
# sizePolicy1.setHorizontalStretch(0)
# sizePolicy1.setVerticalStretch(0)
# sizePolicy1.setHeightForWidth(self.resources_tree.sizePolicy().hasHeightForWidth())
# self.resources_tree.setSizePolicy(sizePolicy1)
# self.resources_tree.setContextMenuPolicy(Qt.DefaultContextMenu)
# self.resources_tree.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
# self.resources_tree.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
# self.resources_tree.setAnimated(False)
# self.resources_tree.setAllColumnsShowFocus(False)
# self.resources_tree.setColumnCount(1)
# self.resources_tree.header().setVisible(False)
# self.resources_tree_files = load_project_resources(self.project_working_path, self.resources_tree)
# =============================================================================================================

# RESOURCE SEARCH BAR =====================================================
# self.resource_search_bar = QLineEdit(self.resources_dock_contents)
# self.resource_search_bar.setObjectName(u"resource_search_bar")
# self.resource_search_bar.setGeometry(QRect(10, 3, 230, 22))
# self.resource_search_bar.setClearButtonEnabled(True)
# self.resource_search_bar_completer = QCompleter(self.resources_tree_files)
# self.resource_search_bar.setCompleter(self.resource_search_bar_completer)


# self.resource_search_bar.textChanged.connect(lambda: search_tree_view(self.resources_tree, self.resource_search_bar))


# def search_resources(self):
#     search_tree_view(self.resources_tree, self.resource_search_bar)

# =====================================================================================



# Custom Context Menus with tree widgets 
# self.resources_tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
# self.resources_tree.customContextMenuRequested.connect(self.create_resources_context_menu)

# def create_resources_context_menu(self, event):
#    menu = QMenu(self.resources_tree)
#    menu.addAction("New File")
#    menu.exec_(self.resources_tree.mapToGlobal(event))
#