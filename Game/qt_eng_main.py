from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from qt_design import Ui_MainWindow

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


from engine.app import *
from engine.libs import SceneService as SceneService
import qt_main, os

class PygameWindowTest(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
       

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.start_button.clicked.connect(self._start_pygame_window)
        self.ui.stop_button.clicked.connect(self._stop_pygame_window)
      
      
    def _start_pygame_window(self):
        self.game = qt_main.Main(True, True)
        self.ui.pygame_widget.set_process(game=self.game, process=self.game.qt_run())
        
    def _stop_pygame_window(self):
        self.ui.pygame_widget.close_process()
        self.game.close_game()
        
        
        
if __name__ == "__main__":
   app = QApplication([])
   widget = PygameWindowTest()
   widget.show()
   
   app.exec_() 