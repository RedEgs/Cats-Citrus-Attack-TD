import libs.classes.main_game as mg  
import sys, importlib

import pyredengine as pyr


class GameHandler():
    def __init__(self, main_file_path: str, project_file_path: str) -> None:
        self.main_file_path = main_file_path
        self.project_file_path = project_file_path
        self.process_attached = False
        self.is_app_process = False
    
    def start_process(self):
        sys.path.insert(0, self.project_file_path) # Makes the project directory importable
        import main # Import the main project file
        importlib.reload(main) # Reload imports, which will update new code
        self.game = main.MainGame(self) # Instance the game within the handler
        
        if issubclass(main.MainGame, pyr.App):
            self.is_app_process = True

        self.process_attached = True


    def stop_process(self):
        self.game.close_game()
        self.process_attached = False
        self.is_app_process = False
        
    def hot_reload(self):
        if not self.process_attached:
            pass # Add an exception here
                
        sys.path.insert(0, self.project_file_path) # Makes the project directory importable
        import main # Import the main project file
        self.save_process_state() # Save the process state 
        importlib.reload(main) # Reload imports, which will update new code
        self.game = main.MainGame(self) # Reinstance game
        self.load_process_state()

    def send_event(self, event):
        if not self.is_app_process:
            if type(event) == str:
                self.game._send_event(event)
            elif type(event) == tuple:
                self.game._send_event(2, None, int(event[0]), int(event[1]))   
        else:
            if type(event) == str:
                self.game.send_key(event)
            elif type(event) == tuple:
                pass
                #self.game._send_event(2, None, int(event[0]), int(event[1]))   
            
    def run_game(self):
        if self.is_app_process:
            return self.game.qt_run()
        else:
            return self.game.run_game()

    def get_game_process(self):
        return self.game
    
    def get_main_display(self):
        return self.game.display
    

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

