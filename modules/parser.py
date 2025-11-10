from bs4 import BeautifulSoup 
from SinCity.Agent.header import header
from SinCity.colors import RED, RESET, GREEN, BLUE, YELLOW
from modules.logger import log_print
from modules.miniTools import log_time
from modules.config import (
        status_type_error, 
        status_type_warning,
        status_type_info
        )
from typing import Optional
import requests


def get_source_page(url:str, parser:Optional[str]=None) -> Optional[str] | list[str] | None:
    mode = parser if parser else 'requests'
    
    log_print(f'{log_time()} {status_type_info} Тип парсера:\t{mode}')
    
    if mode == 'requests':
        head = header()
        response = requests.get(url, headers=head)
        status_code = response.status_code
        if status_code == 200:
            log_print(f'{log_time()} {status_type_info} Доступ к URL: {GREEN}OK{RESET}')
            bs = BeautifulSoup(response.text, 'lxml')
            return bs
        else:
            log_print(f'{log_time()} {status_type_error} Status code: {RED}{status_code}{RESET}')
            return None
    else:
        driver = None
        try:
            driver = driver_chrome()
            driver.get(url)
            page_source = driver.page_source
            bs = BeautifulSoup(page_source, 'lxml')
            if 'Cloudflare' in bs.body.get_text():
                log_print(f'{log_time()} {status_type_warning} Проверка Cloudflare')
                driver.quit()
                parser_result(url=url)
                return None
            else:
                log_print(f'{log_time()} {status_type_info} Проверка Cloudflare не обнаружена')
                page_source = driver.page_source
                bs = BeautifulSoup(page_source, 'lxml')
                return bs
        except Exception as err:
            log_print(f'{log_time()} {status_type_error} Error: {err}')
            return None
        finally:
            if driver:
                driver.quit()
