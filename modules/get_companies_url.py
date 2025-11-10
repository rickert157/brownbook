import os
import csv
import sys
from modules.config import data_dir, categories_doc
from SinCity.colors import RED, RESET, GREEN
from SinCity.Agent.header import header
from typing import Optional

def read_categories_doc() -> None:
    if os.path.exists(categories_doc):
        with open(categories_doc, 'r') as file:
            for row in csv.DictReader(file):
                id_ = row.get('ID')
                category = row.get('Category')
                url = row.get('URL')
                print(f'[{id_}] {category}\t{url}')

    else:
        print(
                f'Собери категори:\n'
                f'python3 -m modules.get_categories'
                )

def get_url_category(category:str) -> Optional[str] | False:
    if os.path.exists(categories_doc):
        status = False
        with open(categories_doc, 'r') as file:
            for row in csv.DictReader(file):
                tag = row.get('Category')
                url = row.get('URL')
                if tag == category:
                    status = True
                    data = {'category':tag, 'url':url}
                    return data
        if status == False:
            return False
    else:
        print(
                f'Собери категори:\n'
                f'python3 -m modules.get_categories'
                )

def parser_category(data:dict[str]):
    print(data)

if __name__ == '__main__':
    params = sys.argv
    if len(params) == 1:
        read_categories_doc()
    elif 'category=' in params[1]:
        category = params[1].split('category=')[1]
        if len(category) > 0:
            category = category.strip()
            check_category = get_url_category(category=category)
            if check_category:
                parser_category(data=check_category)
            else:
                print(f'{RED}Категория "{category}" не обнаружена{RESET}')
        else:
            sys.exit(f'{RED}Необходимо указать категорию{RESET}')
    else:
        print(
                "Пример команды:\n"
                "python3 -m modules.get_companies_url category='business setup dubai'"
                )
