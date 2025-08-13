import socket
import json

HOST = 'localhost'
PORT = 8000

def main():
    print("\n📚 Welcome to the Distributed Digital Library")
    print("🔎 To search, enter the language and genre of books you're interested in.\n")

    while True:
        try:
            language = input("Enter language (e.g., English, Telugu, Hindi): ").strip().capitalize()
            genre = input("Enter genre (e.g., Fiction, Science, History): ").strip().capitalize()

            if not language or not genre:
                print("❌ Language and genre cannot be empty.\n")
                continue

            query = f"{language}:{genre}"

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(query.encode())

                data = s.recv(8192)
                books = json.loads(data.decode())

                if not books:
                    print(f"📭 No books found for language '{language}' and genre '{genre}'.\n")
                else:
                    print(f"\n✅ Found {len(books)} books:")
                    for book in books:
                        print(f"  📖 {book['title']} by {book['author']}")
                    print()

        except KeyboardInterrupt:
            print("\n👋 Exiting client. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")

if __name__ == "__main__":
    main()
