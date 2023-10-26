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



init(autoreset=True)

history = []
current_directory = os.getcwd()



def show_directory_contents(directory):
    print(f"Contents of directory '{directory}':")
    list_files(directory)


log_file = "command_log.txt"  # Komut günlüğünün kaydedileceği dosya


def log_command(user, command):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(f"{timestamp} - User: {user}, Command: {command}\n")


def move_file(src, dest):
    try:
        shutil.move(src, dest)
        print(f"Moved {src} to {dest}")
    except FileNotFoundError:
        print(f"File not found: {src}")

def move_file_command(src, dest):
    try:
        shutil.move(src, dest)
        print(f"Moved {src} to {dest}")
    except FileNotFoundError:
        print(f"File not found: {src}")

def copy_file(src, dest):
    try:
        shutil.copy2(src, dest)
        print(f"Copied {src} to {dest}")
    except FileNotFoundError:
        print(f"File not found: {src}")

def delete_file(file):
    try:
        os.remove(file)
        print(f"Deleted {file}")
    except FileNotFoundError:
        print(f"File not found: {file}")

def create_file(file):
    try:
        with open(file, 'w') as f:
            print(f"Created {file}")
    except FileExistsError:
        print(f"File already exists: {file}")

def list_files():
    files = os.listdir(current_directory)
    for file in files:
        print(file)

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

def go_up():
    global current_directory
    current_directory = os.path.dirname(current_directory)
    os.chdir(current_directory)


def go_back():
    global current_directory
    parent_directory = os.path.dirname(current_directory)
    if parent_directory:
        os.chdir(parent_directory)
        current_directory = parent_directory
        print(f"Moved to parent directory: {current_directory}")
    else:
        print("Already at the root directory.")

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

]


command_completer = CommandCompleter()


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
    print("help: Show this help message.")



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
