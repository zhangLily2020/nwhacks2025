import json
import os

def parse_json():
    data_paths = get_data_paths("./commands")
    d = {}
    id_count = 0
    for path in data_paths:
        print(path)
        try:
            with open(path, "r") as file:
                json_data = json.load(file)
                for command in json_data["commands"]:
                    d[id_count] = command
                    id_count += 1
            
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error: {e}")

    return d

def get_data_paths(folder_path):
    file_paths = []
    for file_name in os.listdir(folder_path):
        full_path = os.path.join(folder_path, file_name)
        file_paths.append(full_path)

    return file_paths