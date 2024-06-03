from PyQt5.QtCore       import *
from PyQt5.QtGui        import *
from PyQt5.QtWidgets    import *
    
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
            self.game.send_event(key_text)
            
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
                
                self.game.send_event(2, None, int(image_x), int(image_y))   
                  
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
            scaled_image = self.image.scaled(rect_width, rect_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
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
