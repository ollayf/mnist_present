import json

def read_json(file_path):
    with open(file_path , 'r') as file:
        data = json.load(file)
    return data

def write_json(json_path, data):
    with open(json_path, 'w') as file:
        file.write(json.dumps(data, indent = 4))