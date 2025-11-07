from SinCity.colors import RED, RESET, GREEN, BLUE, YELLOW
import subprocess
import sys
import time 

def run_command(command:str, count:int):
    divide_line = '-'*50
    print(
            f'[{count}]{divide_line}\n'
            f'{GREEN}{command}{RESET}'
            )
    subprocess.run(command, shell=True)

def container_run():
    i=0
    for _ in range(10):
        i+=1
        command = (
                f"podman run -d "
                f"--hostname container_{i} "
                f"--network host "
                f"-v $PWD/db/machine_1/container_{i}.csv:"
                f"/root/brownbook/db/machine/container.csv "
                f"-v $PWD/Result:/root/brownbook/Result "
                f"--name brownbook_{i} brownbook:latest"
                )
        run_command(command, count=i)
        time.sleep(2)

def container_start():
    i=0
    for _ in range(10):
        i+=1
        command = f"podman start brownbook_{i}"
        run_command(command, count=i)
        time.sleep(2)

if __name__ == '__main__':
    params = sys.argv
    if len(params) == 2 and (params[1] == 'run' or  params[1] == 'start'):
        mode = params[1]
        if mode == 'run':
            container_run()
        else:
            container_start()
    else:
        print("mode: 'run' or 'start'")
    
