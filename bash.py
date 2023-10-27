import os
import shutil
import subprocess
from colorama import Fore, init
from socket import gethostname
from getpass import getuser
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit import ANSI
import datetime

# Otomatik renk sıfırlama özelliğini etkinleştir
init(autoreset=True)

# Kullanıcı komut geçmişi ve mevcut dizin
history = []
current_directory = os.getcwd()

# Dizin içeriğini gösteren işlev
def show_directory_contents(directory):
    print(f"Contents of directory '{directory}':")
    list_files(directory)

# Kullanıcı komutlarını kaydetmek için kullanılan dosya
log_file = "command_log.txt"

# Kullanıcı komutlarını kaydetmek için işlev
def log_command(user, command):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(f"{timestamp} - User: {user}, Command: {command}\n")

# Dosya veya dizin taşıma işlemini gerçekleştiren işlev
def move_file(src, dest):
    try:
        shutil.move(src, dest)
        print(f"Moved {src} to {dest}")
    except FileNotFoundError:
        print(f"File not found: {src}")

# Dosya taşıma komutunu işleyen işlev
def move_file_command(src, dest):
    try:
        shutil.move(src, dest)
        print(f"Moved {src} to {dest}")
    except FileNotFoundError:
        print(f"File not found: {src}")

# Dosya veya dizin kopyalama işlemini gerçekleştiren işlev
def copy_file(src, dest):
    try:
        shutil.copy2(src, dest)
        print(f"Copied {src} to {dest}")
    except FileNotFoundError:
        print(f"File not found: {src}")

# Dosya silme işlemini gerçekleştiren işlev
def delete_file(file):
    try:
        os.remove(file)
        print(f"Deleted {file}")
    except FileNotFoundError:
        print(f"File not found: {file}")

# Yeni bir dosya oluşturma işlemini gerçekleştiren işlev
def create_file(file):
    try:
        with open(file, 'w') as f:
            print(f"Created {file}")
    except FileExistsError:
        print(f"File already exists: {file}")

# Mevcut dizindeki dosyaları listelemek için kullanılan işlev
def list_files():
    files = os.listdir(current_directory)
    for file in files:
        print(file)

# Belirli bir anahtar kelime içeren dosyaları aramak için kullanılan işlev
def search_files(keyword):
    try:
        result = subprocess.run(f'findstr /M /C:"{keyword}" *.*', shell=True, cwd=current_directory)
        if result.returncode == 0:
            print("Matching files:")
            print(result.stdout)
        else:
            print("No matching files found.")
    except FileNotFoundError:
        print("'findstr' command not found. This feature may not work on your system.")

# Dosya düzenleme işlemini başlatan işlev
def edit_file(file):
    try:
        editor = "notepad.exe"  # Varsayılan metin düzenleyiciyi Windows için Notepad olarak ayarlayın. Sistem tipinize göre değiştirebilirsiniz.
        subprocess.run([editor, file])
        print(f"Opened {file} for editing.")
    except FileNotFoundError:
        print("Metin düzenleyici bulunamadı. Bu özellik sisteminizde çalışmayabilir.")

# Üst dizine gitmeyi sağlayan işlev
def go_up():
    global current_directory
    current_directory = os.path.dirname(current_directory)
    os.chdir(current_directory)

# Geri gitmeyi sağlayan işlev
def go_back():
    global current_directory
    parent_directory = os.path.dirname(current_directory)
    if parent_directory:
        os.chdir(parent_directory)
        current_directory = parent_directory
        print(f"Moved to parent directory: {current_directory}")
    else:
        print("Already at the root directory.")

# Kullanıcı komutlarını tamamlamak için kullanılan sınıf
class CommandCompleter(Completer):
    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor()
        if word:
            completions = []
            for cmd in available_commands:
                if cmd.startswith(word):
                    completions.append(Completion(cmd, start_position=-len(word)))
            return completions
        return []

# Kullanılabilir komutlar listesi
available_commands = [
    "cd",
    "ls",
    "exit",
    "move",
    "copy",
    "delete",
    "create",
    "search",
    "up",
    "show",
    "help",
    "edit",  # "edit" komutunu ekledik
]

# Komut tamamlama işlemini sağlamak için kullanılan nesne
command_completer = CommandCompleter()

# Kullanıcıya mevcut komutları gösteren yardım mesajını gösteren işlev
def show_help():
    print("Available commands:")
    print("cd <directory>: Change the current directory.")
    print("ls: List files in the current directory.")
    print("exit: Exit the shell.")
    print("move <source> <destination>: Move a file or directory.")
    print("copy <source> <destination>: Copy a file or directory.")
    print("delete <file>: Delete a file.")
    print("create <file>: Create a new file.")
    print("search <keyword>: Search for files containing a keyword.")
    print("up: Navigate to the parent directory.")
    print("show <directory>: Show the contents of a directory.")
    print("edit <file>: Edit the content of a file")  # "edit" komutunu ekledik
    print("help: Show this help message.")

# Ana döngü, kullanıcıdan komutları alır ve işler
while True:
    try:
        user_input = prompt(
            ANSI(f'{Fore.LIGHTGREEN_EX}{gethostname()}@{Fore.YELLOW}{getuser()}:{Fore.LIGHTBLUE_EX}{current_directory}${Fore.RESET} '),
            completer=command_completer
        )

        if user_input == "":
            continue

        history.append(user_input)

        if user_input.lower() == "history":
            print("Command History:")
            for i, command in enumerate(history, start=1):
                print(f"{i}. {command}")
        elif user_input.startswith("cd "):
            directory = user_input[3:]
            try:
                os.chdir(directory)
                current_directory = os.getcwd()
            except FileNotFoundError:
                print(f"Directory not found: {directory}")
        elif user_input.lower() == "ls":
            list_files()
        elif user_input.lower() == "exit":
            exit(0)
        elif user_input.startswith("move "):
            _, src, dest = user_input.split()
            move_file(src, dest)
        elif user_input.startswith("copy "):
            _, src, dest = user_input.split()
            copy_file(src, dest)
        elif user_input.startswith("delete "):
            _, file = user_input.split()
            delete_file(file)
        elif user_input.startswith("create "):
            _, file = user_input.split()
            create_file(file)
        elif user_input.startswith("search "):
            _, keyword = user_input.split()
            search_files(keyword)
        elif user_input.lower() == "up":
            go_up()
        elif user_input.lower() == "back":
            go_back()
        elif user_input.lower() == "help":
            show_help()
        elif user_input.startswith("edit "):
            _, file = user_input.split()
            edit_file(file)
        elif user_input.lower().startswith("show "):
            directory = user_input[5:]
            show_directory_contents(directory)
        else:
            try:
                subprocess.run(user_input, shell=True, check=True)
            except subprocess.CalledProcessError:
                print(f"Command failed: {user_input}")

        log_command(getuser(), user_input)

    except KeyboardInterrupt:
        print("^C")
