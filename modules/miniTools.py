from SinCity.colors import RED, RESET, GREEN, BLUE
from modules.config import (
        result_dir, 
        result_file_path, 
        status_type_info
        )
import csv
import os
import sys
import time


def log_time():
    current_time = time.strftime("%H:%M:%S")
    log = f"[{BLUE}{current_time}{RESET}]"
    return log

def init_parser():
    print(f'{log_time()} {status_type_info} start...{RESET}')
    
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
        print(f'{log_time()} {status_type_info} CREATE dir:\t{result_dir}')

    if not os.path.exists(result_file_path):
        with open(result_file_path, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['Company', 'Domain', 'Phone', 'Location'])
        print(f'{log_time()} {status_type_info} CREATE file:\t{result_file_path}')


def parse_params(params:list[str]) -> dict[str | None]:
    """Парсер параметров коммандной строки"""
    commands = ['--test-url', '--recording']
    parsed_argv = {}
    
    for command in commands:
        for param in params:
            if command in param:
                try:
                    value = param.split('=', 1)[1].strip()
                    if command not in parsed_argv:
                        parsed_argv[command] = value
                except IndexError:
                    print(
                            f'{log_time()} {status_type_error} '
                            f'необходимо передать значение: {YELLOW}{param}{RESET}=<url>')
    return parsed_argv
