import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def load_recent_projects_from_json(application_path):
    import json 
    
    file_path = application_path + '/recents.json'
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        return None

    return data

def add_to_recent_projects(project_name, project_json):
    import json
    file_path = 'recents.json'
    
    data = {}

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            # Read the existing file
            with open(file_path, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            # Handle case where the file is not a valid JSON
            print("Warning: The file is not a valid JSON. Starting with an empty dictionary.")
    
    
    
    
    # Check if the project already exists
    if project_name not in data:
        data[project_name] = {"json": project_json}
        
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    
def clear_recent_projects():
    import json
    file_path = 'recents.json'
    
    data = {}

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            # Read the existing file
            with open(file_path, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            # Handle case where the file is not a valid JSON
            print("Warning: The file is not a valid JSON. Starting with an empty dictionary.")

    if data != {}:
        with open(file_path, 'w') as file:
            json.dump({}, file, indent=4)

def remove_from_recent_projects(app_path, project_name):
    import json
    
    data = load_recent_projects_from_json(app_path)
    data.pop(project_name)
    
    with open(app_path+"/recents.json", 'w') as file:
        json.dump(data, file, indent=4)
        

    
def check_recent_projects():
    import json
    file_path = 'recents.json'
    
    data = {}

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            # Read the existing file
            with open(file_path, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            # Handle case where the file is not a valid JSON
            print("Warning: The file is not a valid JSON. Starting with an empty dictionary.")

    if data != {}:
        deleted_entry = []
        for key, value in data.copy().items():
            for x in value.items():
                project_path = x[1]["project_path"]
                project_name = x[1]["project_name"]

                
                
                
                
                
                if not os.path.exists(project_path):
                    with open(file_path, "w") as file:
                        remove_value = data.pop(project_name)
                        json.dump(data, file, indent=4  )                        
     
def generate_project_path(window, project_path, project_name, main_project_file=None, project_scenes=None):
    from datetime import date
    import json
    import os
    from PyQt5.QtWidgets import QMessageBox  # Assuming PyQt5 is used for QMessageBox

    # Initialize the project file dictionary with mandatory parameters
    project_file_gen = {
        "project_name": project_name,
        "project_path": project_path,
        "date_created": str(date.today()),
        "date_edited": str(date.today()),
        "user": os.getlogin(),
    }

    # Create the project directory if it doesn't exist
    try:
        os.makedirs(f"{project_path}/.redengine", exist_ok=True)
    except Exception as e:
        QMessageBox.critical(window, "Error", f"Failed to create project directory: {str(e)}", QMessageBox.Ok)
        return -1

    project_file_path = f"{project_path}/.redengine/project.json"

    # Check if the project file already exists
    if os.path.exists(project_file_path):
        with open(project_file_path, "r") as file:
            existing_data = json.load(file)
    else:
        existing_data = {}

    # Update the existing data with new values or set them to None if they don't exist
    for key, value in project_file_gen.items():
        if key not in existing_data:
            existing_data[key] = value

    if "main_project_file" not in existing_data or main_project_file is not None:
        existing_data["main_project_file"] = main_project_file

    if "project_scenes" not in existing_data or project_scenes is not None:
        existing_data["project_scenes"] = project_scenes

    # Write the project file to the specified path
    with open(project_file_path, "w") as file:
        json.dump(existing_data, file, indent=4)

    return project_file_path

def save_project_json(window, project_path, project_name, main_project_file, project_scenes):
    from datetime import date
    import json

    project_file_gen = {
        "project_name": project_name,
        "project_path": project_path,
        "project_scenes": project_scenes,
        "main_project_file": main_project_file, 
        "date_created": str(date.today()),
        "date_edited" : str(date.today()),
        "user": os.getlogin(),
    }
    
    with open(project_path + "/.redengine/project.json", "w") as file:
        json.dump(project_file_gen, file)
        
