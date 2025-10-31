from SinCity.colors import RED, RESET, GREEN, BLUE, YELLOW
import subprocess
import sys
#В терминале для теста попробовал монтировать базу - все ок
#podman run --rm -it \
#             -v $PWD/db/machine_1/container_1.csv:/root/brownbook/db/machine/companies.csv \
#             -v $PWD/Result:/root/brownbook/Result \
#             brownbook:latest
def run_command(command:str):
    divide_line = '-'*50
    print(
            f'{divide_line}\n'
            f'{GREEN}{command}{RESET}'
            )
    subprocess.run(command, shell=True)

def container_run():
    i=0
    for _ in range(10):
        i+=1
        command = (
                f"podman run -it "
                f"-v $PWD/db/machine_1/container_{i}.csv:"
                f"/root/brownbook/machine/container.csv "
                f"-v $PWD/Result:/root/brownbook/Result "
                f"--name brownbook_{i} brownbook:latest"
                )
        run_command(command)

def container_start():
    i=0
    for _ in range(10):
        i+=1
        command = f"podman start brownbook_{i}"
        run_command(command)

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
    
