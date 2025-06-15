# Zenith Desktop Manager

![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

A secure and user-friendly desktop application for managing remote servers through SSH/SFTP connections with an intuitive GUI interface.

## Features

- Secure SSH and SFTP connections with modern encryption
- User-friendly GUI for both novice and advanced users
- Multi-session handling with optimized performance
- Automated file transfer scheduling
- Cross-platform support (Windows, Linux)
- Built-in updater for enhanced security

## Requirements

**Hardware:**
- **Minimum**: Dual-core 2.0 GHz CPU, 2 GB RAM, 2 GB storage
- **Recommended**: Quad-core 3.0 GHz CPU, 4-6 GB RAM, 32 GB SSD

**Software:**
- Python 3.8 or higher
- Git (for automatic updates)
- Required Python packages (install using `pip install -r requirements.txt`):
  - paramiko==3.4.0
  - cryptography==42.0.2
  - requests==2.31.0
  - tkinter (usually comes with Python)

## Installation

### Install From Source

```bash
git clone https://github.com/yourusername/zenithdesktopmanager.git
cd zenithdesktopmanager
pip install -r requirements.txt
python main.py
```

## Usage

1. Launch the application with `python main.py`
2. Click "New Connection" to add a server
3. Enter server details and authentication information
4. Connect and manage your remote files

## License

This project is licensed under the Mozilla Public License Version 2.0 License.
