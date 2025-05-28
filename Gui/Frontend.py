import tkinter as tk
from tkinter import ttk

class ZenithDesktopManager:
    def __init__(self):
        self.root = tk.Tk()
        self.entries = {}
        self.setup_ui()
    
    def setup_ui(self):
        self.root.title("Zenith Desktop Controller")
        self.root.geometry("650x500")
        self.root.configure(bg="#e6f7ff")

        tk.Label(
            self.root, 
            text="Zenith Desktop Controller", 
            font=("Helvetica", 16, "bold"), 
            bg="#e6f7ff", 
            fg="#003366"
        ).pack(pady=10)
        
        self.create_tabs()
        self.create_ssh_tab()
        self.create_buttons()
    
    def create_tabs(self):
        self.tab_control = ttk.Notebook(self.root)
        
        self.tab_ssh = tk.Frame(self.tab_control, bg="#ffffff")
        self.tab_sftp = tk.Frame(self.tab_control, bg="#ffffff")
        self.tab_ftp = tk.Frame(self.tab_control, bg="#ffffff")
        
        self.tab_control.add(self.tab_ssh, text="SSH")
        self.tab_control.add(self.tab_sftp, text="SFTP")
        self.tab_control.add(self.tab_ftp, text="FTP")
        
        self.tab_control.pack(fill="x", padx=10)
    
    def create_ssh_tab(self):
        fields = ["Username:", "Password:", "IP Address / Hostname:", "Port:"]
        
        for i, field in enumerate(fields):
            tk.Label(
                self.tab_ssh, 
                text=field, 
                bg="#ffffff", 
                fg="#333333", 
                font=("Arial", 10)
            ).grid(row=i, column=0, sticky="w", padx=10, pady=5)
            
            ent = tk.Entry(self.tab_ssh, width=45, bd=2)
            ent.grid(row=i, column=1, padx=10, pady=5)
            self.entries[field] = ent
        
        tk.Label(
            self.tab_ssh, 
            text="Profiles:", 
            bg="#ffffff", 
            font=("Arial", 10, "bold")
        ).grid(row=4, column=0, sticky="nw", padx=10, pady=5)
        
        self.profile_listbox = tk.Listbox(
            self.tab_ssh, 
            height=4, 
            width=42, 
            bg="#f2f2f2", 
            bd=2
        )
        self.profile_listbox.grid(row=4, column=1, padx=10, pady=5)
    
    def create_buttons(self):
        button_frame = tk.Frame(self.root, bg="#e6f7ff")
        button_frame.pack(pady=20)
        
        tk.Button(
            button_frame, 
            text="About Us",
            width=15,
            command=self.open_about,
            bg="#d9d9d9", 
            font=("Arial", 10)
        ).pack(side="left", padx=10)
        
        tk.Button(
            button_frame, 
            text="Stop Connection", 
            width=15, 
            bg="#d9d9d9", 
            font=("Arial", 10)
        ).pack(side="left", padx=10)
        
        tk.Button(
            button_frame, 
            text="Start", 
            width=15, 
            bg="#ff6666", 
            fg="white", 
            font=("Arial", 10, "bold"), 
            command=self.show_save_prompt
        ).pack(side="left", padx=10)

    def open_about(self):
        about = tk.Toplevel(self.root)
        about.title("About us - Zenith Software")
        about.geometry("400x300")
        about.configure(bg="#f0f0f0")
        
        tk.Label(
            about, 
            text="Logo", 
            relief="solid", 
            width=20, 
            height=6, 
            bg="#e6f7ff"
        ).pack(pady=10)
        
        tk.Label(
            about, 
            text="Credits:", 
            anchor="w", 
            bg="#f0f0f0", 
            font=("Helvetica", 10, "bold")
        ).pack(anchor="w", padx=10)
        
        tk.Label(
            about, 
            text=" Saan Shepherd Sarkar – Manager/Backend Programmer\n Pranto Malaker – GUI Developer\n Arni During Gomes – Database Scientist\n Md Asif Shovani - Backend Developer\n Jannatul Ferdous Sharna - Tests management", 
            anchor="w", 
            relief="solid", 
            width=45, 
            height=5, 
            bg="white"
        ).pack(padx=10, pady=5)
        
        tk.Button(
            about, 
            text="OK", 
            bg="#ff6666", 
            fg="white", 
            width=10, 
            command=about.destroy

        ).pack(pady=10)
    
    def show_save_prompt(self):
        prompt = tk.Toplevel(self.root)
        prompt.title("Save Information?")
        prompt.geometry("350x150")
        prompt.configure(bg="#f0f8ff")
        
        tk.Label(
            prompt, 
            text="Do you want to save these information for future use?", 
            bg="#f0f8ff", 
            font=("Helvetica", 10)
        ).pack(pady=20)
        
        button_frame = tk.Frame(prompt, bg="#f0f8ff")
        button_frame.pack()
        
        tk.Button(
            button_frame, 
            text="No", 
            width=10, 
            command=prompt.destroy
        ).pack(side="left", padx=10)
        
        tk.Button(
            button_frame, 
            text="Yes", 
            bg="#ff6666", 
            fg="white", 
            width=10, 
            command=prompt.destroy
        ).pack(side="left", padx=10)
    
    def run(self):
        self.root.mainloop()
    
    def get_connection_info(self):
        return {
            field.rstrip(':'): entry.get() 
            for field, entry in self.entries.items()
        }
    
    def set_connection_info(self, info):
        for field, entry in self.entries.items():
            field_key = field.rstrip(':')
            if field_key in info:
                entry.delete(0, tk.END)
                entry.insert(0, info[field_key])