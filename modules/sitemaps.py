from bs4 import BeautifulSoup
from typing import Optional
from modules.logger import log_print
from modules.miniTools import log_time
from modules.config import (
        status_type_error, 
        status_type_warning,
        status_type_info
        )
from SinCity.Agent.header import header
import requests
import time
import os
import sys

count_page = 0
url_xml = 'url_xml.txt'
url_business = 'business.txt'

def recording_xml(url:str, step:Optional[str]=None):
    file_name = url_business if step else url_xml
    with open(file_name, 'a') as file:
        file.write(f'{url}\n')


def parser_xml(url:str, step:Optional[str]=None) -> Optional[list[str] | None]:
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
            recording_xml(url=url, step=step)

    return list_url

def get_urls(mode:str):
    modes = ['sitemap', 'company']
    
    if mode not in modes:
        log_print(f'{log_time()} {status_type_error} необходимо выбрать мод: {modes}')
        return 
    
    elif mode == 'sitemap':
        api_url = 'https://api.brownbook.net/sitemap_indexes.xml'
        #собираем первые сайтмапы
        pages = parser_xml(url=api_url)
        if len(pages) != 0:
            for page in pages:
                #собираем все сайтмапы
                parser_xml(url=page)
                time.sleep(1)
        with open(url_xml, 'r') as file:
            for line in file.readlines():
                url = line.strip()
                if '/sitemap/index_' not in url:
                    parser_xml(url, step='end')

    elif mode == 'company':
        log_print(f'{log_time()} {status_type_info} Модуль в стадии планирования')
    
    

