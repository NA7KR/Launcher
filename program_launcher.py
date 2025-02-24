"""
Copyright © 2024 NA7KR Kevin Roberts. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage
import subprocess
import time
import json
import os
import sys

PROGRAM_LIST_FILE = "program_list.json"

# Function to get resource path (for PyInstaller compatibility)
def resource_path(relative_path):
    """ Get the absolute path to resources, works for dev and PyInstaller """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class ProgramLauncherApp:
    def __init__(self, root):
        self.root = root
        
        # Load and set an image in the title bar
        self.icon_image = PhotoImage(file=resource_path("icon.png"))
        self.root.iconphoto(False, self.icon_image)  # Set window icon
        
        # Set the title with a Unicode symbol for visual enhancement
        self.root.title("⚡ Program Launcher by NA7KR")
        self.root.geometry("500x500")
        
        self.programs = []
        
        frame = tk.Frame(root)
        frame.pack(pady=10)
        
        self.listbox = tk.Listbox(frame, width=50, height=15)
        self.listbox.grid(row=0, column=0, padx=10)
        
        button_frame = tk.Frame(frame)
        button_frame.grid(row=0, column=1, padx=5)
        
        self.move_up_button = tk.Button(button_frame, text="Move Up", command=self.move_up)
        self.move_up_button.pack(fill=tk.X)
        
        self.move_down_button = tk.Button(button_frame, text="Move Down", command=self.move_down)
        self.move_down_button.pack(fill=tk.X)
        
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
        
        # Add an image below the start button
        self.na7kr_image = PhotoImage(file=resource_path("na7kr.png"))
        self.na7kr_label = tk.Label(root, image=self.na7kr_image)
        self.na7kr_label.pack()
        
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
    
    def move_up(self):
        selected = self.listbox.curselection()
        if selected and selected[0] > 0:
            idx = selected[0]
            self.programs[idx], self.programs[idx - 1] = self.programs[idx - 1], self.programs[idx]
            self.listbox.delete(idx)
            self.listbox.insert(idx - 1, f"{self.programs[idx - 1][0]} (Delay: {self.programs[idx - 1][1]}s)")
            self.listbox.select_set(idx - 1)
            self.save_list()
    
    def move_down(self):
        selected = self.listbox.curselection()
        if selected and selected[0] < len(self.programs) - 1:
            idx = selected[0]
            self.programs[idx], self.programs[idx + 1] = self.programs[idx + 1], self.programs[idx]
            self.listbox.delete(idx)
            self.listbox.insert(idx + 1, f"{self.programs[idx + 1][0]} (Delay: {self.programs[idx + 1][1]}s)")
            self.listbox.select_set(idx + 1)
            self.save_list()
    
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
