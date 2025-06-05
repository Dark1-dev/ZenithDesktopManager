import tkinter as tk
from tkinter import ttk
import os
from Backend.ssh import ssh_terminal
from Backend.sftp import sftp_terminal
from Backend.ftp import ftp_terminal

from Backend.ftp import ftp_terminal
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
        self.create_sftp_tab()
        self.create_ftp_tab()
        
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
    
    def create_sftp_tab(self):
        fields = ["Username:", "Password:", "IP Address / Hostname:", "Port:"]
        
        for i, field in enumerate(fields):
            tk.Label(
                self.tab_sftp, 
                text=field, 
                bg="#ffffff", 
                fg="#333333", 
                font=("Arial", 10)
            ).grid(row=i, column=0, sticky="w", padx=10, pady=5)
            
            ent = tk.Entry(self.tab_sftp, width=45, bd=2)
            ent.grid(row=i, column=1, padx=10, pady=5)
            self.entries[f"sftp_{field}"] = ent
        
        tk.Label(
            self.tab_sftp, 
            text="SFTP Profiles:", 
            bg="#ffffff", 
            font=("Arial", 10, "bold")
        ).grid(row=4, column=0, sticky="nw", padx=10, pady=5)
        
        self.sftp_profile_listbox = tk.Listbox(
            self.tab_sftp, 
            height=4, 
            width=42, 
            bg="#f2f2f2", 
            bd=2
        )
        self.sftp_profile_listbox.grid(row=4, column=1, padx=10, pady=5)
    
    def create_ftp_tab(self):
        fields = ["Username:", "Password:", "IP Address / Hostname:", "Port:"]
        
        for i, field in enumerate(fields):
            tk.Label(
                self.tab_ftp, 
                text=field, 
                bg="#ffffff", 
                fg="#333333", 
                font=("Arial", 10)
            ).grid(row=i, column=0, sticky="w", padx=10, pady=5)
            
            ent = tk.Entry(self.tab_ftp, width=45, bd=2)
            ent.grid(row=i, column=1, padx=10, pady=5)
            self.entries[f"ftp_{field}"] = ent
        
        tk.Label(
            self.tab_ftp, 
            text="FTP Profiles:", 
            bg="#ffffff", 
            font=("Arial", 10, "bold")
        ).grid(row=4, column=0, sticky="nw", padx=10, pady=5)
        
        self.ftp_profile_listbox = tk.Listbox(
            self.tab_ftp, 
            height=4, 
            width=42, 
            bg="#f2f2f2", 
            bd=2
        )
        self.ftp_profile_listbox.grid(row=4, column=1, padx=10, pady=5)
        
        tk.Label(
            self.tab_ftp, 
            text="Connection Type:", 
            bg="#ffffff", 
            font=("Arial", 10, "bold")
        ).grid(row=5, column=0, sticky="w", padx=10, pady=5)
        
        conn_frame = tk.Frame(self.tab_ftp, bg="#ffffff")
        conn_frame.grid(row=5, column=1, sticky="w", padx=10, pady=5)
        
        self.ftp_type = tk.StringVar(value="ftp")
        tk.Radiobutton(conn_frame, text="FTP", variable=self.ftp_type, value="ftp", bg="#ffffff").pack(side="left")
        tk.Radiobutton(conn_frame, text="FTPS", variable=self.ftp_type, value="ftps", bg="#ffffff").pack(side="left")
    
    def create_buttons(self):
        button_frame = tk.Frame(self.root, bg="#e6f7ff")
        button_frame.pack(pady=20)
        
        tk.Button(
            button_frame, 
            text="About Us", 
            command=self.open_about, 
            width=15, 
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
            text="<Credits text here>", 
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
    
    def start_connection(self):
        current_tab = self.tab_control.select()
        tab_name = self.tab_control.tab(current_tab, "text")
        
        if tab_name == "SSH":
            os.environ["SSH_HOST"] = self.entries["IP Address / Hostname:"].get()
            os.environ["SSH_PORT"] = self.entries["Port:"].get()
            os.environ["SSH_USER"] = self.entries["Username:"].get()
            os.environ["SSH_PASS"] = self.entries["Password:"].get()
            
            ssh_terminal()
        elif tab_name == "SFTP":
            os.environ["SFTP_HOST"] = self.entries["sftp_IP Address / Hostname:"].get()
            os.environ["SFTP_PORT"] = self.entries["sftp_Port:"].get()
            os.environ["SFTP_USER"] = self.entries["sftp_Username:"].get()
            os.environ["SFTP_PASS"] = self.entries["sftp_Password:"].get()
            
            sftp_terminal()
        elif tab_name == "FTP":
            os.environ["FTP_HOST"] = self.entries["ftp_IP Address / Hostname:"].get()
            os.environ["FTP_PORT"] = self.entries["ftp_Port:"].get()
            os.environ["FTP_USER"] = self.entries["ftp_Username:"].get()
            os.environ["FTP_PASS"] = self.entries["ftp_Password:"].get()
            
            ftp_terminal()
        else:
            pass

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
        
        def handle_yes():
            prompt.destroy()
            self.start_connection()
        
        tk.Button(
            button_frame, 
            text="No", 
            width=10, 
            command=lambda: [prompt.destroy(), self.start_connection()]
        ).pack(side="left", padx=10)
        
        tk.Button(
            button_frame, 
            text="Yes", 
            bg="#ff6666", 
            fg="white", 
            width=10, 
            command=handle_yes
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