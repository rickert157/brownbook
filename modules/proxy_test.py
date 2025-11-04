import requests
import sys
from bs4 import BeautifulSoup
from SinCity.colors import RED, RESET, GREEN

def get_ip(proxies:str=None) -> str:
    ip = None
    url = 'https://ifconfig.me'
    if proxies != None:
        proxy_protocol, proxy_address = proxies.split('://')
        proxies = {proxy_protocol:proxy_address}

    try:
        response = requests.get(url, proxies=proxies)
        if response.status_code == 200:
            bs = BeautifulSoup(response.text, 'lxml')
            ip = bs.body.get_text()

        else:
            print(f'{RED}STATUS CODE: {response.status_code}{RESET}')
    except requests.exceptions.ProxyError:
        print(f'{RED}Некорректный proxy{RESET}')
    
    return ip


if __name__ == '__main__':
    list_params = ['current-ip', 'check-proxy', 'check-list-proxies']
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
    else:
        print(f'Укажи один из параметров:\n{list_params}')
