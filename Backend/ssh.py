import os
import paramiko

def ssh_terminal():
    hostname = os.environ.get("SSH_HOST")
    port = os.environ.get("SSH_PORT")
    username = os.environ.get("SSH_USER")
    password = os.environ.get("SSH_PASS")

    if not all([hostname, port, username, password]):
        print("Missing environment variables.")
        return

    try:
        port = int(port)
    except ValueError:
        print("Invalid port number.")
        return

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, port=port, username=username, password=password)
        print(f"Connected to {hostname}:{port}. Type commands below.\n(Type 'exit' to quit)\n")

        while True:
            cmd = input(f"{username}@{hostname}$ ")
            if cmd.strip().lower() == "exit":
                break
            stdin, stdout, stderr = client.exec_command(cmd)
            print(stdout.read().decode(), end='')
            print(stderr.read().decode(), end='')

    except Exception as e:
        print(f"Connection failed: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    ssh_terminal()
