import socket, threading, sys, json, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import log

HOST = 'localhost'

# Read genre and port from command line
if len(sys.argv) != 3:
    print("Usage: python genre_server.py <Genre> <Port>")
    sys.exit(1)

LANGUAGE = sys.argv[1].capitalize()
PORT = int(sys.argv[2])

with open('config/routing_config.json') as f:
    CONFIG = json.load(f)

GENRE_PORTS = CONFIG["genres"]

def forward_request_to_genre(genre):
    try:
        port = GENRE_PORTS.get(genre)
        if port is None:
            return b'[]'
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, port))
            s.sendall(LANGUAGE.encode())  # Send language
            return s.recv(4096)
    except Exception as ex:
        log(LANGUAGE, f"Error connecting to genre server: {ex}")
        return b'[]'

def handle_client(conn, addr):
    log(LANGUAGE, f"Connected by {addr}")
    try:
        genre = conn.recv(1024).decode()
        data = forward_request_to_genre(genre)
        conn.sendall(data)
    finally:
        conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        log(LANGUAGE, f"Listening to port {PORT}...")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()
