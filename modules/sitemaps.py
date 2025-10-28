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
    modes = ['sitemap-level-1', 'sitemap-level-2', 'company']
    
    if mode not in modes:
        log_print(f'{log_time()} {status_type_error} необходимо выбрать мод:\n{modes}')
        return 
    
    elif mode == 'sitemap-level-1':
        api_url = 'https://api.brownbook.net/sitemap_indexes.xml'
        #собираем первые сайтмапы

    
    

