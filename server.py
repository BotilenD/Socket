import socket
import os
import threading

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5001
BUFFER_SIZE = 1024
UPLOAD_DIR = 'uploads'

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def handle_client(client_socket):
    while True:
        try:

            request = client_socket.recv(BUFFER_SIZE).decode()
            if not request:
                break

            if request.startswith('UPLOAD'):
                _, filename = request.split()
                file_path = os.path.join(UPLOAD_DIR, filename)


                with open(file_path, 'wb') as f:
                    while True:
                        bytes_read = client_socket.recv(BUFFER_SIZE)
                        if not bytes_read:
                            break
                        f.write(bytes_read)
                print(f"[+] File {filename} uploaded successfully.")

            elif request.startswith('DOWNLOAD'):
                _, filename = request.split()
                file_path = os.path.join(UPLOAD_DIR, filename)


                if os.path.exists(file_path):
                    client_socket.send(f"EXISTS {os.path.getsize(file_path)}".encode())
                    with open(file_path, 'rb') as f:
                        while True:
                            bytes_read = f.read(BUFFER_SIZE)
                            if not bytes_read:
                                break
                            client_socket.sendall(bytes_read)
                    print(f"[+] File {filename} sent to the client.")
                else:
                    client_socket.send("FILE_NOT_FOUND".encode())

        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, address = server_socket.accept()
        print(f"[+] Connection from {address} established.")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    start_server()
