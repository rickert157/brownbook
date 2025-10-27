from bs4 import BeautifulSoup
from modules.parser import get_source_page
from SinCity.Agent.header import header
import json
import requests
import sys
import time

def get_info(response:str):
    bs = BeautifulSoup(response, 'lxml')
    scripts = bs.find_all('script')
    for script in scripts:
        script = script.get_text()
        
        if '@context' in script and '\\\\' not in script:
            data = json.loads(script.strip())
            
            for a, b in data.items():
                print(f'{a}: {b}')

            company_name = data.get('name')
            image_url = data.get('image')
            logo = data.get('logo')
            email = data.get('email')
            founder_name = data.get('founder').get('name')
            print(
                    f'company name:\t{company_name}\n'
                    f'email:\t\t{email}\n'
                    f'founder:\t{founder_name}'
                    )


def get_page_info(url:str):
    head = header()
    response = requests.get(url, headers=head)
    status = response.status_code

    if status == 200:
        get_info(response=response.text)

if __name__ == '__main__':
    params = sys.argv
    if len(params) > 1 and 'http' in params[1]:
        url = params[1]
        get_page_info(url=url)
