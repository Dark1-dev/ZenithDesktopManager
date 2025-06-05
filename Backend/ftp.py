import os
from ftplib import FTP

def ftp_terminal():
    host = os.environ.get("FTP_HOST")
    port = int(os.environ.get("FTP_PORT"))
    user = os.environ.get("FTP_USER")
    password = os.environ.get("FTP_PASS")

    ftp = FTP()
    try:
        ftp.connect(host, port)
        ftp.login(user, password)
        print(f"Connected to {host}:{port} via FTP")
        print("Commands: ls, pwd, cd <dir>, get <file>, put <file>, exit")

        while True:
            cmd = input("ftp> ").strip()
            if cmd == "exit":
                break
            elif cmd == "ls":
                ftp.retrlines("LIST")
            elif cmd == "pwd":
                print(ftp.pwd())
            elif cmd.startswith("cd "):
                _, path = cmd.split(" ", 1)
                ftp.cwd(path)
            elif cmd.startswith("get "):
                _, filename = cmd.split(" ", 1)
                with open(filename, "wb") as f:
                    ftp.retrbinary(f"RETR {filename}", f.write)
                print(f"Downloaded {filename}")
            elif cmd.startswith("put "):
                _, filename = cmd.split(" ", 1)
                with open(filename, "rb") as f:
                    ftp.storbinary(f"STOR {filename}", f)
                print(f"Uploaded {filename}")
            else:
                print("Unknown command")
    except Exception as e:
        print("FTP Error:", e)
    finally:
        ftp.quit()

if __name__ == "__main__":
    ftp_terminal()