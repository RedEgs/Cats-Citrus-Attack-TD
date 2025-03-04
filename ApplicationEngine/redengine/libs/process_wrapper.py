import sys, importlib, pickle, pygame, hashlib, os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pyredengine import PreviewMain # type: ignore
from functools import partial

class GameHandler():
    def __init__(self, main_file_path: str, project_file_path: str, launch_fullscreen: bool = False, project_data = None) -> None:
        self.main_file_path = main_file_path
        self.project_file_path = project_file_path
        self.process_attached = False
        self.is_fullscreen = launch_fullscreen
        self.hotdump_location = f"{self.project_file_path}/.redengine/hotdump"
        self.project_data = project_data
        self.plugin_manager = None

        self.exclusion_list = [""]
        self.type_exclusions = [pygame.surface.Surface, pygame.Clock, self.__class__]


        print("intialised handler succesfulay ")

    def start_process(self):  # sourcery skip: class-extract-method
        import importlib.util

        print("starting handle")
        print("Starting Process")
        try:
            print("Before inserting path")
            sys.path.append(self.project_file_path) # Makes the project directory importable
            print(f"Importing Path: {self.project_file_path}")

            try:
                import main  # type: ignore # Import the main project file
                print("Importing File")
            except Exception as e:
                print(f"Error importing main: {e}")

            try:
                self.hotload_modules()
                importlib.reload(main)  # Reload imports, which will update new code





















                print("Reloading Import")
            except Exception as e:
                print(f"Error reloading main: {e}")
        except Exception as e:
            print(f"Error in setup: {e}")

        print("Before Instancing Game")


        self.game: PreviewMain.MainGame = main.Main(fullscreen=self.is_fullscreen) # Instance the game within the handler
        self.game.engine_mode = True
        self.game.__parent = self
        print("After Instancing Game")


        self.process_attached = True

        print("Started Process ")

    def stop_process(self):
        self.game.close_game()
        self.game = None
        self.process_attached = False
        self.is_app_process = False


    def hotload_modules(self):
        import os
        try:
            modules = self.project_data["project_libraries"]
        except: modules = []

        blacklisted_modules = [
            "builtins", "importlib", "_frozen_importlib", "_frozen_importlib_external"
        ]

        for module_name, module in list(sys.modules.items()):
            if not module:
                continue  # Skip uninitialized modules

            if (
                any(module_name.startswith(bl) for bl in blacklisted_modules)
                or module_name in sys.builtin_module_names
            ):
                # Skip blacklisted and built-in modules
                continue

            try:
                if modules == None or len(modules) == 0:
                    pass
                else:
                    for path in modules:
                        if os.path.basename(path) in module_name:
                            importlib.reload(module)
            except: pass

    def hot_reload(self):
        print("started hot reload")

        sys.path.insert(0, self.project_file_path) # Makes the project directory importable
        import main, os # type: ignore # Import the main project file
        self.save_process_state() # Save the process state

        self.hotload_modules()
        importlib.reload(main) # Reload imports, which will update new code





        os.chdir(self.project_file_path)
        print("set working path: " + os.getcwd())

        self.game: PreviewMain.MainGame = main.Main(self.is_fullscreen)
        self.load_process_state(self.game)

        # self.game.engine_mode = True
        # self.game.__parent = self



        print("function finished")

    def send_event(self, id, event):
        self.plugin_manager.on_game_input_event(event)

        if type(event) == str and id == "k":
            self.game._send_event(1, event)
        elif type(event) == tuple or type(event) == list and id == "mm":
            self.game._send_event(2, None, [int(event[0]), int(event[1]), int(event[2])])
        if type(event) == tuple or type(event) == list and id == "md":
            self.game._send_event(3, None, [int(event[0]), int(event[1]), int(event[2])])
        elif type(event) == list and id == "mu":
            self.game._send_event(4, None, [int(event[0]), int(event[1]), 0])

    def run_game(self):
        return self.game.run_game()

    def debug_info(self):

        if self.game is None:
            return False


        fps = self.game.clock.get_fps()
        delta_time = self.game.get_dt()/1000
        blit_count = self.game.get_total_blits()
        current_tick = self.game.get_tick()
        bps = self.game.get_bps()
        draw_count = self.game.get_draw_calls()
        dps = self.game.get_dps()


        return [delta_time, fps, blit_count, current_tick, bps, draw_count, dps]

    def get_game_process(self):
        return self.game

    def get_main_display(self) -> pygame.display: # type: ignore
        return self.game.display

    def _get_properties(self):#
        return self.game._obtain_user_vars()

    def _get_all_vars(self):
        return {
            attr: getattr(self.game, attr)
            for attr in dir(self.game)
            if not attr.startswith('__')  # Skip dunder methods
            and not callable(getattr(self.game, attr))  # Skip callable attributes
            and attr.startswith('_h_')  # Only get variables that start with '_h_'
            and attr not in self.exclusion_list  # Skip excluded variables
        }

    def _filter_and_serialize_vars(self, vars_dict):
        serialized_vars = {}

        for var_name, value in vars_dict.items():
            # Check if the variable's type is in the exclusion list
            if isinstance(value, tuple(self.type_exclusions)):
                print(f"Skipping serialization for excluded type: {var_name} of type {type(value).__name__}")
                continue

            # Skip serialization if the variable name is in the exclusion list
            if var_name in self.exclusion_list:
                print(f"Skipping serialization for excluded variable: {var_name}")
                continue

            # If it’s a valid variable, serialize it
            serialized_vars[var_name] = value

        return serialized_vars

    def save_process_state(self):
        # Parse the AST of the current file and search for #HOTSAVE commented variables
        hot_saves = self._find_hot_save_variables()


        with open(self.hotdump_location, 'wb') as f:
            pickle.dump(hot_saves, f)  # Serialize the hot-saved variables

    def load_process_state(self, game):
        with open(self.hotdump_location, 'rb') as f:
            state = pickle.load(f)  # Load the serialized variables

        for name, value in state[0].items():
            setattr(game, name, value)
            print(f"set {name} to {value}")


        #game._hot_load_modules(self.project_data["project_libraries"]) # load all the modules
        game.on_reload()  # Call a reload function in the game if necessary


    def _find_hot_save_variables(self):  # sourcery skip: low-code-quality
        import ast
        """Parse the current file and find variable assignments with '#HOTSAVE' comment."""
        hot_save_vars = {}
        public_vars = []
        unpacked_vars = []

        with open(self.main_file_path, "r") as source:
            source_code = source.read()

        tree = ast.parse(source_code)

        for node in ast.walk(tree):
            # Look for attribute assignments (e.g., self._h_angle)
            if isinstance(node, ast.Assign):
                # Find the line number and check for the '#HOTSAVE' comment
                if hasattr(node, 'lineno'):
                    line_num = node.lineno
                    lines = source_code.splitlines()
                    if line_num <= len(lines) and "#[HOTSAVE]" in lines[line_num - 1]:
                        # Handle instance variables like self._h_var
                        for target in node.targets:
                            if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name):
                                if target.value.id == "self":  # Detect instance variables
                                    var_name = target.attr
                                    try:
                                        var_value = getattr(self.game, var_name)#eval(compile(ast.Expression(node.value), '<string>', 'eval'))
                                        public_vars.append(var_name)
                                        hot_save_vars[var_name] = var_value

                                    except Exception as e:
                                        print(f"Error evaluating {var_name}: {e}")

                    elif line_num <= len(lines) and "#[PUBLIC]" in lines[line_num - 1]:
                        # Handle instance variables like self._h_var
                        for target in node.targets:
                            if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name):
                                if target.value.id == "self":  # Detect instance variables
                                    var_name = target.attr
                                    try:
                                        public_vars.append(var_name)
                                    except Exception as e:
                                        print(f"Error evaluating {var_name}: {e}")

                    elif line_num <= len(lines) and "#[UNPACK]" in lines[line_num - 1]:
                        # Handle instance variables like self._h_var
                        for target in node.targets:
                            if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name):
                                if target.value.id == "self":  # Detect instance variables
                                    var_name = target.attr
                                    try:
                                        unpacked_vars.append(var_name)
                                        public_vars.append(var_name)
                                    except Exception as e:
                                        print(f"Error evaluating {var_name}: {e}")


        return hot_save_vars, public_vars, unpacked_vars


class Vector3Widget(QWidget):
    stateChanged = pyqtSignal(str, str, str)  # Custom signal to emit when any value changes

    def __init__(self, x=0, y=0, z=0, parent=None):
        super().__init__(parent)

        # Create LineEdits for X, Y, and Z values
        self.line_x = QLineEdit(str(x))
        self.line_y = QLineEdit(str(y))
        self.line_z = QLineEdit(str(z))

        # Create Labels for X, Y, and Z
        self.label_x = QLabel("X:")
        self.label_y = QLabel("Y:")
        self.label_z = QLabel("Z:")

        # Connect text changes to a custom handler
        self.l1_con = self.line_x.editingFinished.connect(self.emit_state_changed)
        self.l2_con = self.line_y.editingFinished.connect(self.emit_state_changed)
        self.l3_con = self.line_z.editingFinished.connect(self.emit_state_changed)

        # Set a layout and add Labels and LineEdits
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for a clean fit

        # Add labels and line edits to the layout
        layout.addWidget(self.label_x)
        layout.addWidget(self.line_x)
        layout.addWidget(self.label_y)
        layout.addWidget(self.line_y)
        layout.addWidget(self.label_z)
        layout.addWidget(self.line_z)

        # Set stretch factors to make all LineEdits fit equally
        layout.setStretch(1, 1)  # Stretch X field
        layout.setStretch(3, 1)  # Stretch Y field
        layout.setStretch(5, 1)  # Stretch Z field

        # Set the layout for this widget
        self.setLayout(layout)

    def emit_state_changed(self):
        # Emit custom signal with current values when any field changes
        self.stateChanged.emit(self.line_x.text(), self.line_y.text(), self.line_z.text())

    def update_value(self, value: tuple):
        self.line_x.setText(str(value[0]))
        self.line_y.setText(str(value[1]))
        self.line_z.setText(str(value[2]))

    def get_val(self):
        return (int(self.line_x.text()), int(self.line_y.text()), int(self.line_z.text()))

class Color3Widget(Vector3Widget):
    stateChanged = pyqtSignal(pygame.Color)  # Custom signal to emit when any value changes

    def __init__(self, x=0, y=0, z=0, parent=None):
        super().__init__(x=x, y=y, z=z, parent=None)

        self.label_x.setText("R: ")
        self.label_y.setText("G: ")
        self.label_z.setText("B: ")

        # Create LineEdits for X, Y, and Z values
        self.line_x = QLineEdit(str(x))
        self.line_y = QLineEdit(str(y))
        self.line_z = QLineEdit(str(z))

        # self.line_x.setValidator(QIntValidator)
        # self.line_y.setValidator(QIntValidator)
        # self.line_z.setValidator(QIntValidator)


        self.line_x.editingFinished.connect(self.emit_state_changed)
        self.line_y.editingFinished.connect(self.emit_state_changed)
        self.line_z.editingFinished.connect(self.emit_state_changed)

        self.line_x.disconnect(self.l1_con)
        self.line_y.disconnect(self.l2_con)
        self.line_z.disconnect(self.l3_con)


    def emit_state_changed(self):
        # Emit custom signal with current values when any field changes
        self.stateChanged.emit(pygame.Color(int(self.line_x.text()), int(self.line_y.text()), int(self.line_z.text())))


    def update_value(self, value: pygame.Color):
        self.line_x.setText(str(value.r))
        self.line_y.setText(str(value.g))
        self.line_z.setText(str(value.b))

    def get_val(self):
        return pygame.Color(int(self.line_x.text()), int(self.line_y.text()), int(self.line_z.text()))

    def get_tuple(self):
        return [int(self.line_x.text()), int(self.line_y.text()), int(self.line_z.text())]

class RectWidget(QWidget):
    stateChanged = pyqtSignal(pygame.Rect)  # Custom signal to emit when any value changes

    def __init__(self, rect: pygame.Rect, parent=None):
        super().__init__(parent)

        self.val = rect
        # Create LineEdits for X, Y, and Z values
        self.line_x = QLineEdit(str(rect.left))
        self.line_y = QLineEdit(str(rect.top))
        self.line_z = QLineEdit(str(rect.width))
        self.line_w = QLineEdit(str(rect.height))

        # Create Labels for X, Y, and Z
        self.label_x = QLabel("L:")
        self.label_y = QLabel("T:")
        self.label_z = QLabel("W:")
        self.label_w = QLabel("H:")

        # Connect text changes to a custom handler
        self.line_x.editingFinished.connect(self.emit_state_changed)
        self.line_y.editingFinished.connect(self.emit_state_changed)
        self.line_z.editingFinished.connect(self.emit_state_changed)
        self.line_w.editingFinished.connect(self.emit_state_changed)

        # Set a layout and add Labels and LineEdits
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for a clean fit

        # Add labels and line edits to the layout
        layout.addWidget(self.label_x)
        layout.addWidget(self.line_x)
        layout.addWidget(self.label_y)
        layout.addWidget(self.line_y)
        layout.addWidget(self.label_z)
        layout.addWidget(self.line_z)
        layout.addWidget(self.label_w)
        layout.addWidget(self.line_w)

        # Set stretch factors to make all LineEdits fit equally
        layout.setStretch(1, 1)  # Stretch X field
        layout.setStretch(2, 1)  # Stretch Y field
        layout.setStretch(3, 1)  # Stretch Z field
        layout.setStretch(4, 1)  # Stretch Z field

        # Set the layout for this widget
        self.setLayout(layout)

    def emit_state_changed(self):
        # Emit custom signal with current values when any field changes
        self.stateChanged.emit(pygame.Rect(int(self.line_x.text()), int(self.line_y.text()), int(self.line_z.text()), int(self.line_w.text())))

    def update_value(self, value: pygame.Rect):
        self.val = value
        self.line_x.setText(str(value.left))
        self.line_y.setText(str(value.top))
        self.line_z.setText(str(value.width))
        self.line_w.setText(str(value.height))


    def get_val(self):
        return pygame.Rect(int(self.line_x.text()), int(self.line_y.text()), int(self.line_z.text()), int(self.line_w.text()))

class Vector2Widget(QWidget):
    stateChanged = pyqtSignal(str, str)  # Custom signal to emit when any value changes

    def __init__(self, x=0, y=0, parent=None):
        super().__init__(parent)

        # Create LineEdits for X, Y, and Z values
        self.line_x = QLineEdit(str(x))
        self.line_y = QLineEdit(str(y))

        # Create Labels for X, Y, and Z
        self.label_x = QLabel("X:")
        self.label_y = QLabel("Y:")

        # Connect text changes to a custom handler
        self.line_x.editingFinished.connect(self.emit_state_changed)
        self.line_y.editingFinished.connect(self.emit_state_changed)

        # Set a layout and add Labels and LineEdits
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for a clean fit

        # Add labels and line edits to the layout
        layout.addWidget(self.label_x)
        layout.addWidget(self.line_x)
        layout.addWidget(self.label_y)
        layout.addWidget(self.line_y)

        # Set stretch factors to make all LineEdits fit equally
        layout.setStretch(1, 1)  # Stretch X field
        layout.setStretch(3, 1)  # Stretch Y field

        # Set the layout for this widget
        self.setLayout(layout)

    def emit_state_changed(self):
        # Emit custom signal with current values when any field changes
        self.stateChanged.emit(self.line_x.text(), self.line_y.text())

    def update_value(self, value: tuple):
        self.line_x.setText(str(value[0]))
        self.line_y.setText(str(value[1]))

    def get_val(self):
        return (self.line_x.text(), self.line_y.text())



class PropertiesThread(QThread):
    var_changed = pyqtSignal(int, str)  # Signal to emit index and new value

    def __init__(self, gamehandler, table, timer, pygamewidget, ui, parent=None):
        super().__init__(parent)

        self.gamehandler = gamehandler
        self.table: QTableWidget = table
        self.timer: QTimer = timer
        self.running = True
        self.pygame_widget = pygamewidget
        self.ui = ui

        self.updating = True

        self.attribute_map = {}  # Map to keep track of attribute to row index
        self.setup_table()  # Setup the initial table

    def setup_table(self):
        # Populate the table with variable names and their corresponding values
        if self.ui.properties_options_1.isChecked():
            game_vars = dir(self.gamehandler.game)
        else:
            _, game_vars, __ = self.gamehandler._find_hot_save_variables()

        if len(game_vars) == 0:
            self.stop()
        else:
            print("resuming properties thread")
            self.running = True
            self.table.clearContents()
            self.table.setEnabled(True)


        built_in_types = (int, float, str, bool, tuple,  list, pygame.Color, pygame.Rect) # Add support for dicts
        blacklist_types = (pygame.Clock)

        user_vars = [var for var in game_vars if not var.startswith("__") and not callable(getattr(self.gamehandler.game, var)) and not isinstance(getattr(self.gamehandler.game, var), blacklist_types)]



        self.table.setColumnCount(2)
        self.table.setRowCount(len(user_vars)+ 20)


        # Populate the table and create the attribute map
        for index, att in enumerate(user_vars):
            self.attribute_map[att] = index  # Map the attribute to its row index
            initial_value = getattr(self.gamehandler.game, att)

            tablewidget = QTableWidgetItem(str(att))
            tablewidget.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.table.setItem(index, 0, tablewidget)  # Column 0: Variable name
            tablewidget._initial_value = initial_value
            self.table.item(index, 0).setData(1, initial_value)


            self.set_cell(index, 1, initial_value, att)

    def set_cell(self, row, col, initial_value, att):
        index = row
        self.table.setRowHeight(index, 28)

        if type(initial_value) == str:
            widget = QLineEdit()
            self.table.setCellWidget(index, 1, widget)
            widget.setText(str(initial_value))

            widget.editingFinished.connect(partial(self.update_var, index, 1, widget.text(), att))


        elif type(initial_value) == int:
            widget = QLineEdit()
            self.table.setCellWidget(index, 1, widget)
            widget.setText(str(initial_value))
            widget.setValidator(QIntValidator())

            widget.editingFinished.connect(partial(self.update_var, index, 1, widget.text(), att))


        elif type(initial_value) == float:
            widget = QLineEdit()
            self.table.setCellWidget(index, 1, widget)
            widget.setText(str(initial_value))
            widget.setValidator(QDoubleValidator())



            widget.editingFinished.connect(partial(self.update_var, index, 1, widget.text(), att))

        elif type(initial_value) == bool:
            widget = QCheckBox()
            self.table.setCellWidget(index, 1, widget)
            widget.setChecked(initial_value)

            print("setting check")

            widget.stateChanged.connect(partial(self.update_var, index, 1, widget.checkState(), att))

        elif type(initial_value) == tuple:
            if len(initial_value) == 3:
                widget = Vector3Widget(initial_value[0], initial_value[1], initial_value[2])
            elif len(initial_value) == 2:
                widget = Vector2Widget(initial_value[0], initial_value[1])

            self.table.setCellWidget(index, 1, widget)
            widget.stateChanged.connect(partial(self.update_var, index, 1, widget.get_val(), att))

        elif type(initial_value) == list:
            widget = QTableWidget()
            widget.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            widget._list = initial_value

            widget.setColumnCount(1)
            widget.setRowCount(len(initial_value))
            widget.horizontalHeader().setVisible(False)
            widget.verticalHeader().setVisible(False)
            widget.horizontalHeader().setStretchLastSection(True)
            self.table.setRowHeight(index, 100)
            widget.setGridStyle(Qt.NoPen)
            widget.setAutoFillBackground(True)
            widget.setStyleSheet(u"QTableWidget{ background-color: rgb(25, 25, 25); }")

            for c_index, i in enumerate(initial_value):
                child = QTableWidgetItem(str(i))
                widget.setItem(c_index, 0, child)
            self.table.setCellWidget(index, 1, widget)

        elif type(initial_value) == pygame.Color:
            widget = Color3Widget(initial_value[0], initial_value[1], initial_value[2])

            self.table.setCellWidget(index, 1, widget)
            widget.stateChanged.connect(partial(self.update_var, index, 1, widget.get_val(), att))

        elif type(initial_value) == pygame.Rect:
            widget = RectWidget(initial_value)

            self.table.setCellWidget(index, 1, widget)
            widget.stateChanged.connect(partial(self.update_var, index, 1, widget.get_val(), att))
        else:
            widget = QLabel()

            widget.setText(str(initial_value))
            self.table.setCellWidget(index, 1, widget)


    def check_cell(self, row, col, initial_value, att, _edit_change = False):
        if att is None or initial_value is None or row is None or col is None:
            if _edit_change: print("all params are None")
            return None
        elif _edit_change:
            print("changing")
            return True

        if initial_value != self.table.item(row, 0)._initial_value:
            if type(initial_value) != type(self.table.item(row, 0)._initial_value):
                print("changing")
                return True
            else:
                return False
        else:
            if _edit_change: print(f"No change in values")
            return None


    def run(self):
        if self.pygame_widget.paused or getattr(self, "gamehandler") == None or self.running == False:
            self.wait()

        try:
            game_vars = dir(self.gamehandler.game)
            built_in_types = (int, float, str, bool, tuple, list, pygame.Color, pygame.Rect)
            user_vars = [var for var in game_vars if not var.startswith("__")]
        except Exception as e:
            return

        prev_values = {}
        prev_types = {}
        for att in user_vars:
            try:
                current_value = getattr(self.gamehandler.game, att)  # Get current value as string
            except:
                return

            current_type = type(current_value)

            # If the attribute is new or has changed, emit a signal to update the table
            if att not in prev_values or prev_values[att] != current_value:

                try:
                    if att in self.attribute_map:  # Ensure the attribute is in the map

                        index = self.attribute_map[att]
                        initial_value = current_value

                        check = self.check_cell(index, 1, current_value, att)

                        if check == True:

                            self.table.item(index, 0)._initial_value = initial_value
                            self.set_cell(index, 1, initial_value, att)

                        elif check == False:
                            self.table.item(index, 0)._initial_value = initial_value
                            self.table.item(index, 0).setData(1, initial_value)


                            if type(initial_value) in [str, int, float]:
                                self.table.cellWidget(index, 1).setText(str(initial_value))

                            elif type(initial_value) == bool:
                                self.table.cellWidget(index, 1).setChecked(initial_value)

                            elif type(initial_value) == tuple:
                                self.table.cellWidget(index, 1).update_value(initial_value)

                            elif type(initial_value) == list:
                                table: QTableWidget = self.table.cellWidget(index, 1)

                                table.clear()
                                table.setRowCount(len(initial_value))
                                for c_index, i in enumerate(initial_value):
                                    child = QTableWidgetItem(str(i))
                                    table.setItem(c_index, 0, child)

                            elif type(initial_value) in [pygame.Rect, pygame.Color]:
                                self.table.cellWidget(index, 1).update_value(initial_value)
                            else:
                                self.table.cellWidget(index, 1).setText(str(initial_value))
                except Exception as e:
                    print(f"<<Warning>>{e}")

    def update_var(self, row, col, initial_value, att):
        print(f"updating var: {row},{col} | {initial_value} ({type(initial_value)}) -> {att}")
        check_val = self.check_cell(row, col, initial_value, att, True)
        if check_val:

            widget = self.table.cellWidget(row, 1)

            if type(initial_value) in [str, int, float]:
                if widget.text() != initial_value:
                    self.update_game_handler(att, widget.text())

            elif type(initial_value) in [Qt.CheckState]:
                if widget.checkState() == 0:
                    self.update_game_handler(att, False)
                else:
                    self.update_game_handler(att, True)

            else:
                if widget.get_val() != initial_value:
                    self.update_game_handler(att, widget.get_val())
        else:
            print(check_val)





    def update_game_handler(self, attribute_name, new_value):
        print("trying to update atrr: " + attribute_name)
        # Assuming all attributes are strings or can be converted to their appropriate types
        try:
            # You may need to convert the new_value to the appropriate type (e.g., int, float)
            # Here we're assuming the attribute can be set as a string
            current_value = getattr(self.gamehandler.game, attribute_name)
            print(f"setting new val {type(new_value)}")

            # Convert the new_value to the same type as the current_value
            if type(current_value) == int:
                new_value = int(new_value)
            elif type(current_value) == float:
                new_value = float(new_value)
            elif type(current_value) == bool:
                new_value = bool(new_value)
            else:
                new_value = new_value

            # Update the game handler's attribute
            setattr(self.gamehandler.game, attribute_name, new_value)


        except Exception as e:
            print(f"Error updating attribute {attribute_name}: {e}")



    def stop(self):
        self.table.clearContents()
        self.table.setEnabled(False)
        self.timer.stop()
        self.running = False  # Method to stop the thread

class ObjectThread(QThread):
    var_changed = pyqtSignal(int, str)  # Signal to emit index and new value

    def __init__(self, gamehandler, tree, timer, pygamewidget, ui, parent=None):
        super().__init__(parent)

        self.gamehandler = gamehandler
        self.tree: QTreeWidget = tree
        self.timer: QTimer = timer
        self.running = True
        self.pygame_widget = pygamewidget
        self.ui = ui
        self.attributes_map = {}  # Map to store attributes

        self.setup_tree()  # Setup the initial table

    def extract_attributes(self, obj, unpacked_attrs, depth=1):
        """
        Recursively extracts attributes of an object or a dictionary up to a maximum depth.
        """
        import inspect

        if depth < 0:  # Base case: stop recursion
            return None

        obj_id = id(obj)  # Use the object's unique identifier as the key
        if obj_id in unpacked_attrs:  # Avoid circular references
            return unpacked_attrs[obj_id]

        # Initialize the parent dictionary for this object
        parent = unpacked_attrs[obj_id] = {}

        if isinstance(obj, dict):  # If obj is a dictionary
            for key, value in obj.items():
                if isinstance(value, dict):  # Recursively unpack nested dictionaries
                    parent[key] = self.extract_attributes(value, unpacked_attrs, depth - 1)
                elif inspect.isclass(value) or hasattr(value, '__dict__'):  # Handle objects or classes
                    parent[key] = self.extract_attributes(value, unpacked_attrs, depth - 1)
                else:  # Primitive types or non-objects
                    parent[key] = value
        else:  # Handle objects
            for attribute in dir(obj):
                if not attribute.startswith('__'):  # Ignore private/internal attributes
                    try:
                        attr_value = getattr(obj, attribute)
                    except AttributeError:  # Skip attributes that raise an error
                        continue
                    if callable(attr_value):  # Skip methods or other callable attributes
                        continue
                    if isinstance(attr_value, dict):  # Recursively unpack nested dictionaries
                        parent[attribute] = self.extract_attributes(attr_value, unpacked_attrs, depth - 1)
                    elif inspect.isclass(attr_value) or hasattr(attr_value, '__dict__'):  # Handle objects or classes
                        parent[attribute] = self.extract_attributes(attr_value, unpacked_attrs, depth - 1)
                    else:  # Primitive types or non-objects
                        parent[attribute] = attr_value

        return parent

    def _add_tree(self, tree_item, obj_name, obj_attrs):
        """
        Recursively adds object attributes to a QTreeWidgetItem.
        """
        obj_item = QTreeWidgetItem(tree_item, [str(obj_name)])

        for attr_name, attr_value in obj_attrs.items():
            if isinstance(attr_value, dict):  # If the attribute is a nested object
                self._add_tree(obj_item, attr_name, attr_value)
            else:
                # Handle displayable text for the value
                display_text = str(attr_value) if attr_value is not None else "None"
                item = QTreeWidgetItem(obj_item, [str(attr_name), display_text])

                # Store the actual value as data
                item.setData(1, 0, attr_value)

    def setup_tree(self):
        """
        Populates the tree and builds the attributes map.
        """
        _, __, packed_vars = self.gamehandler._find_hot_save_variables()

        if len(packed_vars) == 0:
            self.stop()
            return

        self.tree.clear()
        self.tree.setEnabled(True)

        blacklist_types = (pygame.Clock,)
        unpacked_attrs = {}

        unpacked_vars = [
            var for var in packed_vars
            if not var.startswith("__")
            and not callable(getattr(self.gamehandler.game, var))
            and not isinstance(getattr(self.gamehandler.game, var), blacklist_types)
            and getattr(self.gamehandler.game, var).__class__.__module__ != "builtins"
        ]

        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(["Object", "Value"])
        self.tree.setColumnWidth(1, 80)

        for var in unpacked_vars:
            obj = getattr(self.gamehandler.game, var)
            obj_attrs = self.extract_attributes(obj, unpacked_attrs)
            self.attributes_map[var] = obj_attrs  # Store the extracted attributes in the map
            self._add_tree(self.tree, var, obj_attrs)

    def run(self):
        """
        Updates the tree periodically using the attributes map.
        """
        if self.running == False:
            self.wait()

        self.update_tree()


    def update_tree(self):
        """
        Updates the tree using the attributes map.
        """
        for i in range(self.tree.topLevelItemCount()):
            top_item = self.tree.topLevelItem(i)
            var_name = top_item.text(0)
            if var_name in self.attributes_map:
                obj_attrs = self.attributes_map[var_name]
                self._update_tree_item(top_item, obj_attrs)

    def _update_tree_item(self, tree_item, obj_attrs):
        """
        Recursively updates the tree widget item values with the latest attributes.
        """
        for i in range(tree_item.childCount()):
            child_item: QTreeWidgetItem = tree_item.child(i)
            attr_name = child_item.text(0)
            if attr_name in obj_attrs:
                attr_value = obj_attrs[attr_name]
                if isinstance(attr_value, dict):  # If it's a nested object
                    self._update_tree_item(child_item, attr_value)
                else:
                    current_value = child_item.text(1)
                    new_value = getattr(attr_value, "__str__", lambda: attr_value)()

                    if current_value != str(new_value):  # Only update if the value has changed
                        child_item.setText(1, new_value)

                    # current_data = child_item.data(1, 0)
                    # if current_data != attr_value:  # Check if the actual data has changed
                        child_item.setData(1, 1, attr_value)  # Update the actual data

    def stop(self):
        self.timer.stop()
        self.tree.clear()
        self.tree.setEnabled(False)
        self.running = False


class EventStackThread(QThread):
    var_changed = pyqtSignal(int, str)  # Signal to emit index and new value

    def __init__(self, gamehandler, qlist, timer, pygamewidget, ui, parent=None):
        super().__init__(parent)

        self.gamehandler = gamehandler
        self.qlist: QListWidget = qlist
        self.timer: QTimer = timer
        self.running = True
        self.pygame_widget = pygamewidget
        self.ui = ui


    def run(self):
        """
        Updates the tree periodically using the attributes map.
        """
        pass
        # if self.running == False or self.gamehandler:
        #     self.wait()

        # for event in pygame.event.get():
        #     self.qlist.addItem(str(event))

        #if self.previous_event != self.gamehandler.last_event:
            #self.event_stack.append(self.gamehandler.last_event)
            #



    def stop(self):
        self.timer.stop()
        self.running = False
