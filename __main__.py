from bs4 import BeautifulSoup 
from SinCity.colors import RED, RESET, GREEN, BLUE, YELLOW
from SinCity.Browser.driver_chrome import driver_chrome
from modules.miniTools import (
        init_parser, 
        log_time, 
        parse_params
        )
from modules.config import (
        status_type_error, 
        status_type_warning,
        status_type_info
        )
import requests
import sys
import time

def parser_result(url:str) -> None:
    driver = None
    try:
        driver = driver_chrome()
        driver.get(url)
        page_source = driver.page_source
        bs = BeautifulSoup(page_source, 'lxml')
        if 'Cloudflare' in bs.body.get_text():
            print(f'{log_time()} {status_type_warning} Проверка Cloudflare')
            driver.quit()
            parser_result(url=url)
        else:
            print(f'{log_time()} {status_type_info} Проверка Cloudflare не обнаружена')
    except Exception as err:
        print(f'{log_time()} {status_type_error} Error: {err}')
    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    try:
        #инит парсера - создаем директории и подобное
        init_parser()
        #убрать имя скрипта
        params = sys.argv[1:]
    
        args = parse_params(params=params)
    
        if len(args) != 0:
            #print(args)
            test_url = args['--test-url'] if args.get('--test-url') else False 
            recording = args['--recording'] if args.get('--recording') else False
    
            if test_url:
                parser_result(url=test_url)
        if len(args) == 0:
            print(f'{log_time()} {status_type_warning} необходимо передать параметры')
    except KeyboardInterrupt:
        sys.exit(f'\n{log_time()} {status_type_info} Exit...')
    except Exception as err:
        print(f'{log_time()} {status_type_warning} {err}')
