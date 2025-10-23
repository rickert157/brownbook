from SinCity.colors import RED, RESET, GREEN, BLUE, YELLOW
from modules.parser import get_source_page
from modules.logger import log_print
from modules.miniTools import log_time, recording_countries
from modules.config import status_type_error, status_type_warning, status_type_info
import requests
import csv
import os

def get_api_data(api_url:str) -> dict[str] | None:
    response = requests.get(api_url)
    if response.status_code == 200:
        log_print(
                f'{log_time()} {status_type_info} '
                f'{api_url}: {GREEN}{response.status_code}{RESET}'
                )
        data = response.json()
        return data

    else:
        log_time(
                f'{log_time()} {status_type_error} '
                f'{api_url}: {response.status_code}'
                )
        return None

def get_all_countries():
    api_url = 'https://api.brownbook.net/app/api/v1/businesses/countries'
    data = get_api_data(api_url=api_url)

    if data:
        if data.get('success'):
            countries = data['data']
            for i, country in enumerate(countries):
                count = country['count']
                country_code = country['country_code']
                print(f'[{i+1}] country_code: {country_code}\tcount: {count}')
                recording_countries(country=country_code, count=count)

            
