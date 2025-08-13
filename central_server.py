import socket
import threading
import json
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import log

HOST = 'localhost'
PORT = 8000

# Load from config
with open('config/routing_config.json') as f:
    CONFIG = json.load(f)

def forward_to_language_server(language, genre):
    try:
        port = CONFIG["languages"].get(language)
        if port is None:
            return b'[]'
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, port))
            s.sendall(genre.encode())
            return s.recv(4096)
    except Exception as ex:
        log("Central Server", f"Failed to connect to language server: {ex}")
        return b'[]'

def handle_client(conn, addr):
    log("Central Server", f"Connected by {addr}")
    try:
        data = conn.recv(1024).decode()
        language, genre = data.split(':')
        result = forward_to_language_server(language, genre)
        conn.sendall(result)
    finally:
        conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        log("Central Server", f"Listening on port {PORT}...")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()