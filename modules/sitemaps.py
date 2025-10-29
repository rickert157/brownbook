from bs4 import BeautifulSoup
from typing import Optional
from modules.logger import log_print
from modules.miniTools import log_time
from modules.config import (
        status_type_error, 
        status_type_warning,
        status_type_info,
        data_dir,
        sitemap_second_level,
        sitemap_first_step_file,
        sitemap_complite,
        sitemap_db
        )
from modules.sql.recording_url import (
        recording_urls_to_db, 
        get_url_from_db,
        recording_company
        )
from SinCity.Agent.header import header
from SinCity.colors import GREEN, BLUE, RESET
import requests
import time
import os
import sys

count_page = 0


def parser_xml(url:str) -> Optional[list[str] | None]:
    """основной парсер сайтмапов xml"""
    global count_page
    list_url = set()
    head = header()
    response = requests.get(url, headers=head)
    status = response.status_code
    if status != 200:
        log_print(f'{log_time()} {status_type_error} status code: {status} : {url}')
    else:
        bs = BeautifulSoup(response.text, 'xml')
        for url in bs.find_all('loc'):
            url = url.get_text()
            list_url.add(url)
            count_page+=1
            log_print(f'{log_time()} {status_type_info} {url} [{count_page}]')

    return list_url


def recording_first_list_sitemap(list_url:list[str]) -> None:
    with open(sitemap_first_step_file, 'w') as file:
        for url in list_url:
            file.write(f'{url}\n')

def recording_second_level_map(list_url) -> None:
    with open(sitemap_second_level, 'a') as file:
        for url in list_url:
            file.write(f'{url}\n')



def complite_urls():
    list_complite = set()
    if os.path.exists(sitemap_complite):
        with open(sitemap_complite, 'r') as file:
            for line in file.readlines():
                list_complite.add(line.strip())

    return list_complite



def get_urls(mode:str):
    modes = ['sitemap-level-1', 'sitemap-level-2', 'get-company']
    
    if mode not in modes:
        log_print(
                f'{log_time()} {status_type_error} '
                f'необходимо указать корректный мод:\n{modes}'
                )
        return 
    
    elif mode == 'sitemap-level-1':
        api_url = 'https://api.brownbook.net/sitemap_indexes.xml'
        #собираем первые сайтмапы
        log_print(f'{log_time()} {status_type_info} получаем первичный список ссылок')
        list_xml = parser_xml(url=api_url)
        if len(list_xml) != 0:
            recording_first_list_sitemap(list_url=list_xml)
            log_print(
                    f'{log_time()} {status_type_info} '
                    f'получен список первых {len(list_xml)} ссылок'
                    )
    elif mode == 'sitemap-level-2':
        if os.path.exists(sitemap_first_step_file):
            if os.path.exists(sitemap_second_level):os.remove(sitemap_second_level)
            with open(sitemap_first_step_file, 'r') as file:
                count_url = 0
                for line in file.readlines():
                    count_url+=1
                    url = line.strip()
                    print(f'{log_time()} {status_type_info} [{count_url}] {url} ')
                    list_xml = parser_xml(url=url)
                    if len(list_xml) != 0:
                        recording_second_level_map(list_url=list_xml)
                        log_print(
                                f'{log_time()} {status_type_info} '
                                f'получен список первых {len(list_xml)} ссылок'
                        )
            query_recording_url_to_db = input(
                    f'{BLUE}Записать ссылки в базу данных?{RESET}[y/n] '
                    )
            if 'y' in query_recording_url_to_db:
                log_print(
                        f'{log_time()} {status_type_info} '
                        f'{GREEN}Записываем данные в базу данных...'
                        )
                recording_urls_to_db()
                log_print(f'{log_time()} {status_type_info} Ссылки записаны')
            else:
                log_print(
                        f'{log_time()} {status_type_warning} '
                        f'Запись ссылок в базу данных отклонена')
        else:
            log_print(
                    f'{log_time()} {status_type_error} '
                    f'файл {sitemap_first_step_file} не обнаружен')
    elif mode == 'get-company':
        
        txt_status = os.path.exists(sitemap_second_level)
        db_status = os.path.exists(sitemap_db)
        
        if db_status or txt_status:
            if db_status:
                list_urls = get_url_from_db()

                list_complite = complite_urls()
                count_url = 0
                for url in list_urls:
                    count_url+=1
                    if url not in list_complite:
                        list_company = parser_xml(url=url)
                        recording_company(
                                list_url=list_company
                                )
                        with open(sitemap_complite, 'a') as file:
                            file.write(f'{url}\n')
                        print(f'[{count_url} / {len(list_urls)}] {url} recording!')
        else:
            log_print(
                    f'{log_time()} {status_type_error} '
                    f'Не найдены {sitemap_second_level} и {sitemap_db}'
                    )
        
