import re

def log_print(message):
    print(message)
    ansi = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    clear_text = ansi.sub('', message)
    with open('parser.log', 'a+', encoding='utf-8') as file:
        file.write(f'{clear_text}\n')

