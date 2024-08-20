import socket
import os

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5001
BUFFER_SIZE = 1024


def upload_file(filename, client_socket):
    client_socket.send(f"UPLOAD {filename}".encode())

    with open(filename, 'rb') as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            client_socket.sendall(bytes_read)
    print(f"[+] File {filename} uploaded successfully.")


def download_file(filename, client_socket):
    client_socket.send(f"DOWNLOAD {filename}".encode())

    response = client_socket.recv(BUFFER_SIZE).decode()

    if response.startswith("EXISTS"):
        filesize = int(response.split()[1])
        with open(f"downloaded_{filename}", 'wb') as f:
            while filesize > 0:
                bytes_read = client_socket.recv(BUFFER_SIZE)
                f.write(bytes_read)
                filesize -= len(bytes_read)
        print(f"[+] File {filename} downloaded successfully.")
    else:
        print("[-] File not found on the server.")


def client_menu():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    while True:
        choice = input("Enter choice (upload/download/exit): ").strip().lower()
        if choice == 'upload':
            filename = input("Enter filename to upload: ")
            if os.path.exists(filename):
                upload_file(filename, client_socket)
            else:
                print("[-] File not found.")

        elif choice == 'download':
            filename = input("Enter filename to download: ")
            download_file(filename, client_socket)

        elif choice == 'exit':
            client_socket.close()
            break

        else:
            print("Invalid choice. Please choose 'upload', 'download', or 'exit'.")


if __name__ == "__main__":
    client_menu()
