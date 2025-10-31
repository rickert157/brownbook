from bs4 import BeautifulSoup
from modules.parser import get_source_page
from modules.miniTools import termninal_line, recording_company_info
from SinCity.Agent.header import header
from SinCity.colors import RED, RESET, GREEN, BLUE, YELLOW
import json
import requests
import sys
import time


def parser_description(key:str, script:str) -> str:
    try:
        value = script.split(f'"{key}":')[1].split('"')[1]
        return value
    except IndexError:
        pass

def parser_text(key:str, script:str) -> str:
    try:
        value = script.split(f'"{key}":')[1].split(',')[0]
        if '"' in value:value = value.replace('"', '')
        if value == "null":value = None
        return value
    except IndexError:
        pass

def parser_category(key:str, script:str) -> str:
    try:
        tag_block = script.split('"tags":')[1].split(']')[0]
        category = tag_block.split(f'"{key}":')[1].split(',')[0]
        if '"' in category:category = category.replace('"', '')
        return category
    except IndexError:
        pass

def parser_script(script:str):
    try:
        script = script.get_text()

        if 'website' in script and 'email':
            if 'self.__next_f.push(' in script:
                script = script.lstrip("self.__next_f.push(")
                script = script.rstrip(")")
            if '\\' in script:script = script.replace('\\', '')
            #print(script)
            company_name = parser_text(key='name', script=script).title()
            email = parser_text(key="email", script=script)
            phone = parser_text(key="telephone", script=script)
            if phone == None:
                phone = parser_text(key="phone", script=script)
            if phone != None:
                if ']' in phone:phone = phone.replace(']', '')
                if '}' in phone:phone = phone.replace('}', '')
            site = parser_text(key="website", script=script)
            if site != None and '?' in site:site = site.split('?')[0]
            city = parser_text(key="city", script=script)
            street = parser_text(key="streetAddress", script=script)
            country = parser_text(key="country_code", script=script)
            zip_code = parser_text(key="zip_code", script=script)
            category = parser_category(key="name", script=script)
            twitter = parser_text(key="twitter", script=script)
            if twitter != None and '://' not in twitter:
                twitter = twitter = f"https://x.com/{twitter}"
            facebook = parser_text(key="facebook", script=script)
            insta = parser_text(key="instagram", script=script)
            linkedin = parser_text(key="linkedin", script=script)
            description = parser_description(key="description", script=script)
            print(
                    f"{GREEN}{termninal_line()}{RESET}\n"
                    f"{GREEN}|{RESET} Company:\t{company_name}\n"
                    f"{GREEN}|{RESET} Email:\t{email}\n"
                    f"{GREEN}|{RESET} Phone:\t{phone}\n"
                    f"{GREEN}|{RESET} Site:\t\t{site}\n"
                    f"{GREEN}|{RESET} Category:\t{category}\n"
                    f"{GREEN}|{RESET} Country:\t{country}\n"
                    f"{GREEN}|{RESET} City:\t\t{city}\n"
                    f"{GREEN}|{RESET} Street:\t{street}\n"
                    f"{GREEN}|{RESET} Zip Code:\t{zip_code}\n"
                    f"{GREEN}|{RESET} Twitter:\t{twitter}\n"
                    f"{GREEN}|{RESET} Facebook:\t{facebook}\n"
                    f"{GREEN}|{RESET} Instagram:\t{insta}\n"
                    f"{GREEN}|{RESET} Linkedin:\t{linkedin}\n"
                    f"{GREEN}|{RESET} Description:\t{description}\n"
                    f"{GREEN}{termninal_line()}{RESET}\n"
                    )
            recording_company_info(
                    company_name=company_name,
                    email=email,
                    phone=phone,
                    site=site,
                    category=category,
                    country=country,
                    city=city,
                    street=street,
                    zip_code=zip_code,
                    twitter=twitter,
                    facebook=facebook,
                    insta=insta,
                    description=description
                    )
    except IndexError:
        print(f'не наш клиент')


def get_info(response:str):
    bs = BeautifulSoup(response, 'lxml')
    scripts = bs.find_all('script')
    redirect_warning = 'NEXT_REDIRECT'
   
    for script in scripts:
        script = script.get_text()
        if redirect_warning in script:
            redirect_url = script.split(";replace;")[1]
            if ';' in redirect_url:redirect_url = redirect_url.split(';')[0]
            redirect_url = f'https://www.brownbook.net{redirect_url}'
            print(f'{RED}REDIRECT TO: {redirect_url}{RESET}')
            get_page_info(url=redirect_url)
            return

    for script in scripts:
        parser_script(script=script)

def get_page_info(url:str):
    try:
        head = header()

        response = requests.get(url, headers=head, proxies=proxies)
        status = response.status_code

        if status == 200:
            get_info(response=response.text)
        else:
            print(f'{RED}STATUS CODE: {status}{RESET}')
    
    except requests.exceptions.ConnectionError:
        print('ConnectionError')

if __name__ == '__main__':
    params = sys.argv
    if len(params) > 1 and 'http' in params[1]:
        url = params[1]
        get_page_info(url=url)
