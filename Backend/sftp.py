import os
import paramiko

def sftp_terminal():
    hostname = os.environ.get("SFTP_HOST")
    port = os.environ.get("SFTP_PORT")
    username = os.environ.get("SFTP_USER")
    password = os.environ.get("SFTP_PASS")

    if not all([hostname, port, username, password]):
        print("Missing environment variables (SFTP_HOST, SFTP_PORT, SFTP_USER, SFTP_PASS).")
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
        print("Type commands below (ls, cd <dir>, get <local> [remote], put <local> [remote], pwd, exit)")

        while True:
            cmd = input(f"{username}@{hostname} (sftp)> ").strip()
            if cmd.lower() == "exit":
                break

            elif cmd == "ls":
                try:
                    for f in sftp.listdir():
                        print(f)
                except Exception as e:
                    print(f"ls error: {e}")

            elif cmd == "pwd":
                try:
                    print(sftp.getcwd())
                except Exception as e:
                    print(f"pwd error: {e}")

            elif cmd.startswith("cd "):
                try:
                    path = cmd.split(" ", 1)[1]
                    sftp.chdir(path)
                except Exception as e:
                    print(f"cd error: {e}")

            elif cmd.startswith("get "):
                try:
                    parts = cmd.split(" ")
                    remote_file = parts[1]
                    local_file = parts[2] if len(parts) > 2 else os.path.basename(remote_file)
                    sftp.get(remote_file, local_file)
                    print(f"Downloaded: {remote_file} → {local_file}")
                except Exception as e:
                    print(f"get error: {e}")

            elif cmd.startswith("put "):
                try:
                    parts = cmd.split(" ")
                    local_file = parts[1]
                    remote_file = parts[2] if len(parts) > 2 else os.path.basename(local_file)

                    local_file = os.path.normpath(local_file)

                    if not os.path.isfile(local_file):
                        print(f"Local file does not exist: {local_file}")
                        continue

                    sftp.put(local_file, remote_file)
                    print(f"Uploaded: {local_file} → {remote_file}")
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
