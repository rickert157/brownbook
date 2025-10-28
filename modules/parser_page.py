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
            email = data.get('email')
            phone = data.get('telephone')
            description = data.get('description')
            image_url = data.get('image')
            url = data.get('url')
            logo = data.get('logo')
            founder_name = data.get('founder').get('name')
            address_street = data.get('address').get('streetAddress')
            post_code = data.get('address').get('postalCode')
            country = data.get('address').get('addressCountry')
            company_name = company_name.title() if company_name else company_name
            print(
                    f'Company:\t{company_name}\n'
                    f'Founder:\t{founder_name}\n'
                    f'Country:\t{country}\n'
                    f'Post Code:\t{post_code}\n'
                    f'Street:\t\t{address_street}\n'
                    f'Email:\t\t{email}\n'
                    f'Phone:\t\t{phone}\n'
                    f'URL:\t\t{url}\n'
                    f'Description:\t{description}'
                    )


def get_page_info(url:str):
    try:
        head = header()
        response = requests.get(url, headers=head)
        status = response.status_code

        if status == 200:
            get_info(response=response.text)
    
    except requests.exceptions.ConnectionError:
        print('ConnectionError')

if __name__ == '__main__':
    params = sys.argv
    if len(params) > 1 and 'http' in params[1]:
        url = params[1]
        get_page_info(url=url)
