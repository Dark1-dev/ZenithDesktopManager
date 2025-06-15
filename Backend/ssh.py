import os
import paramiko
import threading
import sys

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
        print(f"Connected to {hostname}:{port}. Type commands below.\n(Type 'exit' or Ctrl+D to quit)\n")

        channel = client.invoke_shell()
        
        def receive_output():
            while True:
                try:
                    data = channel.recv(1024)
                    if not data:
                        break
                    sys.stdout.write(data.decode())
                    sys.stdout.flush()
                except Exception:
                    break

        output_thread = threading.Thread(target=receive_output, daemon=True)
        output_thread.start()

        while True:
            try:
                user_input = input()
                if user_input.strip().lower() == "exit":
                    break
                channel.send(user_input + "\n")
            except (EOFError, KeyboardInterrupt):
                break

        channel.close()

    except Exception as e:
        print(f"Connection failed: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    ssh_terminal()
