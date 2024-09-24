import tarfile
import os


class VirtualShell:

    def __init__(self):
        self.current_path = ''
        self.tar_path = 'webanet.tar'

    def ls(self, dir):
        current_dir = f'{self.current_path}/' if self.current_path else ''
        for item in dir:
            if item.startswith(current_dir) and item != current_dir:
                relative_item = item[len(current_dir):]
                if '/' not in relative_item:
                    print(relative_item)

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

    def du(self, dir, path='.'):
        total_size = 0
        path = f'{self.current_path}/{path}' if self.current_path else path
        for item in dir:
            if item.startswith(path):
                with tarfile.open(self.tar_path, 'r') as tar:
                    total_size += tar.getmember(item).size
        print(f'{total_size} байт')

    def tree(self, dir):
        for item in dir:
            print(' ' * 4 * item.count('/') + os.path.basename(item))

    def find(self, dir, name):
        found_items = [item for item in dir if name in item]
        for item in found_items:
            print(item)


def throw(message):
    print(f'\033[31m{message}\033[0m')

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
