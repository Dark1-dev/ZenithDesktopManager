import sqlite3
import os
from cryptography.fernet import Fernet
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="credentials.db"):
        self.db_path = db_path
        self._init_db()
        self._init_encryption()
    
    def _init_encryption(self):
        key_file = "encryption.key"
        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(self.key)
        self.cipher = Fernet(self.key)

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS connections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    protocol TEXT NOT NULL CHECK(protocol IN ('FTP', 'SFTP', 'SSH')),
                    host TEXT NOT NULL,
                    port INTEGER NOT NULL DEFAULT 22,
                    username TEXT NOT NULL,
                    password_id INTEGER,
                    key_pair_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (password_id) REFERENCES passwords(id),
                    FOREIGN KEY (key_pair_id) REFERENCES key_pairs(id)
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS passwords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    encrypted_value TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS key_pairs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    public_key TEXT NOT NULL,
                    private_key TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def save_connection(self, name, protocol, host, port, username, password):
        with sqlite3.connect(self.db_path) as conn:
            encrypted_password = self.cipher.encrypt(password.encode())
            cursor = conn.execute(
                "INSERT INTO passwords (encrypted_value) VALUES (?)",
                (encrypted_password,)
            )
            password_id = cursor.lastrowid

            conn.execute("""
                INSERT INTO connections (name, protocol, host, port, username, password_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, protocol, host, port, username, password_id))

    def get_connections(self, protocol=None):
        with sqlite3.connect(self.db_path) as conn:
            if protocol:
                cursor = conn.execute("""
                    SELECT c.*, p.encrypted_value 
                    FROM connections c
                    JOIN passwords p ON c.password_id = p.id
                    WHERE c.protocol = ?
                """, (protocol,))
            else:
                cursor = conn.execute("""
                    SELECT c.*, p.encrypted_value 
                    FROM connections c
                    JOIN passwords p ON c.password_id = p.id
                """)
            
            connections = []
            for row in cursor:
                conn_dict = {
                    'id': row[0],
                    'name': row[1],
                    'protocol': row[2],
                    'host': row[3],
                    'port': row[4],
                    'username': row[5],
                    'password': self.cipher.decrypt(row[-1]).decode()
                }
                connections.append(conn_dict)
            return connections

    def delete_connection(self, connection_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT password_id FROM connections WHERE id = ?",
                (connection_id,)
            )
            password_id = cursor.fetchone()[0]
            
            conn.execute("DELETE FROM connections WHERE id = ?", (connection_id,))
            conn.execute("DELETE FROM passwords WHERE id = ?", (password_id,)) 