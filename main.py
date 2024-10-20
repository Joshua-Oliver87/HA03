import socket
import threading
import os
import time

def send_file(client_socket):
    filename = input("Enter file path to send to client: ")
    try:
        filesize = os.path.getsize(filename)
        client_socket.send("FILE".encode())  # Notify client that a file will be sent
        time.sleep(0.5)
        client_socket.send(os.path.basename(filename).encode())  # Send file name
        time.sleep(0.5)
        client_socket.send(str(filesize).encode())  # Send file size

        with open(filename, "rb") as file:
            data = file.read()
            client_socket.sendall(data)  # Send file data
        print(f"File {filename} sent successfully to client.")
    except FileNotFoundError:
        print(f"File not found: {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

def recieve_file(client_socket):
    filename = client_socket.recv(1024).decode()  # Receive the file name
    filesize = int(client_socket.recv(1024).decode())  # Receive the file size
    with open(filename, "wb") as file:
        data = client_socket.recv(filesize)  # Receive the file content
        file.write(data)
    print(f"File {filename} received successfully.")

def handle_client(client_socket):
    while True:
        message = client_socket.recv(1024).decode()
        if message == 'FILE':  # If the client is sending a file
            recieve_file(client_socket)
        else:
            print(f"Client: {message}")
            # Server can send a message or a file
            response = input("Server (type 'FILE' to send a file): ")
            if response == 'FILE':
                send_file(client_socket)  # Server sends a file to the client
            else:
                client_socket.send(response.encode())  # Server sends a message

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(5)
    print("Server listening on port 9999")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

start_server()
