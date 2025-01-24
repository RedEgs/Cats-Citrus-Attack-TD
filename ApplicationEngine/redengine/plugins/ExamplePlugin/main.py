from PyQt5.QtWidgets import QMessageBox

class Plugin():
    def __init__(self, plugin_manager):
        self._manager = plugin_manager

    def pre_init_ui(self):
        pass
        #self.blowup()

    def post_init_ui(self):
        pass

    def post_setup(self):

        app = self._manager.get_main_app()
        app.setWindowTitle("Example Plguin test")


        msg = QMessageBox()
        msg.setWindowTitle("Plugin Test!")
        msg.setText("This is an example plugin!")
        x = msg.exec_()
