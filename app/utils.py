import os
import datetime
import json

current_time: datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
current_dir = os.path.dirname(__file__)
parent_dir = os.path.join(current_dir, '..')
file_path = os.path.join(parent_dir, 'library_db.json')


def create_log_file() -> None:
    file_name = "logs.txt"
    if not os.path.exists(file_name):
        with open(file_name, "w") as file:
            file.write("")


def logger(log: str, level: str) -> None:
    create_log_file()
    with open('logs.txt', 'a', encoding='utf-8') as file:
        marker = ''
        if level == 'error':
            marker = ' Error: '
        elif level == 'info':
            marker = ' Info: '
        elif level == 'warning':
            marker = ' Warning: '
        file.write(current_time + marker + str(log) + '\n')


def json_library_reader(file_path: str = file_path) -> list:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError as err:
        logger(err, 'error')


def append_to_json_library(data: dict, file_path: str = file_path) -> None:
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except FileNotFoundError as err:
        logger(err, 'error')
