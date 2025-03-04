import threading, subprocess, sys, os, tempfile, shutil, astor, ast, pygame
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



imports_blacklist = ["pyredengine"]
inheritance_blacklist = ["PreviewMain.MainGame"]
class_vars = {
    "_engine_mode": False,
}

class Cmplr:

    def __init__(self, script, parent_dir, parent):
        self.parent_dir = parent_dir
        self.parent = parent # Instance of engine

        script_content = self.scanfile(script)
        self.translate_file(script_content)

    def scanfile(self, file):
        with open(file, "r") as f:
            print(f"Reading file: {file}")
            return f.read()

    def translate_file(self, content):   # sourcery skip: low-code-quality
        tree = ast.parse(content)

        project_instance = self.parent
        project_name = self.parent.project_name



        class StripVisitor(ast.NodeTransformer):
            def visit_Import(self, node):
                if new_names := [n for n in node.names if n.name not in imports_blacklist]:
                    node.names = new_names
                    return node
                return None

            def visit_ImportFrom(self, node):
                return None if node.module in imports_blacklist else node

            def visit_ClassDef(self, node):
                new_bases = []
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        if base.id not in inheritance_blacklist:
                            new_bases.append(base)
                    elif isinstance(base, ast.Attribute):
                        full_name = f"{base.value.id}.{base.attr}"
                        if full_name not in inheritance_blacklist:
                            new_bases.append(base)

                if len(new_bases) < len(node.bases):
                    node.bases = new_bases
                    print(f"Changed class definition: class {node.name}()")

                if node.name == "Main":
                    required_methods = ["draw", "update", "handle_events"]
                    existing_methods = {n.name for n in node.body if isinstance(n, ast.FunctionDef)}

                    for method_name in required_methods:
                        if method_name not in existing_methods:
                            print(f"Adding missing method {method_name} to {node.name}")
                            empty_method = ast.FunctionDef(
                                name=method_name,
                                args=ast.arguments(
                                    args=[ast.arg(arg='self', annotation=None)],
                                    vararg=None,
                                    kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]
                                ),
                                body=[ast.Pass()],
                                decorator_list=[],
                                returns=None
                            )
                            node.body.append(empty_method)

                    # Adding the test_run method to the Main class
                    test_run_method = ast.FunctionDef(
                        name="test_run",
                        args=ast.arguments(
                            args=[ast.arg(arg='self', annotation=None)],
                            vararg=None,
                            kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]
                        ),
                        body=[
                            ast.Expr(
                                value=ast.Str(s='Handles the running of the game')
                            ),
                            ast.While(
                                test=ast.Attribute(value=ast.Name(id='self', ctx=ast.Load()), attr='run', ctx=ast.Load()),
                                body=[
                                    ast.Expr(
                                        value=ast.Call(
                                            func=ast.Attribute(value=ast.Name(id='self', ctx=ast.Load()), attr='clock.tick', ctx=ast.Load()),
                                            args=[], keywords=[]
                                        )
                                    ),
                                    ast.Expr(
                                        value=ast.Call(
                                            func=ast.Attribute(value=ast.Name(id='self', ctx=ast.Load()), attr='handle_events', ctx=ast.Load()),
                                            args=[], keywords=[]
                                        )
                                    ),
                                    ast.Expr(
                                        value=ast.Call(
                                            func=ast.Attribute(value=ast.Name(id='self', ctx=ast.Load()), attr='update', ctx=ast.Load()),
                                            args=[], keywords=[]
                                        )
                                    ),
                                    ast.Expr(
                                        value=ast.Call(
                                            func=ast.Attribute(value=ast.Name(id='self', ctx=ast.Load()), attr='draw', ctx=ast.Load()),
                                            args=[], keywords=[]
                                        )
                                    )
                                ],
                                orelse=[]
                            ),
                            ast.Expr(
                                value=ast.Call(
                                    func=ast.Attribute(value=ast.Name(id='pygame', ctx=ast.Load()), attr='quit', ctx=ast.Load()),
                                    args=[], keywords=[]
                                )
                            ),
                            ast.Expr(
                                value=ast.Call(
                                    func=ast.Attribute(value=ast.Name(id='sys', ctx=ast.Load()), attr='exit', ctx=ast.Load()),
                                    args=[], keywords=[]
                                )
                            )
                        ],
                        decorator_list=[],
                        returns=None
                    )

                    node.body.append(test_run_method)

                    self.remove_super_init(node)
                    self.add_custom_attributes(node)

                return node

                new_bases = []
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        if base.id not in inheritance_blacklist:
                            new_bases.append(base)
                    elif isinstance(base, ast.Attribute):
                        full_name = f"{base.value.id}.{base.attr}"
                        if full_name not in inheritance_blacklist:
                            new_bases.append(base)

                if len(new_bases) < len(node.bases):
                    node.bases = new_bases
                    print(f"Changed class definition: class {node.name}()")

                if node.name == "Main":
                    required_methods = ["draw", "update", "handle_events"]
                    existing_methods = {n.name for n in node.body if isinstance(n, ast.FunctionDef)}

                    for method_name in required_methods:
                        if method_name not in existing_methods:
                            print(f"Adding missing method {method_name} to {node.name}")
                            empty_method = ast.FunctionDef(
                                name=method_name,
                                args=ast.arguments(
                                    args=[ast.arg(arg='self', annotation=None)],
                                    vararg=None,
                                    kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]
                                ),
                                body=[ast.Pass()],
                                decorator_list=[],
                                returns=None
                            )
                            node.body.append(empty_method)

                    self.remove_super_init(node)

                    self.add_custom_attributes(node)

                return node

            def remove_super_init(self, node):
                for n in node.body:
                    if isinstance(n, ast.FunctionDef) and n.name == '__init__':
                        new_body = [
                            stmt
                            for stmt in n.body
                            if not (
                                isinstance(stmt, ast.Expr)
                                and isinstance(stmt.value, ast.Call)
                                and isinstance(stmt.value.func, ast.Attribute)
                                and stmt.value.func.attr == '__init__'
                                and isinstance(stmt.value.func.value, ast.Call)
                                and isinstance(
                                    stmt.value.func.value.func, ast.Name
                                )
                                and stmt.value.func.value.func.id == 'super'
                            )
                        ]
                        n.body = new_body
                        break

            def add_custom_attributes(self, node):
                # self.add_display_and_caption(node)
                # self.add_clock_attribute(node)
                self.create_init_with_display_and_dynamic_vars(node)

            def add_display_and_caption(self, node):
                display_assign = ast.Assign(
                    targets=[ast.Attribute(value=ast.Name(id='self', ctx=ast.Store()), attr='display', ctx=ast.Store())],
                    value=ast.Call(
                        func=ast.Attribute(value=ast.Name(id='pygame.display', ctx=ast.Load()), attr='set_mode', ctx=ast.Load()),
                        args=[ast.Constant(value=(1280, 720))],
                        keywords=[]
                    )
                )

                set_caption_expr = ast.Expr(
                    value=ast.Call(
                        func=ast.Attribute(value=ast.Name(id='pygame.display', ctx=ast.Load()), attr='set_caption', ctx=ast.Load()),
                        args=[ast.Constant(value=project_name)],
                        keywords=[]
                    )
                )

                run_assign = ast.Assign(
                    targets=[ast.Attribute(value=ast.Name(id='self', ctx=ast.Store()), attr='run', ctx=ast.Store())],
                    value=ast.Constant(value=True)
                )

                clock_assign = ast.Assign(
                    targets=[ast.Attribute(value=ast.Name(id='self', ctx=ast.Store()), attr='clock', ctx=ast.Store())],
                    value=ast.Call(
                        func=ast.Attribute(value=ast.Name(id='pygame.time', ctx=ast.Load()), attr='Clock', ctx=ast.Load()),
                        args=[],
                        keywords=[]
                    )
                )

                for n in node.body:
                    if isinstance(n, ast.FunctionDef) and n.name == '__init__':
                        n.body.insert(0, clock_assign)
                        n.body.insert(0, run_assign)
                        n.body.insert(0, set_caption_expr)
                        n.body.insert(0, display_assign)
                        break
                else:
                    self.create_init_with_display_and_dynamic_vars(node)

            def add_clock_attribute(self, node):
                clock_assign = ast.Assign(
                    targets=[ast.Attribute(value=ast.Name(id='self', ctx=ast.Store()), attr='clock', ctx=ast.Store())],
                    value=ast.Call(
                        func=ast.Attribute(value=ast.Name(id='pygame.time', ctx=ast.Load()), attr='Clock', ctx=ast.Load()),
                        args=[],
                        keywords=[]
                    )
                )
                for n in node.body:
                    if isinstance(n, ast.FunctionDef) and n.name == '__init__':
                        if not any(
                            isinstance(stmt, ast.Assign) and
                            isinstance(stmt.targets[0], ast.Attribute) and
                            stmt.targets[0].attr == 'clock'
                            for stmt in n.body
                        ):
                            n.body.append(clock_assign)
                        break
                else:
                    self.create_init_with_display_and_dynamic_vars(node)

            def create_init_with_display_and_dynamic_vars(self, node):
                """
                Creates or updates the __init__ method, adding display, caption, run, clock assignments, and dynamic variable assignments
                from `vars_dict`.
                """
                # Prepare the standard initializations for display, caption, run, and clock
                display_assign = ast.Assign(
                    targets=[ast.Attribute(value=ast.Name(id='self', ctx=ast.Store()), attr='display', ctx=ast.Store())],
                    value=ast.Call(
                        func=ast.Attribute(value=ast.Name(id='pygame.display', ctx=ast.Load()), attr='set_mode', ctx=ast.Load()),
                        args=[ast.Constant(value=(1280, 720))],
                        keywords=[]
                    )
                )
                set_caption_expr = ast.Expr(
                    value=ast.Call(
                        func=ast.Attribute(value=ast.Name(id='pygame.display', ctx=ast.Load()), attr='set_caption', ctx=ast.Load()),
                        args=[ast.Constant(value=project_instance.project_name)],
                        keywords=[]
                    )
                )
                run_assign = ast.Assign(
                    targets=[ast.Attribute(value=ast.Name(id='self', ctx=ast.Store()), attr='run', ctx=ast.Store())],
                    value=ast.Constant(value=True)
                )
                clock_assign = ast.Assign(
                    targets=[ast.Attribute(value=ast.Name(id='self', ctx=ast.Store()), attr='clock', ctx=ast.Store())],
                    value=ast.Call(
                        func=ast.Attribute(value=ast.Name(id='pygame.time', ctx=ast.Load()), attr='Clock', ctx=ast.Load()),
                        args=[],
                        keywords=[]
                    )
                )

                # Create the variable assignments from the dictionary
                dynamic_assignments = [
                    ast.Assign(
                        targets=[ast.Attribute(value=ast.Name(id='self', ctx=ast.Store()), attr=var_name, ctx=ast.Store())],
                        value=ast.Constant(value=var_value)
                    ) for var_name, var_value in class_vars.items()
                ]

                # Search for the __init__ method
                for n in node.body:
                    if isinstance(n, ast.FunctionDef) and n.name == '__init__':
                        # If __init__ exists, append the dynamic assignments and ensure the standard initializations are first
                        n.body = [display_assign, set_caption_expr, run_assign, clock_assign] + dynamic_assignments + n.body
                        break
                else:
                    # If __init__ does not exist, create it
                    init_method = ast.FunctionDef(
                        name='__init__',
                        args=ast.arguments(
                            args=[ast.arg(arg='self', annotation=None)],
                            vararg=None,
                            kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]
                        ),
                        body=[display_assign, set_caption_expr, run_assign, clock_assign] + dynamic_assignments,
                        decorator_list=[],
                        returns=None
                    )
                    node.body.insert(0, init_method)


        self.add_initial_code(tree)
        tree = StripVisitor().visit(tree)
        self.add_final_code(tree)

        new_code = astor.to_source(tree)

        # Construct the new file path

        os.chdir(os.path.join(self.parent_dir, ".redengine"))

        if not os.path.exists("build"):
            build_folder = os.mkdir("build")
        if os.path.exists("build/StripMain.py"):
            os.remove("build/StripMain.py")
        if os.path.exists("build/StripMain.exe"):
            os.remove("build/StripMain.exe")
        if os.path.exists("build/Main.exe"):
            os.remove("build/Main.exe")


        output_file_path = os.path.join(self.parent_dir, ".redengine", "build",  "StripMain.py")

        with open(output_file_path, "w") as f:
            f.write(new_code)

        return output_file_path



    def add_initial_code(self, tree):
        # Create the code you want to insert
        initial_code = ast.Expr(
            value=ast.Call(
                func=ast.Name(id='pygame.init', ctx=ast.Load()),
                args=[],
                keywords=[]
            )
        )

        # Find the first non-import node in the module body
        for index, node in enumerate(tree.body):
            if not isinstance(node, (ast.Import, ast.ImportFrom)):
                # Insert the initial code just before the first non-import node
                tree.body.insert(index, initial_code)
                return

        # If all nodes are imports, add the initial code at the end
        tree.body.append(initial_code)

    def add_final_code(self, tree):
        # Create the code you want to insert
        game_assignment = ast.Assign(
            targets=[ast.Name(id='game', ctx=ast.Store())],
            value=ast.Call(
                func=ast.Name(id='Main', ctx=ast.Load()),
                args=[],
                keywords=[]
            )
        )

        test_run_call = ast.Expr(
            value=ast.Call(
                func=ast.Attribute(value=ast.Name(id='game', ctx=ast.Load()), attr='test_run', ctx=ast.Load()),
                args=[],
                keywords=[]
            )
        )

        # Append the game assignment and test_run call at the end of the module body
        tree.body.append(game_assignment)
        tree.body.append(test_run_call)



class CompileDialog(QDialog):
    def __init__(self, script_path, project_path, engine_instance, parent=None):
        super(CompileDialog, self).__init__(parent)

        # Dialog layout
        self.setWindowTitle("Compilation Progress")
        self.resize(500, 400)
        layout = QVBoxLayout(self)

        # Progress bar for fake progress
        self.progressBar = QProgressBar(self)
        layout.addWidget(self.progressBar)

        # Text area for real-time output
        self.outputConsole = QTextEdit(self)
        self.outputConsole.setReadOnly(True)
        layout.addWidget(self.outputConsole)

        # Checkbox to decide whether to keep compiled source
        self.keepCompiledSourceCheckBox = QCheckBox("Keep compiled source", self)
        layout.addWidget(self.keepCompiledSourceCheckBox)

        # Include Assets button
        assetsLayout = QHBoxLayout()
        self.assetsLabel = QLabel("Selected Assets: None", self)
        assetsLayout.addWidget(self.assetsLabel)
        self.includeAssetsButton = QPushButton("Include Assets Within Package", self)
        assetsLayout.addWidget(self.includeAssetsButton)
        layout.addLayout(assetsLayout)
        self.includeAssetsButton.clicked.connect(self.open_file_dialog)

        # Start Compilation button
        self.startButton = QPushButton("Start Compilation", self)
        layout.addWidget(self.startButton)
        self.startButton.clicked.connect(self.start_compilation)

        # Cancel button
        self.cancelButton = QPushButton("Cancel", self)
        layout.addWidget(self.cancelButton)
        self.cancelButton.clicked.connect(self.cancel_process)
        self.cancelButton.setEnabled(False)  # Disable until the compilation starts

        # Initialize the progress bar and timer
        self.progress = 0
        self.progressBar.setValue(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress_bar)

        Compiler = Cmplr(script_path, project_path, engine_instance)

        # Store the script path
        self.script_path = script_path
        self.project_path = project_path
        self.assets_to_include = []  # List of assets to include

        # Initialize QProcess for compilation
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.on_read_output)
        self.process.readyReadStandardError.connect(self.on_read_output)
        self.process.finished.connect(self.on_process_finished)

    def open_file_dialog(self):
        # Open file dialog to select multiple files (assets) to include
        files, _ = QFileDialog.getOpenFileNames(self, "Select Assets", "", "All Files (*)")
        if files:
            self.assets_to_include = files
            self.assetsLabel.setText(f"Selected Assets: {len(files)} files selected")

    def start_compilation(self):
        # Disable start button and enable cancel button once compilation starts

        self.startButton.setEnabled(False)
        self.cancelButton.setEnabled(True)

        # Start the timer for progress bar updates
        self.timer.start(100)  # Update progress every 100 ms

        # Command to run the PyInstaller process
        command = [
            sys.executable,
            "-m",
            "PyInstaller",
            "--onefile",
            "--windowed",
            "--distpath", f"{self.project_path}/.redengine/build"
            # Optional: Hide console window for the final game
        ]

        # Include assets in the command if any selected
        command.extend(
            f"--add-data={asset};{os.path.basename(os.path.dirname(asset))}"
            for asset in self.assets_to_include
        )
        # Add the main script for packaging
        command.append(f"{self.project_path}/.redengine/build/StripMain.py")

        # Start the process
        self.process.start(command[0], command[1:])

    def on_read_output(self):
        # Append output from the process to the text area
        output = self.process.readAllStandardOutput().data().decode()
        error = self.process.readAllStandardError().data().decode()
        if output:
            self.outputConsole.append(output)
        if error:
            self.outputConsole.append(error)

    def update_progress_bar(self):
        # Fake progress bar update - halt at 50%
        if self.progress < 50:
            self.progress += 5  # Increment progress
            self.progressBar.setValue(self.progress)

    def on_process_finished(self, exit_code, exit_status):
        import webbrowser, platform
        # Stop the timer and set the progress bar to 100% when done
        self.timer.stop()
        self.progressBar.setValue(100)

        if exit_code == 0:
            if not self.keepCompiledSourceCheckBox.isChecked():
                if os.path.exists(f"{self.project_path}/.redengine/build/StripMain.py"):
                    os.remove(f"{self.project_path}/.redengine/build/StripMain.py")


            if platform.system() != "Windows":
                shutil.move(f"{self.project_path}/.redengine/build/StripMain", f"{self.project_path}/.redengine/build/Main")
            else:
                shutil.move(f"{self.project_path}/.redengine/build/StripMain.exe", f"{self.project_path}/.redengine/build/Main.exe")


            self.outputConsole.append("\nCompilation successful.")
            QMessageBox.information(self, "Compilation Finished", "Compilation finished successfully!", QMessageBox.Ok)
            webbrowser.open(f"{self.project_path}/.redengine/build")
        else:
            self.outputConsole.append("\nCompilation failed.")
            QMessageBox.critical(self, "Compilation Error", "Compilation failed!", QMessageBox.Ok)

        # Disable the Cancel button when the process is done
        self.cancelButton.setEnabled(False)

    def cancel_process(self):
        # Kill the process if running
        if self.process.state() == QProcess.Running:
            self.process.kill()
            self.outputConsole.append("\nCompilation cancelled.")
            self.timer.stop()
            self.progressBar.setValue(0)
            self.cancelButton.setEnabled(False)
            self.startButton.setEnabled(True)  # Enable start button again
