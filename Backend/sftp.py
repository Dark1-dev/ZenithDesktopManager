import os
import paramiko

def sftp_terminal():
    hostname = os.environ.get("SFTP_HOST")
    port = os.environ.get("SFTP_PORT")
    username = os.environ.get("SFTP_USER")
    password = os.environ.get("SFTP_PASS")

    if not all([hostname, port, username, password]):
        print("Missing environment variables.")
        return

    try:
        port = int(port)
    except ValueError:
        print("Invalid port number.")
        return

    try:
        transport = paramiko.Transport((hostname, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        print(f"Connected to {hostname}:{port} via SFTP.")
        print("Type commands below (ls, cd <dir>, get <file>, put <file>, pwd, exit)")

        while True:
            cmd = input(f"{username}@{hostname} (sftp)> ").strip()
            if cmd.lower() == "exit":
                break
            elif cmd == "ls":
                for f in sftp.listdir():
                    print(f)
            elif cmd == "pwd":
                print(sftp.getcwd())
            elif cmd.startswith("cd "):
                try:
                    path = cmd.split(" ", 1)[1]
                    sftp.chdir(path)
                except Exception as e:
                    print(f"cd error: {e}")
            elif cmd.startswith("get "):
                try:
                    filename = cmd.split(" ", 1)[1]
                    sftp.get(filename, filename)
                    print(f"Downloaded: {filename}")
                except Exception as e:
                    print(f"get error: {e}")
            elif cmd.startswith("put "):
                try:
                    filename = cmd.split(" ", 1)[1]
                    sftp.put(filename, filename)
                    print(f"Uploaded: {filename}")
                except Exception as e:
                    print(f"put error: {e}")
            else:
                print("Unknown command.")
    except Exception as e:
        print(f"Connection failed: {e}")
    finally:
        try:
            sftp.close()
            transport.close()
        except:
            pass

if __name__ == "__main__":
    sftp_terminal()
