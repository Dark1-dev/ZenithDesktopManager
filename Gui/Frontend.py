import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import os
import requests
import subprocess
import sys
from Backend.ssh import ssh_terminal
from Backend.sftp import sftp_terminal
from Backend.ftp import ftp_terminal
from Backend.db_manager import DatabaseManager

class ZenithDesktopManager:
    def __init__(self):
        self.root = tk.Tk()
        self.entries = {}
        self.db = DatabaseManager()
        self.current_version = "1.0.0"
        self.github_repo = "https://github.com/Dark1-dev/ZenithDesktopManager.git"
        self.setup_ui()
        self.load_profiles()
    
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
        
        self.ssh_profile_listbox = tk.Listbox(
            self.tab_ssh, 
            height=4, 
            width=42, 
            bg="#f2f2f2", 
            bd=2
        )
        self.ssh_profile_listbox.grid(row=4, column=1, padx=10, pady=5)
    
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
            text="Check for Updates", 
            command=self.check_for_updates,
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
    
    def show_save_prompt(self):
        current_tab = self.tab_control.select()
        tab_name = self.tab_control.tab(current_tab, "text")
        
        if tab_name == "SSH":
            host = self.entries["IP Address / Hostname:"].get()
            port = int(self.entries["Port:"].get())
            username = self.entries["Username:"].get()
            password = self.entries["Password:"].get()
        elif tab_name == "SFTP":
            host = self.entries["sftp_IP Address / Hostname:"].get()
            port = int(self.entries["sftp_Port:"].get())
            username = self.entries["sftp_Username:"].get()
            password = self.entries["sftp_Password:"].get()
        else:
            host = self.entries["ftp_IP Address / Hostname:"].get()
            port = int(self.entries["ftp_Port:"].get())
            username = self.entries["ftp_Username:"].get()
            password = self.entries["ftp_Password:"].get()
        
        existing_connections = self.db.get_connections(tab_name)
        for conn in existing_connections:
            if (conn['host'] == host and 
                conn['port'] == port and 
                conn['username'] == username and 
                conn['password'] == password):
                self.start_connection()
                return
        
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
            name = simpledialog.askstring("Save Connection", "Enter a name for this connection:")
            if name:
                if tab_name == "SSH":
                    self.db.save_connection(
                        name=name,
                        protocol="SSH",
                        host=host,
                        port=port,
                        username=username,
                        password=password
                    )
                elif tab_name == "SFTP":
                    self.db.save_connection(
                        name=name,
                        protocol="SFTP",
                        host=host,
                        port=port,
                        username=username,
                        password=password
                    )
                elif tab_name == "FTP":
                    self.db.save_connection(
                        name=name,
                        protocol="FTP",
                        host=host,
                        port=port,
                        username=username,
                        password=password
                    )
                self.load_profiles()
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
    
    def load_profiles(self):
        self.ssh_profile_listbox.delete(0, tk.END)
        self.sftp_profile_listbox.delete(0, tk.END)
        self.ftp_profile_listbox.delete(0, tk.END)
        
        for protocol in ['SSH', 'SFTP', 'FTP']:
            connections = self.db.get_connections(protocol)
            listbox = getattr(self, f"{protocol.lower()}_profile_listbox")
            for conn in connections:
                listbox.insert(tk.END, conn['name'])
    
    def check_for_updates(self):
        try:
            api_url = "https://api.github.com/repos/Dark1-dev/ZenithDesktopManager/releases/latest"
            response = requests.get(api_url)
            
            if response.status_code == 200:
                latest_version = response.json()["tag_name"].replace("v", "")
                
                if self.compare_versions(latest_version, self.current_version) > 0:
                    if messagebox.askyesno("Update Available", 
                                         f"A new version ({latest_version}) is available!\n"
                                         f"Current version: {self.current_version}\n\n"
                                         "Would you like to update now?"):
                        self.update_application()
                else:
                    messagebox.showinfo("Up to Date", 
                                      f"You are running the latest version ({self.current_version})")
            else:
                messagebox.showerror("Update Check Failed", 
                                   "Could not check for updates. Please try again later.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while checking for updates: {str(e)}")
    
    def compare_versions(self, version1, version2):
        v1_parts = [int(x) for x in version1.split('.')]
        v2_parts = [int(x) for x in version2.split('.')]
        
        for i in range(max(len(v1_parts), len(v2_parts))):
            v1 = v1_parts[i] if i < len(v1_parts) else 0
            v2 = v2_parts[i] if i < len(v2_parts) else 0
            
            if v1 > v2:
                return 1
            elif v1 < v2:
                return -1
        return 0
    
    def update_application(self):
        try:
            temp_dir = os.path.join(os.path.expanduser("~"), "ZenithDesktopManager_update")
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            
            subprocess.run(["git", "clone", self.github_repo, temp_dir], check=True)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            if sys.platform == "win32":
                # Windows update script
                update_script = f"""@echo off
timeout /t 2 /nobreak
xcopy /y /e "{temp_dir}\\*" "{current_dir}\\"
rmdir /s /q "{temp_dir}"
start "" "{sys.executable}" "{os.path.join(current_dir, 'main.py')}"
"""
                script_path = os.path.join(current_dir, "update.bat")
                with open(script_path, "w") as f:
                    f.write(update_script)
                subprocess.Popen(["cmd", "/c", script_path])
            else:
                # Unix-like systems update script
                update_script = f"""#!/bin/bash
sleep 2
cp -r "{temp_dir}/"* "{current_dir}/"
rm -rf "{temp_dir}"
"{sys.executable}" "{os.path.join(current_dir, 'main.py')}" &
"""
                script_path = os.path.join(current_dir, "update.sh")
                with open(script_path, "w") as f:
                    f.write(update_script)
                os.chmod(script_path, 0o755)  # Make the script executable
                subprocess.Popen(["/bin/bash", script_path])
            
            self.root.quit()
            
        except Exception as e:
            messagebox.showerror("Update Failed", 
                               f"An error occurred while updating: {str(e)}\n"
                               "Please try updating manually from GitHub.")
    
    def run(self):
        self.root.mainloop()