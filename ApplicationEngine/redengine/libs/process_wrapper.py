import sys, importlib, pickle, re, os

from pyredengine import PreviewMain

class GameHandler():
    def __init__(self, main_file_path: str, project_file_path: str) -> None:
        self.main_file_path = main_file_path
        self.project_file_path = project_file_path
        self.process_attached = False
        
        print("intialised handler succesfulay ")
    
    def start_process(self):
        import importlib.util
        
        
        print("Starting Process")
        try:
            print("Before inserting path")
            sys.path.append(self.project_file_path) # Makes the project directory importable
            print("Importing Path: " + self.project_file_path)

            try:
                import main  # Import the main project file
                print("Importing File")
            except Exception as e:
                print(f"Error importing main: {e}")

            try:
                importlib.reload(main)  # Reload imports, which will update new code
                print("Reloading Import")
            except Exception as e:
                print(f"Error reloading main: {e}")
        except Exception as e:
            print(f"Error in setup: {e}")
        
        print("Before Instancing Game")
        self.game: PreviewMain.MainGame = main.Main() # Instance the game within the handler
        print("After Instancing Game")


        self.process_attached = True

        print("Started Process ")

    def stop_process(self):
        self.game.close_game()
        self.process_attached = False
        self.is_app_process = False
        
    def hot_reload(self):
        print("started hot reload")

        sys.path.insert(0, self.project_file_path) # Makes the project directory importable

        
        import main # Import the main project file
        self.save_process_state() # Save the process state 
        importlib.reload(main) # Reload imports, which will update new code

        self.game: PreviewMain.MainGame = main.Main()
        
        self.load_process_state()
        print("function finished")

    def send_event(self, id, event):
        if type(event) == str and id == "k":
            self.game._send_event(event)
        elif type(event) == tuple or type(event) == list and id == "mm":
            self.game._send_event(2, None, [int(event[0]), int(event[1]), int(event[2])])   
        if type(event) == tuple or type(event) == list and id == "md":
            self.game._send_event(3, None, [int(event[0]), int(event[1]), int(event[2])])   
        elif type(event) == tuple or type(event) == list and id == "mu":
            self.game._send_event(4, None, [int(event[0]), int(event[1]), 0])   



    def run_game(self):
        return self.game.run_game()

    def get_game_process(self):
        return self.game
    
    def get_main_display(self):
        return self.game.display
    
    def save_process_state(self):
        self.hotsave_manager.save_process_state()
        
    def load_process_state(self):
        self.hotsave_manager.load_process_state()

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
        
        m_lines = self._get_marked_lines(self.main_file_path)
        state = self._get_marked_vars(m_lines, self.main_file_path)

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

