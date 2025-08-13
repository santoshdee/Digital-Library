import socket
import threading
import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import log
from database_config.db_config import get_db_connection
from utils.cache import get_cache, set_cache


HOST = 'localhost'

# Read genre and port from command line
if len(sys.argv) != 3:
    print("Usage: python genre_server.py <Genre> <Port>")
    sys.exit(1)

GENRE = sys.argv[1].capitalize()
PORT = int(sys.argv[2])

def fetch_books_from_db(language):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT title, author FROM books WHERE genre = %s AND language = %s",
            (GENRE, language)
        )
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except Exception as ex:
        log(GENRE, f"DB Error: {ex}")
        return []

def handle_client(conn, addr):
    log(GENRE, f"Connected by {addr}")
    try:
        language = conn.recv(1024).decode().strip().capitalize()
        cache_key = (GENRE, language)
        
        books = get_cache(cache_key)
        if books:
            log(GENRE, f"Cache hit for ({GENRE}, {language})")
        else:
            log(GENRE, f"Cache miss for ({GENRE}, {language}), fetching from DB")
            books = fetch_books_from_db(language)
            set_cache(cache_key, books)

        conn.sendall(json.dumps(books).encode())
    except Exception as ex:
        log(GENRE, f"Error handling client {addr}: {ex}")
        conn.sendall(json.dumps([]).encode())
    finally:
        conn.close()
        log(GENRE, f"Connection closed for {addr}")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        log(GENRE, f"Listening on port {PORT}...")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()
