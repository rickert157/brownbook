from bs4 import BeautifulSoup 
from SinCity.colors import RED, RESET, GREEN, BLUE, YELLOW
from modules.logger import log_print
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
from modules.parser import get_source_page 
from modules.get_countries import get_all_countries
from modules.sitemaps import get_urls
import requests
import sys
import time


if __name__ == '__main__':
    try:
        #инит парсера - создаем директории и подобное
        init_parser()
        #убрать имя скрипта
        params = sys.argv[1:]
    
        argv = parse_params(params=params)
    
        if len(argv) != 0:
            #print(argv)
            test_url = argv['--test-url'] if argv.get('--test-url') else None 
            parser = argv['--parser'] if argv.get('--parser') else None 
            countries = argv['--countries'] if argv.get('--countries') else None
            sitemap = argv['--sitemap'] if argv.get('--sitemap') else None

            parser_mode_list = ['requests', 'selenium', None]

            if parser not in parser_mode_list:
                sys.exit(
                        f'{log_time()} {status_type_error} '
                        f'Выбери из доступных методов: {parser_mode_list[0:-1]}')
            
            if countries:
                get_all_countries()
            elif sitemap:
                get_urls(mode=sitemap)
            elif test_url:
                get_source_page(url=test_url, parser=parser)
            
        if len(argv) == 0:
            log_print(f'{log_time()} {status_type_warning} необходимо передать параметры')
    except KeyboardInterrupt:
        sys.exit(f'\n{log_time()} {status_type_info} Exit...')
    except Exception as err:
        log_print(f'{log_time()} {status_type_warning} {err}')
