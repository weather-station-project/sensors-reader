import json
import logging
import os
from collections import OrderedDict

FILE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'health_check.json')
APP_KEY = 'APP'


def register_error_in_health_check_file(key, message):
    if os.path.exists(FILE_NAME):
        with open(file=FILE_NAME, mode='r') as fs:
            file_content = json.loads(s=fs.read(), object_pairs_hook=OrderedDict)
    else:
        file_content = {}
    file_content[key] = message

    with open(file=FILE_NAME, mode='w') as fw:
        json.dump(obj=file_content, fp=fw, indent=4)

    logging.debug(msg=f'Health check registered with key "{key}" and message "{message}".')


def register_success_for_class_into_health_check_file(class_name):
    if not os.path.exists(FILE_NAME):
        return

    with open(file=FILE_NAME, mode='r') as fs:
        file_content = json.loads(s=fs.read(), object_pairs_hook=OrderedDict)

    if class_name not in file_content:
        return

    del file_content[class_name]
    with open(file=FILE_NAME, mode='w') as fw:
        json.dump(obj=file_content, fp=fw, indent=4)

    logging.debug(msg=f'Health check successful registered for class name "{class_name}".')


def erase_health_check_file():
    if os.path.exists(FILE_NAME):
        os.remove(path=FILE_NAME)


def get_error_messages():
    result = []

    if not os.path.exists(FILE_NAME):
        return result

    with open(file=FILE_NAME, mode='r') as fs:
        file_content = json.loads(s=fs.read(), object_pairs_hook=OrderedDict)

    for key in file_content:
        result.append(file_content[key])

    return '\n'.join(result)
