import xml.etree.ElementTree as ET
from datetime import datetime
import argparse
import tarfile
import os


class VirtualShell:

    def __init__(self, tar_path, log_path):
        self.current_path = ''
        self.tar_path = tar_path
        self.log_path = log_path
        self.log_element = ET.Element('session')

    def log(self, command):
        cmd = ET.SubElement(self.log_element, 'command')
        cmd.text = command
        ET.ElementTree(self.log_element).write(self.log_path)

    def ls(self, dir, path):
        if path:
            current_dir = f'{path}/'
        else:
            current_dir = f'{self.current_path}/' if self.current_path else ''
        for item in dir:
            if item.startswith(current_dir) and item != current_dir:
                relative_item = item[len(current_dir):]
                if '/' not in relative_item:
                    print(relative_item)
        self.log(f'[{datetime.now()}]: ls в {self.current_path}')

    def cd(self, path, dir):
        if path == '/':
            self.current_path = ''
        elif path == '..':
            self.current_path = os.path.dirname(self.current_path)
        else:
            new_path = os.path.join(self.current_path, path)
            if any(item == new_path for item in dir):
                self.current_path = new_path
            else:
                throw(f'cd : Не удается найти путь "{self.current_path}/{new_path}", так как он не существует')
        self.log(f'[{datetime.now()}]: cd в {self.current_path}')

    def du(self, dir, path='.'):
        total_size = 0
        path = f'{self.current_path}/{path}' if self.current_path else path

        with tarfile.open(self.tar_path, 'r') as tar:
            if path in dir and not path.endswith('/'):
                total_size += tar.getmember(path).size
            else:
                for item in dir:
                    full_path = f'{path}/' if not path.endswith('/') else path
                    if item.startswith(full_path) and not item.endswith('/'):
                        try:
                            total_size += tar.getmember(item).size
                        except KeyError:
                            pass

        print(f'{total_size} байт')
        self.log(f'[{datetime.now()}]: du для {path}')

    def tree(self, dir):
        for item in dir:
            print(' ' * 4 * item.count('/') + os.path.basename(item))
        self.log(f'[{datetime.now()}]: tree в {self.current_path}')

    def find(self, dir, name):
        found_items = [item for item in dir if name in item]
        for item in found_items:
            print(item)
        self.log(f'[{datetime.now()}]: find в {self.current_path}')


def throw(message):
    message = f'\033[31m{message}\033[0m'
    print(message)

def main():
    parser = argparse.ArgumentParser(description="VirtualShell CLI")
    parser.add_argument('--tar_path', type=str, required=True, help="Путь к tar архиву виртуальной файловой системы")
    parser.add_argument('--log_path', type=str, required=True, help="Путь к лог-файлу")
    args = parser.parse_args()

    shell = VirtualShell(args.tar_path, args.log_path)

    with tarfile.open('webanet.tar', 'a') as tar:
        while True:
            command = input(f'\033[36m{shell.current_path}> \033[0m').strip().split()
            if command[0] == 'exit':
                break
            elif command[0] == 'ls':
                shell.ls(tar.getnames(), command[1] if len(command) > 1 else None)
            elif command[0] == 'cd' and len(command) >= 2:
                shell.cd(command[1], tar.getnames())
            elif command[0] == 'du':
                shell.du(tar.getnames(), command[1] if len(command) >= 2 else '.')
            elif command[0] == 'tree':
                shell.tree(tar.getnames())
            elif command[0] == 'find':
                shell.find(tar.getnames(), command[1])
            else:
                throw(f'"{command[0]}" не является внутренней или внешней командой, исполняемой программой или пакетным файлом')


if __name__ == '__main__':
    main()
