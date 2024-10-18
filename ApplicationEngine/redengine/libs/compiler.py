import threading, subprocess, sys, os, tempfile, shutil, astor, ast, pygame
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



imports_blacklist = ["pyredengine"]
inheritance_blacklist = ["PreviewMain.MainGame"]

class Cmplr:
    # Goal: 
    # 1. Copy script to temp directory or project directory
    # 2. Translate elements of the original into general pygame code
    # 3. Then get the path of that script and compile that in the main directory
        
    def __init__(self, script, parent_dir):
        self.parent_dir = parent_dir
        
        script_content = self.scanfile(script)
        self.translate_file(script_content)
            
    def scanfile(self, file):
        with open(file, "r") as f:
            print(f"Reading file: {file}")
            return f.read()
    
    def translate_file(self, content):  # sourcery skip: use-named-expression
        print("Parsing file")
        tree = ast.parse(content)
        print("Finished parsing")

        class StripVisitor(ast.NodeTransformer):
            def visit_Import(self, node):
                # Check each alias (imported module)
                new_names = [n for n in node.names if n.name not in imports_blacklist]
                if new_names:
                    node.names = new_names
                    return node  # Keep if there are valid imports left
                return None  # Remove the import statement if all are blacklisted

            def visit_ImportFrom(self, node):
                # Check if it's a blacklisted module
                return None if node.module in imports_blacklist else node

            def visit_ClassDef(self, node):
                # Check if the class inherits from a blacklisted class
                new_bases = []
                
                for base in node.bases:
                    # Check if the base is a simple name or an attribute
                    if isinstance(base, ast.Name):
                        if base.id not in inheritance_blacklist:
                            new_bases.append(base)
                    elif isinstance(base, ast.Attribute):
                        # Check if the base's full name is in the blacklist
                        full_name = f"{base.value.id}.{base.attr}"
                        if full_name not in inheritance_blacklist:
                            new_bases.append(base)
                
                if len(new_bases) < len(node.bases):
                    # If any bases were removed, update the class definition
                    node.bases = new_bases
                    print(f"Changed class definition: class {node.name}()")

                    # Add custom attributes to the class
                    self.add_custom_attributes(node)

                return node
            
            def add_custom_attributes(self, node):
                # Example of adding attributes 'compiled' and 'version'
                attribute_definitions = [
                    
                ]
                
                # Insert attribute definitions into the class body
                for attr_name, attr_value in attribute_definitions:
                    # Create an assignment statement for each attribute
                    assign_node = ast.Assign(
                        targets=[ast.Attribute(value=ast.Name(id='self', ctx=ast.Store()), attr=attr_name, ctx=ast.Store())],
                        value=attr_value
                    )
                    # Insert the attribute assignment at the beginning of the class body
                    node.body.insert(0, assign_node)

                # Add the display and clock attributes, ensuring pygame is available
                self.add_display_attribute(node)
                self.add_clock_attribute(node)

            def add_display_attribute(self, node):
                # Create an assignment statement for the display attribute
                display_assign = ast.Assign(
                    targets=[ast.Attribute(value=ast.Name(id='self', ctx=ast.Store()), attr='display', ctx=ast.Store())],
                    value=ast.Call(
                        func=ast.Attribute(value=ast.Name(id='pygame.display', ctx=ast.Load()), attr='set_mode', ctx=ast.Load()),
                        args=[ast.Constant(value=(1280, 720))],
                        keywords=[]
                    )
                )
                run_assign = ast.Assign(
                    targets=[ast.Attribute(value=ast.Name(id='self', ctx=ast.Store()), attr='run', ctx=ast.Store())],
                    value=ast.Constant(value=True)
                )
                
                
                # Find the __init__ method and add the display assignment there
                for n in node.body:
                    if isinstance(n, ast.FunctionDef) and n.name == '__init__':
                        n.body.append(display_assign)
                        n.body.append(run_assign)
                        break
                else:
                    # If __init__ is not found, we could create one (optional)
                    self.create_init_with_display(node)

            def add_clock_attribute(self, node):
                # Create an assignment statement for the clock attribute
                clock_assign = ast.Assign(
                    targets=[ast.Attribute(value=ast.Name(id='self', ctx=ast.Store()), attr='clock', ctx=ast.Store())],
                    value=ast.Call(
                        func=ast.Attribute(value=ast.Name(id='pygame.time', ctx=ast.Load()), attr='Clock', ctx=ast.Load()),
                        args=[],
                        keywords=[]
                    )
                )
                
                # Find the __init__ method and add the clock assignment there
                for n in node.body:
                    if isinstance(n, ast.FunctionDef) and n.name == '__init__':
                        n.body.append(clock_assign)
                        break
                else:
                    # If __init__ is not found, we could create one (optional)
                    self.create_init_with_display(node)  # Ensure display is also created

            def create_init_with_display(self, node):
                # Create an __init__ method with display and clock attributes
                init_method = ast.FunctionDef(
                    name='__init__',
                    args=ast.arguments(
                        args=[ast.arg(arg='self', annotation=None)],
                        vararg=None,
                        kwonlyargs=[],
                        kw_defaults=[],
                        kwarg=None,
                        defaults=[]
                    ),
                    body=[
                        # Add display attribute assignment
                        ast.Assign(
                            targets=[ast.Attribute(value=ast.Name(id='self', ctx=ast.Store()), attr='display', ctx=ast.Store())],
                            value=ast.Call(
                                func=ast.Attribute(value=ast.Name(id='pygame.display', ctx=ast.Load()), attr='set_mode', ctx=ast.Load()),
                                args=[],
                                keywords=[]
                            )
                        ),
                        # Add clock attribute assignment
                        ast.Assign(
                            targets=[ast.Attribute(value=ast.Name(id='self', ctx=ast.Store()), attr='clock', ctx=ast.Store())],
                            value=ast.Call(
                                func=ast.Attribute(value=ast.Name(id='pygame.time', ctx=ast.Load()), attr='Clock', ctx=ast.Load()),
                                args=[],
                                keywords=[]
                            )
                        ),
                        # Add caption setting expression
                        ast.Expr(
                            value=ast.Call(
                                func=ast.Attribute(value=ast.Name(id='pygame.display', ctx=ast.Load()), attr='set_caption', ctx=ast.Load()),
                                args=[ast.Constant(value="My Game")],
                                keywords=[]
                            )
                        )
                    ],
                    decorator_list=[],
                    returns=None
                )
                
                # Insert __init__ at the beginning of the class body
                node.body.insert(0, init_method)
        
        self.add_initial_code(tree)
        
        print("Stripping file")
        tree = StripVisitor().visit(tree)
    
        self.add_final_code(tree)
        
        
        new_code = astor.to_source(tree)
        print("Finished stripping")
    
        # Construct the new file path
        output_file_path = os.path.join(self.parent_dir, "StripMain.py")
        print(f"Writing file to: {output_file_path}")
        
        with open(output_file_path, "w") as f:
            f.write(new_code)
        print("Finished file compiling, starting exe compilation")

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
    def __init__(self, script_path, project_path, parent=None):
        super(CompileDialog, self).__init__(parent)

        # Dialog layout
        self.setWindowTitle("Compilation Progress")
        self.resize(500, 300)
        layout = QVBoxLayout(self)

        # Progress bar for fake progress
        self.progressBar = QProgressBar(self)
        layout.addWidget(self.progressBar)

        # Text area for real-time output
        self.outputConsole = QTextEdit(self)
        self.outputConsole.setReadOnly(True)
        layout.addWidget(self.outputConsole)

        # Cancel button
        self.cancelButton = QPushButton("Cancel", self)
        layout.addWidget(self.cancelButton)
        self.cancelButton.clicked.connect(self.cancel_process)

        # Initialize the progress bar and timer
        self.progress = 0
        self.progressBar.setValue(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress_bar)
        self.timer.start(100)  # Update progress every 100 ms

        # Store the script path
        self.script_path = script_path
        self.project_path = project_path

        print("instancing compiler")
        cmplr = Cmplr(self.script_path, self.project_path)
        print("closing compiler instance")

        # Initialize QProcess for compilation
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.on_read_output)
        self.process.readyReadStandardError.connect(self.on_read_output)
        self.process.finished.connect(self.on_process_finished)

        # Start the compilation
        self.start_compilation()

    def start_compilation(self):
        # Command to run the PyInstaller process
        command = [sys.executable, "-m", "PyInstaller", "--onefile", self.project_path+"/StripMain.py"]
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
        # Stop the timer and set the progress bar to 100% when done
        self.timer.stop()
        self.progressBar.setValue(100)

        if exit_code == 0:
            self.outputConsole.append("\nCompilation successful.")
            QMessageBox.information(self, "Compilation Finished", "Compilation finished successfully!", QMessageBox.Ok)
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

     



