import subprocess
from modules.config import data_dir

def run_command(command:str):
    print(command)
    subprocess.run(command, shell=True)

def recording_torrc():
    template = f'{data_dir}/torrc'
    with open(template, 'r') as file:
        for line in file.readlines():
            line = line.strip()
            command = f'echo {line} | sudo tee -a /etc/tor/torrc'
            run_command(command=command)

def install_tor():
    install_package = 'sudo pacman -S tor'
    start_service = 'sudo systemctl start tor && sudo systemctl enable tor'
    restart_service = 'sudo systemctl restart tor'

    run_command(command=install_package)
    run_command(command=start_service)
    recording_torrc()    
    run_command(command=restart_service)
    

if __name__ == '__main__':
    install_tor()
