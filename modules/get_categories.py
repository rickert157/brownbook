import csv
import os
import requests
from modules.config import data_dir, categories_doc

def recording_categories(count:int, category:str, url:str):
    if not os.path.exists(categories_doc):
        with open(categories_doc, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Category', 'URL'])

    with open(categories_doc, 'a') as file:
        writer = csv.writer(file)
        writer.writerow([count, category, url])

def get_categories():
    api = 'https://api.brownbook.net/app/api/v1/businesses/categories/all?country=worldwide'
    response = requests.get(api)

    if response.status_code == 200:
        object_categories = response.json()
        categories = object_categories['categories']
        count_category = 0
        for info in categories:
            category = info.get('category')
            if category:
                count_category+=1
                url = f'https://www.brownbook.net/search/worldwide/all-cities/{category}?page=1'
                print(f'[{count_category}] {category}')
                recording_categories(count=count_category, category=category, url=url)
    else:
        print(f'status code: {response.status_code}')


if __name__ == '__main__':
    get_categories()
