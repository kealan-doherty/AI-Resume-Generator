import json


def load_json_data(filename,data:list):
    rapid_data = []
    with open(filename, 'r') as file:
        for line in file:
            try:
                data.append(json.loads(line))
                rapid_data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print("error decoding")
    return data





