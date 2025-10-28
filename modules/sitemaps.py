from bs4 import BeautifulSoup
from typing import Optional
from modules.logger import log_print
from modules.miniTools import log_time
from modules.config import (
        status_type_error, 
        status_type_warning,
        status_type_info,
        data_dir
        )
from SinCity.Agent.header import header
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

sitemap_first_step_file = f'{data_dir}/sitemap_start.txt'

def recording_first_list_sitemap(list_url:list[str]) -> None:
    with open(sitemap_first_step_file, 'w') as file:
        for url in list_url:
            file.write(f'{url}\n')

def get_urls(mode:str):
    modes = ['sitemap-level-1', 'sitemap-level-2', 'company']
    
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
            with open(sitemap_first_step_file, 'r') as file:
                count_url = 0
                for line in file.readlines():
                    count_url+=1
                    url = line.strip()
                    print(f'{log_time()} {status_type_info} [{count_url}] {url} ')
        else:
            log_print(
                    f'{log_time()} {status_type_error} '
                    f'файл {sitemap_first_step_file} не обнаружен')
        

    
    

