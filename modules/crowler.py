from SinCity.colors import RED, RESET, GREEN, BLUE, YELLOW
from modules.config import data_dir
from modules.miniTools import init_parser
from modules.parser_page import get_page_info
from typing import Optional
import csv
import os
import sys
import time

path_base = f'{data_dir}/businesses_url.csv'
complite_file = f'{data_dir}/complite_url.txt'

def complite_url_list() -> Optional[set({})] | None:
    list_url = set()
    if os.path.exists(complite_file):
        with open(complite_file, 'r') as file:
            for line in file:
                list_url.add(line.strip())
    return list_url

def crowler():
    init_parser()
    with open(path_base, 'r') as file:
        complite_url = complite_url_list()
        count_url = 0
        for row in csv.DictReader(file):
            count_url+=1
            id_url = row.get('id')
            url = row.get('url')
            category = row.get('category')
            if url not in complite_url:
                print(f'[{count_url}] {url}')
                
                #Парсим страницу
                get_page_info(url=url, category=category)
                time.sleep(10)

                with open(complite_file, 'a') as file:
                    file.write(f'{url}\n')



if __name__ == '__main__':
    try:
        crowler()
    except KeyboardInterrupt:
        sys.exit(f'{RED}\nExit...{RESET}')
