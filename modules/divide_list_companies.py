import csv
import os
import sys

def recording_info(id_url:str, url:str, file_name:str):
    if not os.path.exists('db/machine_1'):os.makedirs('db/machine_1')
    file_name = f'db/machine_1/{file_name}'
    if not os.path.exists(file_name):
        with open(file_name, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'url'])

    with open(file_name, 'a') as file:
        writer = csv.writer(file)
        writer.writerow([id_url, url])
        print(f'[{id_url}] {url}')


def read_base(base:str):
    with open(base, 'r') as file:

        count_file = 0
        for row in csv.DictReader(file):
            count_file+=1
            url = row.get('company')
            id_url = row.get('id')

            recording_info(url=url, id_url=id_url, file_name=f'conteiner_{count_file}.csv')

            if count_file == 10:count_file = 0
            
            

            

if __name__ == '__main__':
    try:
        base = 'db/companies.csv'
        read_base(base=base)
    except KeyboardInterrupt:
        sys.exit(f'\nExit')
