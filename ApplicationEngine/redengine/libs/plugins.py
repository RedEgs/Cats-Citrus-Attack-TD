import os, json, importlib.util, sys, traceback
from PyQt5.QtWidgets import QMessageBox

file_dir = os.path.dirname(os.path.abspath(__file__))

class Plugin():
    def __init__(self, plugin_manager):
        self._manager = plugin_manager

    def pre_init_ui(self):
        pass

    def post_init_ui(self):
        pass

    def post_setup(self):
        pass


class PluginManager():
    def __init__(self, main_app):
        self.main_app = main_app

        self.loaded_plugins = {}
        self.plugins_dir = os.path.join(file_dir, "..", "plugins")
        self.current_phase = "Init"

        self.load_plugins()

    def ErrorMsg(self, plugin, exception):
        msg = QMessageBox()
        msg.setWindowTitle(f"Plugin Loading Error: {plugin.name}")
        msg.setIcon(QMessageBox.Icon.Critical)

        msg.setText(f"Plugin: {plugin.name}, Errored during {self.current_phase}")
        msg.setDetailedText(f"{traceback.format_exc()}")

        disable = msg.addButton("Disable", QMessageBox.YesRole)
        cont = msg.addButton("Leave Enabled and Continue", QMessageBox.NoRole)

        x = msg.exec_()

        if msg.clickedButton() == disable:
            copy = dict(self.loaded_plugins)
            del copy[plugin.name]

            self.loaded_plugins = copy
        if msg.clickedButton() == cont:
            return


    def run_func(self, obj, func_name):
        if hasattr(obj, func_name):
            # Call the function dynamically
            try:
                getattr(obj, func_name)()
            except Exception as e:
                self.ErrorMsg(obj, e)
        else:
            pass


    def load_plugins(self):
        for plugin in os.listdir(self.plugins_dir):
            plugin_path = os.path.join(self.plugins_dir, plugin)
            plugin_json = os.path.join(plugin_path, "plugin.json")
            plugin_script = os.path.join(plugin_path, "main.py")
            plugin_module_name = f"{plugin}.main"

            if not os.path.isfile(plugin_json): return
            if not os.path.isfile(plugin_script): return

            json_data = None
            with open(plugin_json, "r") as f:
                json_data = json.loads(f.read())



            spec = importlib.util.spec_from_file_location(plugin_module_name, plugin_script)
            foo = importlib.util.module_from_spec(spec) # type: ignore
            sys.modules[plugin_module_name] = foo
            spec.loader.exec_module(foo) # type: ignore

            plug_inst = foo.Plugin(self)
            plug_inst.name = f"{json_data["Name"]}"
            self.loaded_plugins[plugin] = plug_inst

    def pre_init_ui_phase(self):
        # Called after a window has been initialised,
        # But before the UI has been initialized

        print("Loading Pre-Init UI phase.")
        self.current_phase = "Pre Init UI"
        for plugin in self.loaded_plugins.values():
            self.run_func(plugin, "pre_init_ui")

    def post_init_ui_phase(self):
        # Called after the window has been initialised,
        # And after the UI has been instanced and drawn.

        print("Loading Post UI phase.")
        self.current_phase = "Post Init UI"
        for plugin in self.loaded_plugins.values():
            self.run_func(plugin, "post_init_ui")

    def post_setup_phase(self):
        # Called when the whole engine is ready to be used.
        print("<<Success>> Loading End of Setup Phase.")
        self.current_phase = "Post Setup"
        for plugin in self.loaded_plugins.values():
            self.run_func(plugin, "post_setup")

    def get_ui(self):
        if hasattr(self.main_app, "ui"):
            return self.main_app.ui
        else:
            print("UI hasn't been initialized yet!")
            return False

    def get_main_app(self):
        # Very dangerous, unregistered access to the main application
        return self.main_app
