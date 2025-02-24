import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import time
import json
import os

PROGRAM_LIST_FILE = "program_list.json"

class ProgramLauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Program Launcher")
        self.root.geometry("500x400")
        
        self.programs = []
        
        self.listbox = tk.Listbox(root, width=50, height=15)
        self.listbox.pack(pady=10)
        
        self.add_button = tk.Button(root, text="Add Program", command=self.add_program)
        self.add_button.pack()
        
        self.remove_button = tk.Button(root, text="Remove Selected", command=self.remove_program)
        self.remove_button.pack()
        
        self.delay_label = tk.Label(root, text="Delay (seconds) between programs:")
        self.delay_label.pack()
        
        self.delay_entry = tk.Entry(root)
        self.delay_entry.pack()
        self.delay_entry.insert(0, "2")
        
        self.start_button = tk.Button(root, text="Start Programs", command=self.start_programs)
        self.start_button.pack(pady=10)
        
        self.save_button = tk.Button(root, text="Save List", command=self.save_list)
        self.save_button.pack()
        
        self.load_button = tk.Button(root, text="Load List", command=self.load_list)
        self.load_button.pack()
        
        self.load_list()  # Auto-load saved list on start
    
    def add_program(self):
        filepath = filedialog.askopenfilename(filetypes=[("Executable Files", "*.exe")])
        if filepath:
            delay = self.get_delay_time()
            self.programs.append((filepath, delay))
            self.listbox.insert(tk.END, f"{filepath} (Delay: {delay}s)")
            self.save_list()  # Auto-save on add
    
    def remove_program(self):
        selected = self.listbox.curselection()
        if selected:
            self.programs.pop(selected[0])
            self.listbox.delete(selected[0])
            self.save_list()  # Auto-save on remove
    
    def start_programs(self):
        try:
            for program, delay in self.programs:
                subprocess.Popen(program, shell=True)
                time.sleep(delay)
        except ValueError:
            messagebox.showerror("Error", "Invalid delay time in program list.")
    
    def save_list(self):
        with open(PROGRAM_LIST_FILE, "w") as file:
            json.dump(self.programs, file)
    
    def load_list(self):
        if os.path.exists(PROGRAM_LIST_FILE):
            try:
                with open(PROGRAM_LIST_FILE, "r") as file:
                    self.programs = json.load(file)
                    self.listbox.delete(0, tk.END)
                    for program, delay in self.programs:
                        self.listbox.insert(tk.END, f"{program} (Delay: {delay}s)")
            except (FileNotFoundError, json.JSONDecodeError):
                messagebox.showerror("Error", "Failed to load program list.")
    
    def get_delay_time(self):
        try:
            return int(self.delay_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid delay time.")
            return 2

if __name__ == "__main__":
    root = tk.Tk()
    app = ProgramLauncherApp(root)
    root.mainloop()
