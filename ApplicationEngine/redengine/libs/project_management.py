import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def load_recent_projects_from_json():
    import json 
    
    file_path = 'recents.json'
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        print(f"No such file: {file_path}")
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
        print(f"Project '{project_name}' added.")
    else:
        print(f"Project '{project_name}' already exists.")
    
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
        for key, value in data.items():
            for x in value.items():
                project_path = x[1]["project_path"]
                project_name = x[1]["project_name"]
                if not os.path.exists(project_path):
                    with open(file_path, "w") as file:
                        remove_value = data.pop(project_name)
                        json.dump(data, file, indent=4  )                        

        
def generate_project_path(window, project_path, project_name, main_project_file = None):
    from datetime import date
    import json
    
    #print(project_path + "/project.json")
    project_file_gen = {
        "project_name": project_name,
        "project_path": project_path,
        "main_project_file": main_project_file, 
        "date_created": str(date.today()),
        "date_edited" : str(date.today())  
    }

    try:
        os.mkdir(project_path + "/.redengine") # Error Handling ehre
    except:
        QMessageBox.critical(window, "Error", f"Project already exists.", QMessageBox.Ok)
        return -1
    
    with open(project_path + "/.redengine/project.json", "w") as file:
        json.dump(project_file_gen, file)

    return project_path + "/.redengine/project.json"

def save_project_json(window, project_path, project_name, main_project_file):
    from datetime import date
    import json
    
    #print(project_path + "/project.json")
    project_file_gen = {
        "project_name": project_name,
        "project_path": project_path,
        "main_project_file": main_project_file, 
        "date_created": str(date.today()),
        "date_edited" : str(date.today())  
    }
    
    with open(project_path + "/.redengine/project.json", "w") as file:
        json.dump(project_file_gen, file)

        