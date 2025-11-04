import os
import requests
import sys
import socks
from bs4 import BeautifulSoup
from SinCity.colors import RED, RESET, GREEN
from SinCity.Agent.header import header

def get_ip(proxies:str=None, tor:bool=False) -> str:
    ip = None
    url = 'https://ident.me'
    head = header()
    if proxies != None:
        proxy_protocol, proxy_address = proxies.split('://')
        proxies = {proxy_protocol:proxy_address}
    
    if tor:
        TOR_SOCKS_PROXY = 'socks5://127.0.0.1:9050'
        proxies = {
                'http':TOR_SOCKS_PROXY,
                'https':TOR_SOCKS_PROXY
                }

    try:
        response = requests.get(url, proxies=proxies, headers=head)
        if response.status_code == 200:
            bs = BeautifulSoup(response.text, 'lxml')
            ip = bs.body.get_text()
            print(ip)

        else:
            print(f'{RED}STATUS CODE: {response.status_code}{RESET}')
    except requests.exceptions.ProxyError:
        print(f'{RED}Некорректный proxy{RESET}')
    except requests.exceptions.SSLError:
        print(f'SSLError')
    
    return ip


if __name__ == '__main__':
    list_params = ['current-ip', 'check-proxy', 'check-list-proxies', 'tor']
    params = sys.argv
    if list_params[0] in params:
        current_ip = get_ip()
        print(f'{GREEN}Текущий IP: {current_ip}{RESET}')
    elif list_params[1] in params:
        if len(params) > 2 and 'http' in params[2] and '://' in params[2]:
            proxy_address = params[2]
            print(f'{GREEN}Тестируемый прокси: {proxy_address}{RESET}')
            current_ip = get_ip()
            check_ip = get_ip(proxies=proxy_address)
            verdict = 'IP сменился' if current_ip != check_ip and check_ip != None \
                    else 'IP не сменился'
            print(
                    f'Результат тестирования:\n'
                    f'Без прокси:\t{current_ip}\n'
                    f'С прокси:\t{check_ip}\n'
                    f'Вердикт:\t{verdict}'
                    )
        else:
            print(
                    f'Пример использования:\n'
                    f'python3 -m modules.proxy_test check-proxy "http://127.0.0.1:8080"'
                    )
    elif list_params[2] in params:
        if len(params) > 2 and '.txt' in params[2]:
            txt_file = params[2]
            if os.path.exists(txt_file):
                with open(txt_file, 'r') as file:
                    number_line = 0
                    for line in file.readlines():
                        number_line+=1
                        proxy = line.strip()
                        print(f'[{number_line}] {proxy}')
                        print(f'{GREEN}Тестируемый прокси: {proxy}{RESET}')
                        current_ip = get_ip()
                        check_ip = get_ip(proxies=proxy)
                        verdict = 'IP сменился' if current_ip != check_ip \
                                and check_ip != None else 'IP не сменился'
                        print(
                        f'Результат тестирования:\n'
                        f'Без прокси:\t{current_ip}\n'
                        f'С прокси:\t{check_ip}\n'
                        f'Вердикт:\t{verdict}\n'
                        )
            else:
                print(f'{RED}Файл {txt_file} не обнаружен{RESET}')
        else:
            print(
                    f'Пример использования\n'
                    f'python3 -m modules.proxy_test check-list-proxies list.txt'
                    )

    elif list_params[3] in params:
        print(f'Работаем через TOR')
        get_ip(tor=True)
    
    else:
        print(f'Укажи один из параметров:\n{list_params}')
