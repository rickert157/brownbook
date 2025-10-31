import csv
import os
import sys

def recording_info(id_url:str, url:str, base_name):
    if not os.path.exists(base_name):
        with open(base_name, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'url'])

    with open(base_name, 'a') as file:
        writer = csv.writer(file)
        writer.writerow([id_url, url])
        print(f'[{id_url}] {url}')


def read_base(base:str):
    with open(base, 'r') as file:

        count_machine_dir = 1
        count_file = 0
        
        for row in csv.DictReader(file):
            url = row.get('company')
            id_url = row.get('id')
            count_file+=1
            if count_file == 11:
                count_machine_dir += 1
                count_file = 1
            
            file_name = f'container_{count_file}'
            machine_dir = f'db/machine_{count_machine_dir}'
            if not os.path.exists(machine_dir):os.makedirs(machine_dir)
            base_name = f'{machine_dir}/{file_name}'
            recording_info(id_url=id_url, url=url, base_name=base_name)
            if count_machine_dir == 20:count_machine_dir = 1
            

            

if __name__ == '__main__':
    try:
        base = 'db/companies.csv'
        read_base(base=base)
    except KeyboardInterrupt:
        sys.exit(f'\nExit')
