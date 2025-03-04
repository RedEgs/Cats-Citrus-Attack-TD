from PyQt5.QtWidgets import QMessageBox

class Plugin():
    def __init__(self, plugin_manager):
        self._manager = plugin_manager
        self.tick = 0

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

    def on_game_start(self, fullscreen):
        print(f"Plugin Fullscreen status: {fullscreen}")

    def on_file_change(self, is_main, file):
        print(f"Plugin File Change: {file}")

    def on_game_tick(self):
        # self.tick += 1
        # print(f"game ticked: {self.tick}")
        pass


    def on_game_frame_draw(self, frame):
        pass
        #print(f"fame drawn: {frame}")

    def on_game_input_event(self, event):
        print(f"plugin input: {event}")
