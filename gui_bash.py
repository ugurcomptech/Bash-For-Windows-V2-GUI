import tkinter as tk
import subprocess
import os
import shutil
from colorama import Fore, init
from socket import gethostname
from getpass import getuser
from prompt_toolkit import ANSI
import datetime
from prompt_toolkit.completion import Completer, Completion

class CustomTerminal:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom Terminal")
        self.root.geometry("800x400")
        self.root.configure(bg="black")

        self.command_frame = tk.Frame(self.root, bg="black")
        self.command_frame.pack(fill=tk.X, side=tk.BOTTOM)

         # Logo eklemek için
        p1 = tk.PhotoImage(file = 'icon.png') 
        # Setting icon of master window 
        root.iconphoto(False, p1) 

        self.root.title("BASH")  # "Yeni Başlık" kısmını istediğiniz başlıkla değiştirin.


        self.current_directory = os.getcwd()
        self.hostname = gethostname()
        self.username = getuser()

        self.current_directory_label = tk.Label(self.command_frame, text=f"{self.hostname}:{self.current_directory}$ ", bg="black", fg="white", font=("Courier New", 14))
        self.current_directory_label.pack(side=tk.LEFT)



        self.command_entry = tk.Entry(self.command_frame, bg="black", fg="white", insertbackground="white", font=("Courier New", 14, "bold"), borderwidth=0, relief=tk.FLAT)
        self.command_entry.pack(fill=tk.X, expand=True, pady=0)
        self.command_entry.bind("<KeyRelease>", self.on_key_release)
        self.command_entry.bind("<Return>", self.execute_command)

        self.output_text = tk.Text(self.root, wrap=tk.WORD, bg="black", fg="white", font=("Courier New", 14))
        self.output_text.pack(fill=tk.BOTH, expand=True)

        self.input_height = 1
        self.output_text.config(state=tk.DISABLED)

    def on_key_release(self, event):
        self.input_height += 1
        self.command_entry.config(font=("Courier New", 14))



    def update_current_directory(self):
        self.current_directory = os.getcwd()
        self.current_directory_label.config(text=f"{self.hostname}:{self.current_directory}$ ")
        self.command_frame.update_idletasks()

    # Diğer fonksiyonlar burada

    def execute_command(self, event):
        command = self.command_entry.get()
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, f"{self.current_directory_label['text']}{command}\n")
        self.update_current_directory()

    def execute_command(self, event):
        command = self.command_entry.get()
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, f"{self.current_directory_label['text']}{command}\n")
        self.update_current_directory()


        if command.lower() == "history":
            self.show_history()
        elif command.startswith("cd "):
            self.change_directory(command[3:])
        elif command.lower() == "ls":
            self.list_files()
        elif command.lower() == "exit":
            self.root.quit()
        elif command.startswith("move "):
            _, src, dest = command.split()
            self.move_file(src, dest)
        elif command.startswith("copy "):
            _, src, dest = command.split()
            self.copy_file(src, dest)
        elif command.startswith("delete "):
            _, file = command.split()
            self.delete_file(file)
        elif command.startswith("create "):
            _, file = command.split()
            self.create_file(file)
        elif command.startswith("search "):
            _, keyword = command.split()
            self.search_files(keyword)
        elif command.lower() == "up":
            self.go_up()
        elif command.lower() == "back":
            self.go_back()
        elif command.lower() == "help":
            self.show_help()
        elif command.startswith("edit "):
            _, file = command.split()
            self.edit_file(file)
        elif command.lower().startswith("show "):
            directory = command[5:]
            self.show_directory_contents(directory)
        else:
            try:
                result = subprocess.check_output(command, shell=True, text=True, encoding='utf-8')
                self.output_text.insert(tk.END, result)
            except subprocess.CalledProcessError as e:
                self.output_text.insert(tk.END, f"Error: {e}\n")

        self.output_text.config(state=tk.DISABLED)
        self.command_entry.delete(0, tk.END)
        self.update_current_directory()  # Burada input yanındaki yazıyı güncelliyoruz
        self.input_height = 1  # Yüksekliği sıfırlar
        self.command_entry.config(height=self.input_height)



    def handle_up_key(self, event):
        if self.command_history_index > 0:
            self.command_history_index -= 1
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, self.command_history[self.command_history_index])

    def handle_down_key(self, event):
        if self.command_history_index < len(self.command_history) - 1:
            self.command_history_index += 1
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, self.command_history[self.command_history_index])

    def handle_up_key(self, event):
        if self.command_history_index > 0:
            self.command_history_index -= 1
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, self.command_history[self.command_history_index])

    def handle_down_key(self, event):
        if self.command_history_index < len(self.command_history) - 1:
            self.command_history_index += 1
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, self.command_history[self.command_history_index])

    def show_history(self):
        self.output_text.insert(tk.END, "Command History:\n")
        for i, command in enumerate(self.command_history, start=1):
            self.output_text.insert(tk.END, f"{i}. {command}\n")

    def change_directory(self, directory):
        try:
            os.chdir(directory)
            self.current_directory = os.getcwd()
        except FileNotFoundError:
            self.output_text.insert(tk.END, f"Directory not found: {directory}\n")

    def list_files(self):
        files = os.listdir(self.current_directory)
        self.output_text.insert(tk.END, f"Contents of directory '{self.current_directory}':\n")
        for file in files:
            self.output_text.insert(tk.END, f"{file}\n")

    def move_file(self, src, dest):
        try:
            shutil.move(src, dest)
            self.output_text.insert(tk.END, f"Moved {src} to {dest}\n")
        except FileNotFoundError:
            self.output_text.insert(tk.END, f"File not found: {src}\n")

    def copy_file(self, src, dest):
        try:
            shutil.copy2(src, dest)
            self.output_text.insert(tk.END, f"Copied {src} to {dest}\n")
        except FileNotFoundError:
            self.output_text.insert(tk.END, f"File not found: {src}\n")

    def delete_file(self, file):
        try:
            os.remove(file)
            self.output_text.insert(tk.END, f"Deleted {file}\n")
        except FileNotFoundError:
            self.output_text.insert(tk.END, f"File not found: {file}\n")

    def create_file(self, file):
        try:
            with open(file, 'w') as f:
                self.output_text.insert(tk.END, f"Created {file}\n")
        except FileExistsError:
            self.output_text.insert(tk.END, f"File already exists: {file}\n")

    def search_files(self, keyword):
        try:
            result = subprocess.run(f'findstr /M /C:"{keyword}" *.*', shell=True, cwd=self.current_directory, text=True)
            if result.returncode == 0:
                self.output_text.insert(tk.END, "Matching files:\n")
                self.output_text.insert(tk.END, result.stdout)
            else:
                self.output_text.insert(tk.END, "No matching files found.\n")
        except FileNotFoundError:
            self.output_text.insert(tk.END, "'findstr' command not found. This feature may not work on your system.\n")

    def edit_file(self, file):
        try:
            editor = "notepad.exe"
            subprocess.run([editor, file])
            self.output_text.insert(tk.END, f"Opened {file} for editing.\n")
        except FileNotFoundError:
            self.output_text.insert(tk.END, "Metin düzenleyici bulunamadı. Bu özellik sisteminizde çalışmayabilir.\n")

    def go_up(self):
        parent_directory = os.path.dirname(self.current_directory)
        if parent_directory:
            os.chdir(parent_directory)
            self.current_directory = parent_directory
            self.output_text.insert(tk.END, f"Moved to parent directory: {self.current_directory}\n")
        else:
            self.output_text.insert(tk.END, "Already at the root directory.\n")

    def go_back(self):
        parent_directory = os.path.dirname(self.current_directory)
        if parent_directory:
            os.chdir(parent_directory)
            self.current_directory = parent_directory
            self.output_text.insert(tk.END, f"Moved to parent directory: {self.current_directory}\n")
        else:
            self.output_text.insert(tk.END, "Already at the root directory.\n")

    def show_help(self):
        self.output_text.insert(tk.END, "Available commands:\n")
        self.output_text.insert(tk.END, "cd <directory>: Change the current directory.\n")
        self.output_text.insert(tk.END, "ls: List files in the current directory.\n")
        self.output_text.insert(tk.END, "exit: Exit the shell.\n")
        self.output_text.insert(tk.END, "move <source> <destination>: Move a file or directory.\n")
        self.output_text.insert(tk.END, "copy <source> <destination>: Copy a file or directory.\n")
        self.output_text.insert(tk.END, "delete <file>: Delete a file.\n")
        self.output_text.insert(tk.END, "create <file>: Create a new file.\n")
        self.output_text.insert(tk.END, "search <keyword>: Search for files containing a keyword.\n")
        self.output_text.insert(tk.END, "up: Navigate to the parent directory.\n")
        self.output_text.insert(tk.END, "show <directory>: Show the contents of a directory.\n")
        self.output_text.insert(tk.END, "edit: Used to change file content.\n")
        self.output_text.insert(tk.END, "help: Show this help message.\n")

if __name__ == "__main__":
    root = tk.Tk()
    terminal = CustomTerminal(root)
    root.bind("<Up>", terminal.handle_up_key)
    root.bind("<Down>", terminal.handle_down_key)
    root.mainloop()
