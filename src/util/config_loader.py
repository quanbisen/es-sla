import json


# 加载配置文件函数
def load_config_as_json(path):
    print('loading config file: ' + path + '.')
    try:
        with open(path, 'r') as file_object:
            json_object = json.load(file_object)
    except FileNotFoundError:
        print('file: ' + path + ' not exist.')
    return json_object

