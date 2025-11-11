import os
import csv
import requests
import sys
import time
from bs4 import BeautifulSoup
from modules.config import data_dir, categories_doc
from SinCity.colors import RED, RESET, GREEN, YELLOW
from SinCity.Agent.header import header
from typing import Optional

path_base = f'{data_dir}/businesses_url.csv'

#######################################
#   Показываем все категории
#######################################
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

#######################################
#       Проверим, есть ли категория 
#       Если есть - вернем с URL
#######################################
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

#######################################
#       Основная функция модуля
#######################################
def recording_business(id_:int, url:str, category:str):
    if not os.path.exists(path_base):
        with open(path_base, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'url', 'category'])
    with open(path_base, 'a') as file:
        writer = csv.writer(file)
        writer.writerow([id_, url, category])

def parser_category(data:dict[str]):
    category = data['category']
    url = data['url'].split('?page=')[0]

    max_pages = 0
    count_page = 0
    while True:
        count_page+=1
        
        api = (
                f'https://api.brownbook.net/app/api/v1/businesses'
                f'/search/by-name/{category}/?page={count_page}&city=all-cities'
                )
        
        try:
            response = requests.get(api, headers=header())
            if response.status_code == 200:
                info = response.json()
                if count_page == 1:
                    max_pages = info['pages']

                data = info['data']
                businesses_list =  data['businesses']
                
                divide_line = '-'*50
                count_company = 0
                for businesses in businesses_list:
                    count_company+=1
                    print(
                            f'[page {count_page}/{max_pages}] '
                            f'[{count_company}]{divide_line}'
                            )
                    id_ = businesses.get('id')
                    short_name = businesses.get('short_name')
                    url_company =(
                            f'https://www.brownbook.net/business'
                            f'/{id_}/{short_name}'
                            )
                    site = businesses.get('website')
                    print(
                            f'\n'
                            f'ID: {id_}\n'
                            f'Site: {site}\n'
                            f'URL: {url_company}\n'
                            )
                    recording_business(id_=id_, url=url_company, category=category)

            else:
                print(f'{YELLOW}status code: {response.status_code}{RESET}')
            
            if count_page == max_pages:
                break
        #except Exception as err:
        #    print(f'{RED}{err}{RESET}')
        finally:
            time.sleep(5)




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
                try:
                    parser_category(data=check_category)
                except KeyboardInterrupt:
                    sys.exit(f'{RED}\nExit...{RESET}')
            else:
                print(f'{RED}Категория "{category}" не обнаружена{RESET}')
        else:
            sys.exit(f'{RED}Необходимо указать категорию{RESET}')
    else:
        print(
                "Пример команды:\n"
                "python3 -m modules.get_companies_url category='business setup dubai'"
                )
