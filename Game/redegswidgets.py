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
        
    def set_process(self, process, game):
        """Sets the pygame process that should be rendered to the screen.

        Args:
            process (pygame.Surface): Should return or yield a surface here for every frame.
            game: The instance of the pygame game or object.
        """
        
        self.process = process
        self.game = game
        self.can_run = True
        
        self.timer = QTimer(self)
        self.timer.setInterval(0)
        self.timer.timeout.connect(self.redraw)
        self.timer.start()
        
    def close_process(self):
        """Closes the game or object, and prevents the screen from rendering regularly (at all).
        """
        self.process = None
        self.game = None
        self.can_run = False
        
        self.timer.stop()
        self.repaint()
        
        
    def keyPressEvent(self, event):
        """Catches input from the window/widget and sends to pygame.
        """
        
        if isinstance(event, QKeyEvent) and self.can_run:
            key_text = event.text()
            print(key_text)
            self.game.send_key(key_text)
            
    def redraw(self):
        """Handles the drawing of the screen to an image
        """
        
        if self.can_run:
            surface = next(self.process)
            w=surface.get_width()
            h=surface.get_height()
            self.data=surface.get_buffer().raw
            self.image= QImage(self.data,w,h, QImage.Format_RGB32)
            
            self.repaint()

    def paintEvent(self,event):
        qp=QPainter()
        qp.begin(self)
            
        if self.can_run:
            qp.drawImage(0,0,self.image)
        else:
            # Render a black screen with "No preview available" text
            qp.fillRect(self.rect(), QColor(0, 0, 0))  # Fill the screen with black
            qp.setPen(QColor(255, 255, 255))  # Set the text color to white
            qp.setFont(self.font())  # Use the default font
            text = "No preview available"
            text_rect = self.rect()
            qp.drawText(text_rect, Qt.AlignCenter, text)  # Draw text centered
        qp.end()