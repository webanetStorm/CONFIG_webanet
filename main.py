import tarfile
import os


class VirtualShell:

    def __init__(self):
        self.current_path = ''
        self.tar_path = 'webanet.tar'

    def ls(self, dir):
        for item in dir:
            if '/' not in item and item != self.current_path and item.startswith(self.current_path):
                print(item)

    def cd(self, path, dir):
        new_path = os.path.join(self.current_path, path)
        if any(item == new_path for item in dir):
            self.current_path = new_path
        else:
            print(f'\033[31mcd : Не удается найти путь "{self.current_path}/{new_path}", так как он не существует\033[0m')


def main():
    shell = VirtualShell()

    with tarfile.open('webanet.tar', 'a') as tar:
        while True:
            command = input(f'\033[36m{shell.current_path}> \033[0m').strip().split()

            if command[0] == 'exit':
                break
            elif command[0] == 'ls':
                shell.ls(tar.getnames())
            elif command[0] == 'cd' and len(command) >= 2:
                shell.cd(command[1], tar.getnames())
            else:
                print(f'\033[31m"{command[0]}" не является внутренней или внешней командой, исполняемой программой или пакетным файлом\033[0m')


if __name__ == "__main__":
    main()
