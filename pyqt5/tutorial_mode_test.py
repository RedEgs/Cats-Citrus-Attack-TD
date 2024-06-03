import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt

class RectangleOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._target_widget = None
        self._show_rectangle = False
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
    
    def setTargetWidget(self, widget):
        self._target_widget = widget
        self.update()
    
    def setShowRectangle(self, show):
        self._show_rectangle = show
        self.update()
    
    def paintEvent(self, event):
        if not self._target_widget or not self._show_rectangle:
            return
        
        painter = QPainter(self)
        pen = QPen(Qt.red, 3, Qt.SolidLine)
        painter.setPen(pen)
        
        button_rect = self._target_widget.geometry()
        painter.drawRect(button_rect.left(), button_rect.top(), button_rect.width(), button_rect.height())

class ExampleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setGeometry(100, 100, 300, 200)  # Set the position and size of the window
        self.setWindowTitle('Toggle Rectangle Outline Over Button')
        
        self.layout = QVBoxLayout(self)
        
        self.button = QPushButton('Click Me', self)
        self.toggle_button = QPushButton('Toggle Rectangle', self)
        
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.toggle_button)
        
        self.overlay = RectangleOverlay(self)
        self.overlay.setTargetWidget(self.button)
        self.overlay.setGeometry(self.rect())
        self.overlay.show()
        
        self.toggle_button.clicked.connect(self.toggleRectangle)
    
    def resizeEvent(self, event):
        self.overlay.setGeometry(self.rect())
        super().resizeEvent(event)
    
    def toggleRectangle(self):
        self.overlay.setShowRectangle(not self.overlay._show_rectangle)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ExampleApp()
    ex.show()
    sys.exit(app.exec_())
