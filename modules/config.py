from SinCity.colors import RED, RESET, GREEN, BLUE, YELLOW

#директории/файл для хранения инфы
result_dir = 'Result'
result_file = 'brownbook.csv'
result_file_path = f'{result_dir}/{result_file}'
data_dir = 'Data'
countries_file = f'{data_dir}/countries.csv'


#статусы
status_type_info = f"[{GREEN}INFO{RESET}]"
status_type_error = f"[{RED}ERROR{RESET}]"
status_type_warning = f"[{YELLOW}WARNING{RESET}]"
