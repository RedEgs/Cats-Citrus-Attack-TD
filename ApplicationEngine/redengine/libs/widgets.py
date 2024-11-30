from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import *
from PyQt5.Qsci import *
from PyQt5.QtWidgets import QWidget
import libs.process_wrapper as pw  
import traceback, sys, os, pygame
class PygameWidget(QWidget):
    def __init__(self, parent=None):
        super(PygameWidget,self).__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        
        self.can_run = False
        self.can_draw = True
        self.paused = False
        self.parent = parent

    def start_game_clock(self):
        self.timer = QTimer(self)
        self.timer.setInterval(0)
        self.timer.timeout.connect(self.redraw)
        self.timer.start()
        self.setMouseTracking(True)
        self.can_draw = True
        self.paused = False
        self.reloading = False
      
    def stop_game_clock(self):
        self.timer.stop()
        self.setMouseTracking(False)
      
    def convert_mouse_coords(self, mouse_x, mouse_y):
        """Converts the mouse coords to widgets relative coordinates"""  
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
        
        # Calculate the mouse position relative to the image
        relative_x = mouse_x - center_x
        relative_y = mouse_y - center_y
        
        # Convert the relative position to the image's coordinate system
        if 0 <= relative_x < scaled_image.width() and 0 <= relative_y < scaled_image.height():
            image_x = relative_x * self.image.width() / scaled_image.width()
            image_y = relative_y * self.image.height() / scaled_image.height()
            return [image_x, image_y]
        return [mouse_x, mouse_y]
        
    def set_process(self, file_path, project_file_path, launch_fullscreen):
        """Sets the pygame process that should be rendered to the screen.

        Args:
            process (pygame.Surface): Should return or yield a surface here for every frame.
            game: The instance of the pygame game or object.
        """
        self.file_path = file_path
        self.project_file_path = project_file_path
        self.can_run = True
        self.is_fullscreen = launch_fullscreen

        try:
            self._launch_game(file_path, project_file_path)
        except Exception as e:
            print(traceback.format_exc())
            QMessageBox.critical(self.parent, f"Fatal Error Starting Game Loop | {str(os.path.basename(traceback.extract_tb(sys.exc_info()[2])[-1].filename))}", 
                                f"{traceback.format_exc()}", QMessageBox.Ok)

    # TODO Rename this here and in `set_process`
    def _launch_game(self, file_path, project_file_path):
        self.start_game_clock()
        print("started clock")
        self.game = pw.GameHandler(file_path, project_file_path, self.is_fullscreen)
        print("init game")
        self.game.start_process()
        print("started game")




            

    def close_process(self):
        """Closes the game or object, and prevents the screen from rendering regularly (at all).
        """
        self.can_run = False
        self.game.stop_process()
        self.game = None
        self.stop_game_clock()
        self.repaint()

    def reload_process(self):
        def _reset_reload_state(self):
            self.reloading = False
            print("reset ")
        
        if hasattr(self, 'game') and not self.is_fullscreen:
            self.game.hot_reload()
            print("returned focus")
            
        self.reloading = True
            
        self.reload_timer = QTimer()
        self.reload_timer.setSingleShot(True)
        self.reload_timer.setInterval(100)
        self.reload_timer.timeout.connect(lambda: _reset_reload_state(self))
        self.reload_timer.start()
            
            
            
    def get_process(self):
        if hasattr(self, 'game'):
            return self.game.game

    def keyPressEvent(self, event):
        """Catches input from the window/widget and sends to pygame.
        """
        
        if isinstance(event, QKeyEvent) and self.can_run and not self.is_fullscreen and not self.paused:
            key_text = event.text()
            self.game.send_event("k", key_text)
            print(f"key pressed within widget: {key_text}")
            
    def mouseMoveEvent(self, event):  # sourcery skip: class-extract-method
        """Catches mouse movement from the window/widget and sends to pygame.
        """
        if self.can_run and hasattr(self, 'image') and not self.is_fullscreen and not self.paused:
            pos = event.pos()
            coords = self.convert_mouse_coords(pos.x(),  pos.y())
            if coords != [pos.x(), pos.y()]:
                self.game.send_event("mm", [coords[0], coords[1], 0])   
           
    def mousePressEvent(self, event):
        if not self.can_run or not hasattr(self, 'image') or self.is_fullscreen and not self.paused:
            return
        if event.button() == Qt.MouseButton.LeftButton:
            self.send_mousePressEvent(event, 1)
        elif event.button() == Qt.MouseButton.RightButton:
            self.send_mousePressEvent(event, 2)
        elif event.button() == Qt.MouseButton.MiddleButton:
            self.send_mousePressEvent(event, 3)   

    def mouseReleaseEvent(self, event):
        if not self.can_run or not hasattr(self, 'image') or self.is_fullscreen and not self.paused:
            return
        if event.button() == Qt.MouseButton.LeftButton:
            self.send_mouseReleaseEvent(event)
        elif event.button() == Qt.MouseButton.RightButton:
            self.send_mouseReleaseEvent(event)
        elif event.button() == Qt.MouseButton.MiddleButton:
            self.send_mouseReleaseEvent(event)   


    # TODO Rename this here and in `mousePressEvent`
    def send_mousePressEvent(self, event, arg1):
        pos = event.pos()
        coords = self.convert_mouse_coords(pos.x(),  pos.y())
        if coords != [pos.x(), pos.y()]:
            self.game.send_event("md", [coords[0], coords[1], arg1])   
            

    # TODO Rename this here and in `mouseReleaseEvent`
    def send_mouseReleaseEvent(self, event):
        pos = event.pos()
        coords = self.convert_mouse_coords(pos.x(),  pos.y())
        if coords != [pos.x(), pos.y()]:
            self.game.send_event("mu", [coords[0], coords[1], 0])   
            
                       
    def redraw(self):
        """Handles the drawing of the screen to an image
        """
        #print("No game exists")
        try:
            if self.can_run and hasattr(self, 'game') and hasattr(self.game, 'game') and not self.is_fullscreen and not self.paused:
                try:
                    self.surface = next(self.game.run_game())
                    w=self.surface.get_width()
                    h=self.surface.get_height()
                    self.data=self.surface.get_buffer().raw
                    self.image= QImage(self.data,w,h, QImage.Format_RGB32)
                except Exception as e:
                    pass
            elif self.can_run and hasattr(self, 'game') and hasattr(self.game, 'game') and self.is_fullscreen == True:
                try:
                    next(self.game.run_game())
                except StopIteration as e:

                    self.close_process() 
                    self.parent.parent().parent().parent().parent().ui._reset_play_button(True)

        except Exception as e:
            print(traceback.format_exc())

            if e not in [StopIteration, pygame.error]:
                QMessageBox.critical(self.parent, f"Fatal Error Within Render Loop | {str(os.path.basename(traceback.extract_tb(sys.exc_info()[2])[-1].filename))}", traceback.format_exc(), QMessageBox.Ok)
                #self.close_process()            
                self.parent.parent().parent().parent().parent()._reset_play_button(True)


        self.repaint()
  
    def paintEvent(self,event):
        qp = QPainter(self)
        try:
            if self.can_run and self.can_draw and hasattr(self, 'game') and hasattr(self.game, 'game') and hasattr(self, 'image') and not self.is_fullscreen:
                self._extracted_from_paintEvent_6(qp)
            else:       
                # Render a black screen with "No preview available" text
                if self.can_run and hasattr(self, 'game') and hasattr(self.game, 'game') and self.is_fullscreen == True:
                    qp.fillRect(self.rect(), QColor(0, 180, 0))  # Fill the screen with green
                    text = "Rendering in fullscreen"
                else:
                    qp.fillRect(self.rect(), QColor(0, 0, 0))  # Fill the screen with black
                    text = "No preview available"

                qp.setPen(QColor(255, 255, 255))  # Set the text color to white
                qp.setFont(self.font())  # Use the default font

                text_rect = self.rect()
                qp.drawText(text_rect, Qt.AlignCenter, text)  # Draw text centered
               
        finally:
            qp.end()  # Ensure QPainter is properly ended

    # TODO Rename this here and in `paintEvent`
    def _extracted_from_paintEvent_6(self, qp):  # sourcery skip: extract-method
        qp.fillRect(self.rect(), QColor(0, 0, 0))  # Fill the screen with black

        # Get the size of the widget (black rectangle)
        rect = self.rect()
        rect_width = rect.width()
        rect_height = rect.height()

        # Scale the image to fit the widget size
        if hasattr(self, 'image'):
            scaled_image = self.image.scaled(rect_width, rect_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Calculate the position to center the scaled image
        center_x = (rect_width - scaled_image.width()) // 2
        center_y = (rect_height - scaled_image.height()) // 2

        qp.drawImage(center_x, center_y, scaled_image)
        
        if self.paused:
            grey_out_color = QColor(0, 0, 0, 150)  # Semi-transparent black
            qp.fillRect(center_x, center_y, scaled_image.width(), scaled_image.height(), grey_out_color)

            qp.setPen(QColor(255, 255, 255))  # Set the text color to white
            qp.setFont(self.font())  # Use the default font

            text_rect = self.rect()
            qp.drawText(text_rect, Qt.AlignCenter, "Paused")  # Draw text centered
        
        elif self.reloading:
            qp.setPen(QColor(255, 255, 255))  # Set the text color to white
            qp.setFont(self.font())  # Use the default font
            
            text_rect = self.rect()
            qp.drawText(text_rect, Qt.AlignCenter, "Reloaded")  # Draw text centered

        

class QIdeWindow(QWidget):
    
    
    def __init__(self, parent_tabs:QTabWidget, filepath = None, index = None):
        super(QWidget, self).__init__(parent_tabs)
        self._parent_tabs = parent_tabs
        self._filepath = filepath
        self._index = index

        if self._filepath is None:
            self.tab_title = f"Script IDE - Untitled"
        else:
            self.tab_title = f"Script IDE - {filepath[1]}"

        self._saved = False
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
        self._parent_tabs.setTabText(self.tab_index, f"{self.tab_title}*")
    
    def load_file(self):
        import libs.resource_management as rm
        # Load contents into file 
        contents = rm.open_file(self, self._filepath[0])
        self.script_edit.setText(contents)
        
    def save_file(self):
        with open(self._filepath[0], "w") as file:
            file.write(self.script_edit.text())
        self._saved = True
        self._parent_tabs.setTabText(self.tab_index, self.tab_title)

        verticalLayout.addWidget(self) # type: ignore
         
def load_project_resources(startpath, tree, main_file_name=None, app_path=None):
    """
    Load Project structure tree
    :param startpath: 
    :param tree: 
    :return: 
    """
    import os
    from PyQt5.QtWidgets import QTreeWidgetItem
    from PyQt5.QtGui import QIcon

    
    hidden_folders = [".redengine", "__pycache__"]
    hidden_files = ["hotdump.pkl"]
    resources_items = []
    for element in os.listdir(startpath):
        path_info = f"{str(startpath)}/{element}"
        parent_itm = QTreeWidgetItem(tree, [os.path.basename(element)])
        file_type = element.split(".")

        resources_items.append(element)

        # if scenes_dir_path != None and path_info == scenes_dir_path:
        #     load_project_resources(path_info, parent_itm)
        #     parent_itm.setIcon(0, QIcon('assets/scenes_home.png'))
        #     parent_itm.setData(0, 5, "Folder")
        #     parent_itm.setData(0, 6, "Scenes")


        if os.path.isdir(path_info):
            parent_itm.setData(0, 5, "Folder")
            if load_project_resources(path_info, parent_itm) != []:
                parent_itm.setIcon(0, QIcon('assets/icons/folder-open-document.png'))
            else:
                parent_itm.setIcon(0, QIcon('assets/icons/folder-open.png'))
                
                

            if element in hidden_folders:
                parent_itm.setHidden(True)
            
        elif element == main_file_name:
            #print(element)
            parent_itm.setIcon(0, QIcon('assets/icons/document-mainpy.png'))
            parent_itm.setData(0, 5, file_type[1])
            parent_itm.setData(0, 6, "Main")
            #parent_itm.setBackground(0, QColor.fromRgb(48, 48, 48, 255))

        elif len(file_type) >= 2 and os.path.isfile(f'assets/icons/document-{file_type[len(file_type)-1]}.png'):
            parent_itm.setIcon(0, QIcon(f'assets/icons/document-{file_type[len(file_type)-1]}.png'))
            parent_itm.setData(0, 5, file_type[1])
            
            if element in hidden_files:
                parent_itm.setHidden(True)
                
        else:
            parent_itm.setIcon(0, QIcon('assets/icons/document.png'))
            parent_itm.setData(0, 5, "Empty")
            
            if element in hidden_files:
                parent_itm.setHidden(True)


    return resources_items

def reload_project_resources(startpath, tree, main_file_name, app_path):    
    os.chdir(app_path)
    tree.clear()
    return load_project_resources(startpath, tree, main_file_name, app_path)
        
def search_tree_view(tree_widget, line_edit):
    search_query = line_edit.text().lower()
    for item in tree_widget.findItems("", Qt.MatchContains):
        item.setHidden(search_query not in item.text(0).lower())
        
def get_tree_parent_path(item):
    parent = item.parent()
    if parent is None:
        return ""
    else:
        return f"{get_tree_parent_path(parent)}/{parent.data(0, 0)}"

def get_tree_item_path(working_dir, item):
    return f"{working_dir}/{get_tree_parent_path(item)}" + f"/{item.data(0, 0)}"
  



def info_box(parent, title, text):
    QMessageBox.information(parent, title, text, QMessageBox.Ok)

def error_box(parent, title, text):
    QMessageBox.critical(parent, title, text, QMessageBox.Ok)

