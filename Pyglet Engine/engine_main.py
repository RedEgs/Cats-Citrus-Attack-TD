# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitledMzlQEK.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from libs.WidgetsLib import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qsci import *

import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets
from pathlib import Path

#creds to https://github.com/art1415926535/PyQt5-syntax-highlighting/blob/master/example.py
#creds to https://qscintilla.com/#margins/margin_basics/symbol_margin
#creds to https://www.softicons.com/toolbar-icons/must-have-icons-by-visualpharm/new-icon
    # https://www.softicons.com/toolbar-icons/must-have-icons-by-visualpharm


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
        


        

class Ui_main_window(object):
    def __init__(self, project_path):
        import json
        # Load from project file here
        self.project_working_path = project_path
        self.project_json = json.load(open(f"{project_path}/project.json"))
        self.project_name = self.project_json["project_name"]
        print(self.project_name)
        self.project_window_title = f"Red Engine - {self.project_name}"
        
        self.ide_tabs = []
        
    def setupUi(self, main_window):
        if not main_window.objectName():
            main_window.setObjectName(u"main_window")
        main_window.resize(1280, 737)
        main_window.setMinimumSize(QSize(1280, 720))
        self.actionSave = QAction(main_window)
        self.actionSave.setObjectName(u"actionSave")
        icon = QIcon()
        icon.addFile(u"assets/10125_icons/imageres_28.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.actionSave.setIcon(icon)
        self.actionSave_as = QAction(main_window)
        self.actionSave_as.setObjectName(u"actionSave_as")
        icon1 = QIcon()
        icon1.addFile(u"assets/10125_icons/imageres_29.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.actionSave_as.setIcon(icon1)
        self.actionNew_Project = QAction(main_window)
        self.actionNew_Project.setObjectName(u"actionNew_Project")
        icon2 = QIcon()
        icon2.addFile(u"assets/10125_icons/shell32_264.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.actionNew_Project.setIcon(icon2)
        self.actionOpen_Project = QAction(main_window)
        self.actionOpen_Project.setObjectName(u"actionOpen_Project")
        icon3 = QIcon()
        icon3.addFile(u"assets/10125_icons/imageres_1025.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.actionOpen_Project.setIcon(icon3)
        self.actionRecent_Projects = QAction(main_window)
        self.actionRecent_Projects.setObjectName(u"actionRecent_Projects")
        icon4 = QIcon()
        icon4.addFile(u"assets/10125_icons/imageres_185.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.actionRecent_Projects.setIcon(icon4)
        self.actionRun_Project = QAction(main_window)
        self.actionRun_Project.setObjectName(u"actionRun_Project")
        icon5 = QIcon()
        icon5.addFile(u"assets/10125_icons/Play.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.actionRun_Project.setIcon(icon5)
        self.actionResources = QAction(main_window)
        self.actionResources.setObjectName(u"actionResources")
        self.actionResources.setCheckable(True)
        self.actionResources.setChecked(True)
        icon6 = QIcon()
        icon6.addFile(u"assets/10125_icons/Folder.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.actionResources.setIcon(icon6)
        self.actionAssets_Library = QAction(main_window)
        self.actionAssets_Library.setObjectName(u"actionAssets_Library")
        self.actionAssets_Library.setCheckable(True)
        self.actionAssets_Library.setChecked(True)
        icon7 = QIcon()
        icon7.addFile(u"assets/10125_icons/rar.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.actionAssets_Library.setIcon(icon7)
        self.actionProperties = QAction(main_window)
        self.actionProperties.setObjectName(u"actionProperties")
        self.actionProperties.setCheckable(True)
        self.actionProperties.setChecked(True)
        icon8 = QIcon()
        icon8.addFile(u"assets/10125_icons/imageres_5366.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.actionProperties.setIcon(icon8)
        self.actionUndo = QAction(main_window)
        self.actionUndo.setObjectName(u"actionUndo")
        icon9 = QIcon()
        icon9.addFile(u"assets/10125_icons/imageres_5315.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.actionUndo.setIcon(icon9)
        self.actionRedo = QAction(main_window)
        self.actionRedo.setObjectName(u"actionRedo")
        icon10 = QIcon()
        icon10.addFile(u"assets/10125_icons/imageres_5311.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.actionRedo.setIcon(icon10)
        self.actionVisit_Source = QAction(main_window)
        self.actionVisit_Source.setObjectName(u"actionVisit_Source")
        icon11 = QIcon()
        icon11.addFile(u"assets/10125_icons/link.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.actionVisit_Source.setIcon(icon11)
        self.actionNew_File = QAction(main_window)
        self.actionNew_File.setObjectName(u"actionNew_File")
        icon12 = QIcon()
        icon12.addFile(u"assets/10125_icons/Add.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.actionNew_File.setIcon(icon12)
        self.actionNew_Folder = QAction(main_window)
        self.actionNew_Folder.setObjectName(u"actionNew_Folder")
        self.actionNew_Folder.setIcon(icon12)
        self.central_widget = QWidget(main_window)
        self.central_widget.setObjectName(u"central_widget")
        self.central_tabs = QTabWidget(self.central_widget)
        self.central_tabs.setObjectName(u"central_tabs")
        self.central_tabs.setGeometry(QRect(0, 0, 770, 701))
        self.viewport_tab = QWidget()
        self.viewport_tab.setObjectName(u"viewport_tab")
        icon13 = QIcon()
        icon13.addFile(u"assets/10125_icons/shell32_35.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.central_tabs.addTab(self.viewport_tab, icon13, "")
        self.actionDelete_Resource = QAction(main_window)
        self.actionDelete_Resource.setObjectName(u"actionDelete_Resource")
        icon13 = QIcon()
        icon13.addFile(u"assets/10125_icons/Delete.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.actionDelete_Resource.setIcon(icon13)
        
        
        
        self.scripting_tab = QWidget()
        self.scripting_tab.setObjectName(u"scripting_tab")
        
        self.script_tabs = QTabWidget(self.scripting_tab)
        self.script_tabs.setObjectName(u"script_tabs")
        self.script_tabs.setGeometry(QRect(10, 5, 740, 661))
        self.script_tabs.setTabPosition(QTabWidget.North)
        self.script_tabs.setTabShape(QTabWidget.Rounded)
        self.script_tabs.setElideMode(Qt.ElideLeft)
        self.script_tabs.setUsesScrollButtons(True)
        self.script_tabs.setTabsClosable(True)
        self.script_tabs.tabCloseRequested.connect(lambda index: self._close_ide_tab(index))
        
        
        
        self.vscript_tab = QWidget()
        self.vscript_tab.setObjectName(u"vscript_tab")
        self.vscript_workspace = QGraphicsView(self.vscript_tab)
        self.vscript_workspace.setObjectName(u"vscript_workspace")
        self.vscript_workspace.setGeometry(QRect(10, 10, 710, 600))
        icon14 = QIcon()
        icon14.addFile(u"assets/10125_icons/imageres_5365.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.script_tabs.addTab(self.vscript_tab, icon14, "")

        self.ide_tab = QWidget()
        self.ide_tab.setObjectName(u"ide_tab")
        self.script_edit = QPlainTextEdit(self.ide_tab)
        self.script_edit.setObjectName(u"script_edit")
        self.script_edit.setGeometry(QRect(10, 9, 710, 611))
        self.script_edit.setFrameShape(QFrame.StyledPanel)
        self.script_edit.setFrameShadow(QFrame.Raised)
        self.script_edit.setLineWidth(0)
        self.script_edit.setAcceptDrops(True)

        
        
        icon15 = QIcon()
        icon15.addFile(u"assets/10125_icons/Text Document.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.script_tabs.addTab(self.ide_tab, icon15, "")
        icon16 = QIcon()
        icon16.addFile(u"assets/10125_icons/script.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.central_tabs.addTab(self.scripting_tab, icon16, "")
        main_window.setCentralWidget(self.central_widget)
        self.resources_dock = QDockWidget(main_window)
        self.resources_dock.setObjectName(u"resources_dock")
        self.resources_dock.setMinimumSize(QSize(250, 320))
        self.resources_dock.setMaximumSize(QSize(250, 320))
        self.resources_dock.setBaseSize(QSize(250, 350))
        font = QFont()
        font.setUnderline(False)
        self.resources_dock.setFont(font)
        self.resources_dock.setAutoFillBackground(True)
        self.resources_dock.setFloating(False)
        self.resources_dock.setFeatures(QDockWidget.AllDockWidgetFeatures)
        self.resources_dock.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        self.resources_dock_contents = QWidget()
        self.resources_dock_contents.setObjectName(u"resources_dock_contents")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.resources_dock_contents.sizePolicy().hasHeightForWidth())
        self.resources_dock_contents.setSizePolicy(sizePolicy)
        self.resources_dock_contents.setMinimumSize(QSize(0, 350))
        self.resources_dock_contents.setAutoFillBackground(False)

        self.resources_tree = QTreeWidget(self.resources_dock_contents)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.resources_tree.setHeaderItem(__qtreewidgetitem)
        self.resources_tree.setObjectName(u"resources_tree")
        self.resources_tree.setGeometry(QRect(10, 30, 230, 251))
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.resources_tree.sizePolicy().hasHeightForWidth())
        self.resources_tree.setSizePolicy(sizePolicy1)
        self.resources_tree.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.resources_tree.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.resources_tree.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.resources_tree.setAnimated(False)
        self.resources_tree.setAllColumnsShowFocus(False)
        self.resources_tree.setColumnCount(1)
        self.resources_tree.setDragDropMode(QAbstractItemView.DragOnly)
        self.resources_tree.header().setVisible(False)
        self.resources_tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.resources_tree.customContextMenuRequested.connect(self.create_resources_context_menu)
        self.resources_tree_files = load_project_resources(self.project_working_path, self.resources_tree)
        
        self.resources_tree.itemClicked.connect(self._select_item_resources_tree)
        self.resources_tree.itemDoubleClicked.connect(self._open_in_editor)
        
        
        self.actionNew_File.triggered.connect(self._create_file_resources_tree)
        self.actionNew_Folder.triggered.connect(self._create_folder_resources_tree)
        self.actionDelete_Resource.triggered.connect(self._delete_file_resources_tree)
        
        
        
        
        self.resource_search_bar = QLineEdit(self.resources_dock_contents)
        self.resource_search_bar.setObjectName(u"resource_search_bar")
        self.resource_search_bar.setGeometry(QRect(10, 3, 131, 22))
        self.resource_search_bar.setClearButtonEnabled(True)
        self.resources_sort_button = QPushButton(self.resources_dock_contents)
        self.resources_sort_button.setObjectName(u"resources_sort_button")
        self.resources_sort_button.setGeometry(QRect(150, 3, 91, 23))
        self.resources_dock.setWidget(self.resources_dock_contents)
        main_window.addDockWidget(Qt.LeftDockWidgetArea, self.resources_dock)
        self.assets_library_dock = QDockWidget(main_window)
        self.assets_library_dock.setObjectName(u"assets_library_dock")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.assets_library_dock.sizePolicy().hasHeightForWidth())
        self.assets_library_dock.setSizePolicy(sizePolicy2)
        self.assets_library_dock.setMinimumSize(QSize(250, 150))
        self.assets_library_dock.setMaximumSize(QSize(250, 400))
        self.assets_library_dock.setBaseSize(QSize(250, 350))
        self.assets_library_dock.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea|Qt.TopDockWidgetArea)
        self.assets_library_dock_contents = QWidget()
        self.assets_library_dock_contents.setObjectName(u"assets_library_dock_contents")
        self.assets_library_listview = QTableView(self.assets_library_dock_contents)
        self.assets_library_listview.setObjectName(u"assets_library_listview")
        self.assets_library_listview.setGeometry(QRect(10, 30, 230, 311))
        self.assets_library_listview.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.assets_library_search_bar = QLineEdit(self.assets_library_dock_contents)
        self.assets_library_search_bar.setObjectName(u"assets_library_search_bar")
        self.assets_library_search_bar.setGeometry(QRect(10, 3, 230, 22))
        self.assets_library_search_bar.setClearButtonEnabled(True)
        self.assets_library_dock.setWidget(self.assets_library_dock_contents)
        main_window.addDockWidget(Qt.LeftDockWidgetArea, self.assets_library_dock)
        self.properties_dock = QDockWidget(main_window)
        self.properties_dock.setObjectName(u"properties_dock")
        self.properties_dock.setMinimumSize(QSize(250, 250))
        self.properties_dock.setMaximumSize(QSize(250, 524287))
        self.properties_dock.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea|Qt.TopDockWidgetArea)
        self.properties_dock_contents = QWidget()
        self.properties_dock_contents.setObjectName(u"properties_dock_contents")
        self.properties_dock.setWidget(self.properties_dock_contents)
        main_window.addDockWidget(Qt.RightDockWidgetArea, self.properties_dock)
        self.menu_bar = QMenuBar(main_window)
        self.menu_bar.setObjectName(u"menu_bar")
        self.menu_bar.setGeometry(QRect(0, 0, 1280, 26))
        self.project_button = QMenu(self.menu_bar)
        self.project_button.setObjectName(u"project_button")
        self.windows_button = QMenu(self.menu_bar)
        self.windows_button.setObjectName(u"windows_button")
        self.help_button = QMenu(self.menu_bar)
        self.help_button.setObjectName(u"help_button")
        self.menuEdit = QMenu(self.menu_bar)
        self.menuEdit.setObjectName(u"menuEdit")
        main_window.setMenuBar(self.menu_bar)
        QWidget.setTabOrder(self.resources_tree, self.resource_search_bar)

        self.menu_bar.addAction(self.project_button.menuAction())
        self.menu_bar.addAction(self.menuEdit.menuAction())
        self.menu_bar.addAction(self.windows_button.menuAction())
        self.menu_bar.addAction(self.help_button.menuAction())
        self.project_button.addAction(self.actionNew_Project)
        self.project_button.addAction(self.actionOpen_Project)
        self.project_button.addAction(self.actionRecent_Projects)
        self.project_button.addSeparator()
        self.project_button.addAction(self.actionSave)
        self.project_button.addAction(self.actionSave_as)
        self.windows_button.addAction(self.actionResources)
        self.windows_button.addAction(self.actionAssets_Library)
        self.windows_button.addAction(self.actionProperties)
        self.help_button.addAction(self.actionVisit_Source)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)


        self.actionSave.triggered.connect(self._save_file_in_editor)




        self.retranslateUi(main_window)

        self.central_tabs.setCurrentIndex(1)
        self.script_tabs.setCurrentIndex(1)

        
        QMetaObject.connectSlotsByName(main_window)
    # setupUi

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(QCoreApplication.translate("main_window", u"Red Engine - {project name}", None))
        self.actionSave.setText(QCoreApplication.translate("main_window", u"Save ", None))
#if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(QCoreApplication.translate("main_window", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave_as.setText(QCoreApplication.translate("main_window", u"Save as", None))
#if QT_CONFIG(shortcut)
        self.actionSave_as.setShortcut(QCoreApplication.translate("main_window", u"Ctrl+Shift+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionNew_Project.setText(QCoreApplication.translate("main_window", u"New Project", None))
        self.actionOpen_Project.setText(QCoreApplication.translate("main_window", u"Open Project", None))
        self.actionDelete_Resource.setText(QCoreApplication.translate("main_window", u"Delete Resource", None))
        self.actionRecent_Projects.setText(QCoreApplication.translate("main_window", u"Recent Projects", None))
        self.actionRun_Project.setText(QCoreApplication.translate("main_window", u"Run Project", None))
        self.actionResources.setText(QCoreApplication.translate("main_window", u"Resources", None))
        self.actionAssets_Library.setText(QCoreApplication.translate("main_window", u"Assets Library", None))
        self.actionProperties.setText(QCoreApplication.translate("main_window", u"Properties", None))
        self.actionUndo.setText(QCoreApplication.translate("main_window", u"Undo", None))
        self.actionRedo.setText(QCoreApplication.translate("main_window", u"Redo", None))
        self.actionVisit_Source.setText(QCoreApplication.translate("main_window", u"Visit Source", None))
        self.actionNew_File.setText(QCoreApplication.translate("main_window", u"New File", None))
        self.actionNew_Folder.setText(QCoreApplication.translate("main_window", u"New Folder", None))
        self.central_tabs.setTabText(self.central_tabs.indexOf(self.viewport_tab), QCoreApplication.translate("main_window", u"Game (Viewport)", None))
        self.script_tabs.setTabText(self.script_tabs.indexOf(self.vscript_tab), QCoreApplication.translate("main_window", u"Visual Script (VScript)", None))
        self.script_edit.setPlaceholderText(QCoreApplication.translate("main_window", u"Double click a file to open it in the code editor...", None))
        self.script_tabs.setTabText(self.script_tabs.indexOf(self.ide_tab), QCoreApplication.translate("main_window", u"Script IDE", None))
        self.central_tabs.setTabText(self.central_tabs.indexOf(self.scripting_tab), QCoreApplication.translate("main_window", u"Scripting", None))
        self.resources_dock.setWindowTitle(QCoreApplication.translate("main_window", u"Resources", None))
        self.resource_search_bar.setPlaceholderText(QCoreApplication.translate("main_window", u"Search...", None))
        self.resources_sort_button.setText(QCoreApplication.translate("main_window", u"Sort By Type", None))
        self.assets_library_dock.setWindowTitle(QCoreApplication.translate("main_window", u"Assets Library", None))
        self.assets_library_search_bar.setPlaceholderText(QCoreApplication.translate("main_window", u"Search...", None))
        self.properties_dock.setWindowTitle(QCoreApplication.translate("main_window", u"Properties", None))
        self.project_button.setTitle(QCoreApplication.translate("main_window", u"Project", None))
        self.windows_button.setTitle(QCoreApplication.translate("main_window", u"Windows", None))
        self.help_button.setTitle(QCoreApplication.translate("main_window", u"Help", None))
        self.menuEdit.setTitle(QCoreApplication.translate("main_window", u"Edit", None))
    # retranslateUi


    def _close_ide_tab(self, index):
        self.script_tabs.removeTab(index)
        
        try: self.ide_tabs.pop(index-2)
        except IndexError:pass

    def _open_in_editor(self, item):
        path = get_tree_item_path(self.project_working_path, item).replace("//", "/")
        self.resources_tree_dselected_item = [path , item.data(0,0)]
       
        if os.path.isfile(self.resources_tree_dselected_item[0]):
            self.ide_index = 0
            self.ide_index +=1
        
            new_ide_tab = QIdeTab(self.script_tabs, self.resources_tree_dselected_item, self.ide_index)
            text_edit = new_ide_tab.script_edit
            self.ide_tabs.append(new_ide_tab)
       
    def _save_file_in_editor(self):
        focused = QtWidgets.QApplication.focusWidget()

        if focused.__class__ == QsciScintilla:
            for tab in self.ide_tabs:
                tab.save_file()
        else:
            print("saved project")
            
    def _select_item_resources_tree(self, item:QTreeWidgetItem):
        self.resources_tree_selected_item = self.project_working_path + "/" + item.data(0,0)

    def _delete_file_resources_tree(self, event):
        item = self.resources_tree_selected_item_from_context
        path = get_tree_item_path(self.project_working_path, item)

        delete_file(self, path)
        self.resources_tree_files = reload_project_resources(self.resources_tree_files, self.project_working_path, self.resources_tree)
      
    def _create_file_resources_tree(self, event):
        item = self.resources_tree_selected_item_from_context
        path = self.project_working_path
        
        if item != None:
            if not os.path.isfile(self.project_working_path + f"/{item.data(0, 0)}"):
                path = get_tree_item_path(self.project_working_path, item)
                
        create_file(main_window, path)
        self.resources_tree_files = reload_project_resources(self.resources_tree_files, self.project_working_path, self.resources_tree)
      
    def _create_folder_resources_tree(self, event):
        item = self.resources_tree_selected_item_from_context
        path = self.project_working_path
        
        print(path)
        
        if item != None:
            path = get_tree_item_path(self.project_working_path, item) #self.project_working_path + f"/{get_tree_parent_path(item)}" + f"/{item.data(0, 0)}"
            self.resources_tree.expandItem(item)
      
        
        create_folder(main_window, path)
        self.resources_tree_files = reload_project_resources(self.resources_tree_files, self.project_working_path, self.resources_tree)
            
    def create_resources_context_menu(self, event):
        menu = QMenu(self.resources_tree)
        
        menu.addAction(self.actionNew_File)
        menu.addAction(self.actionNew_Folder)
        menu.addAction(self.actionDelete_Resource)

        self.resources_tree_selected_item_from_context = self.resources_tree.itemAt(event)


        menu.exec_(self.resources_tree.mapToGlobal(event))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
 
    main_window = QtWidgets.QMainWindow()
    ui = Ui_main_window(str(os.getcwd())+"/example")

    ui.setupUi(main_window)
    main_window.show()

    sys.exit(app.exec_())