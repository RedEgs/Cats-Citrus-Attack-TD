from PyQt5.QtCore       import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui        import *
from PyQt5.QtWidgets    import *
from PyQt5.Qsci import *
from PyQt5.QtWidgets import QWidget
    
class PygameWidget(QWidget):
    def __init__(self, parent=None):
        super(PygameWidget,self).__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        
        self.can_run = False
        
        self.process = None
        self.game = None
        
    def set_process(self, process, game, file_path):
        """Sets the pygame process that should be rendered to the screen.

        Args:
            process (pygame.Surface): Should return or yield a surface here for every frame.
            game: The instance of the pygame game or object.
        """
        
        self._recent_args = [process, game]
        
        self.file_path = file_path
        self.process = process
        self.game = game
        self.can_run = True
        
        self.timer = QTimer(self)
        self.timer.setInterval(0)
        self.timer.timeout.connect(self.redraw)
        self.timer.start()
        self.setMouseTracking(True)
        
    def close_process(self):
        """Closes the game or object, and prevents the screen from rendering regularly (at all).
        """
        self.can_run = False
        self.process = None
        self.game = None
        
        
        self.timer.stop()
        self.repaint()
        self.setMouseTracking(False)
       
    def reload_process(self):
        self.close_process()
        self.set_process(self._recent_args[0], self._recent_args[1])
        
    def keyPressEvent(self, event):
        """Catches input from the window/widget and sends to pygame.
        """
        
        if isinstance(event, QKeyEvent) and self.can_run:
            key_text = event.text()
            print(key_text)
            self.game._send_event(key_text)
            
    def mouseMoveEvent(self, event):
        """Catches mouse movement from the window/widget and sends to pygame.
        """
        if self.can_run and hasattr(self, 'image'):
            pos = event.pos()
            mouse_x = pos.x()
            mouse_y = pos.y()
            
            # Get the size of the widget (black rectangle)
            rect = self.rect()
            rect_width = rect.width()
            rect_height = rect.height()
            
            # Scale the image to fit the widget size
            scaled_image = self.image.scaled(rect_width, rect_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # Calculate the position to center the scaled image
            center_x = (rect_width - scaled_image.width()) // 2
            center_y = (rect_height - scaled_image.height()) // 2
            
            # Calculate the mouse position relative to the image
            relative_x = mouse_x - center_x
            relative_y = mouse_y - center_y
            
            # Convert the relative position to the image's coordinate system
            if 0 <= relative_x < scaled_image.width() and 0 <= relative_y < scaled_image.height():
                image_x = relative_x * self.image.width() / scaled_image.width()
                image_y = relative_y * self.image.height() / scaled_image.height()
                
                self.game._send_event(2, None, int(image_x), int(image_y))   
                  
    def redraw(self):
        """Handles the drawing of the screen to an image
        """
        # try:
        if self.can_run:
            surface = next(self.process)
            w=surface.get_width()
            h=surface.get_height()
            self.data=surface.get_buffer().raw
            self.image= QImage(self.data,w,h, QImage.Format_RGB32)
            
            self.repaint()
        # except: pass

    def paintEvent(self,event):
        qp=QPainter()
        qp.begin(self)
            
        # try:
        if self.can_run:
            qp.fillRect(self.rect(), QColor(0, 0, 0))  # Fill the screen with black
            
            # Get the size of the widget (black rectangle)
            rect = self.rect()
            rect_width = rect.width()
            rect_height = rect.height()
            
            # Scale the image to fit the widget size
            try:
                scaled_image = self.image.scaled(rect_width, rect_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            except: pass
            # Calculate the position to center the scaled image
            center_x = (rect_width - scaled_image.width()) // 2
            center_y = (rect_height - scaled_image.height()) // 2
            
            qp.drawImage(center_x, center_y, scaled_image)
        else:
            # Render a black screen with "No preview available" text
            qp.fillRect(self.rect(), QColor(0, 0, 0))  # Fill the screen with black
            qp.setPen(QColor(255, 255, 255))  # Set the text color to white
            qp.setFont(self.font())  # Use the default font
            text = "No preview available"
            text_rect = self.rect()
            qp.drawText(text_rect, Qt.AlignCenter, text)  # Draw text centered
        qp.end()
        # except: pass
        
        
    def _get_marked_lines(self, file):
        import pickle, inspect, re
        
        
        with open(file, 'r') as file:
            line_numbers = []
            for line_num, line in enumerate(file, start=1):
                if line.strip().startswith('#'):
                    if re.search(r'\b{}\b'.format(re.escape("HOTSAVE")), line):
                        line_numbers.append(line_num)
        return line_numbers
    
    def _get_marked_vars(self, line_numbers, file_path):
        import inspect 
        
        variables = {}
        with open(file_path, 'r') as file:
            source_lines = file.readlines()
            
            for line_number in line_numbers:    
                line_index = line_number - 2  # Convert line number to zero-based index
                if line_index >= 0 and line_index < len(source_lines):
                    line = source_lines[line_index].strip()
                    if line.startswith('self.'):
                        variable_name = line.split('=')[0].strip().split('self.')[1]
                        variables[variable_name] = getattr(self.game, variable_name)
        return variables
      
    def save_process_state(self):
        import pickle
        # state = {
        #     'mouse_pos': self.mouse_pos,
        #     # Add other variables you want to save here
        # }
        
        m_lines = self._get_marked_lines(self.file_path)
        state = self._get_marked_vars(m_lines, self.file_path)

        with open("hotdump.pkl", 'wb') as f:
            pickle.dump(state, f)
        print(f"Saved game state to {f.name}")

    def load_process_state(self):
        import pickle
        
        with open("hotdump.pkl", 'rb') as f:
            state = pickle.load(f)
        for name, value in state.items():
            setattr(self.game, name, value)
        print(f"Loaded game state from {f.name}")

class QIdeWindow(QWidget):
    def __init__(self, parent_tabs:QTabWidget, filepath = None, index = None):
        super(QWidget, self).__init__(parent_tabs)
        self._parent_tabs = parent_tabs
        self._filepath = filepath
        self._index = index
        
        if self._filepath == None:
            self._saved = False
            self.tab_title = f"Script IDE - Untitled"
        else:
            self._saved = False
            self.tab_title = f"Script IDE - {filepath[1]}"
        
        self.ide_tab = QWidget()
        self.ide_tab.setObjectName(f"ide_tab")
            
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
        self.script_edit.setAutoCompletionThreshold(2)
        self.script_edit.setAutoCompletionReplaceWord(True)
 
        self.script_edit.setLineWidth(0)
        self.script_edit.setUtf8(True) 
        self.script_edit.setTabWidth(4)
        self.script_edit.setIndentationsUseTabs(False)
        self.script_edit.setAutoIndent(True)
        self.script_edit.setIndentationGuides(True)  
        
        self.horizontalLayout.addWidget(self.script_edit)
        
        self.tab_index = parent_tabs.addTab(self.ide_tab, self.tab_title)
        self.load_file()
        
        self.script_edit.textChanged.connect(self.mark_as_unsaved)
        self._parent_tabs.setCurrentIndex(self.tab_index)
        
        self._parent_tabs.tabCloseRequested.connect(self.close_tab)
    
    def close_tab(self): 
        current_widget = self._parent_tabs.indexOf(self.ide_tab)
        if self._parent_tabs.currentIndex() == current_widget:
            self._parent_tabs.removeTab(current_widget)
    
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
   
class QLogItem(QLabel):
    def __init__(self, parent: QWidget, verticalLayout = None, text = None) -> None:
        super().__init__(parent)
        

        self.setText(text)
        self.setMinimumSize(QSize(0, 50))
        self.setAutoFillBackground(True)
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Raised)
        self.setTextFormat(Qt.PlainText)
        self.setScaledContents(False)
        self.setWordWrap(False)
        self.setMargin(10)
        self.setIndent(0)

        verticalLayout.addWidget(self)
    
   
         
def load_project_resources(startpath, tree, main_file_name = None):
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
            if element == main_file_name:
                #print(element)
                parent_itm.setIcon(0, QIcon('assets/icon32.png'))
            elif len(file_type) >= 2 and os.path.isfile(f'assets/{file_type[len(file_type)-1]}.ico'):
                parent_itm.setIcon(0, QIcon(f'assets/{file_type[len(file_type)-1]}.ico'))
            else:
                parent_itm.setIcon(0, QIcon('assets/file.ico'))
        
        
                
    return resources_items

def reload_project_resources(previous_files=None, startpath = None, tree = None, main_file_name = None):    
    tree.clear()
    files = load_project_resources(startpath, tree, main_file_name)
    return files
        
def search_tree_view(tree_widget, line_edit):
    search_query = line_edit.text().lower()
    for item in tree_widget.findItems("", Qt.MatchContains):
        item.setHidden(search_query not in item.text(0).lower())
        
def get_tree_parent_path(item):
    parent = item.parent()
    if parent is None:
        return ""
    else:
        return get_tree_parent_path(parent) + "/" + parent.data(0, 0)

def get_tree_item_path(working_dir, item):
    return working_dir + f"/{get_tree_parent_path(item)}" + f"/{item.data(0, 0)}"
  
    