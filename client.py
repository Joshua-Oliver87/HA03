import socket
import os
import time

def send_file(client_socket):
    filename = input("Enter file path: ")
    try:
        filesize = os.path.getsize(filename)
        client_socket.send("FILE".encode())  # Inform server a file will be sent
        time.sleep(0.5)
        client_socket.send(os.path.basename(filename).encode())  # Send file name
        time.sleep(0.5)
        client_socket.send(str(filesize).encode())  # Send file size

        with open(filename, "rb") as file:
            data = file.read()
            client_socket.sendall(data)  # Send file content
        print(f"File {filename} sent successfully.")
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

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 9999))  # Connect to the server

    while True:
        message = input("Client (type 'FILE' to send a file): ")
        if message == 'FILE':
            send_file(client)
        else:
            client.send(message.encode())
            response = client.recv(1024).decode()
            if response == 'FILE':  # Server is sending a file
                recieve_file(client)
            else:
                print(f"Server: {response}")

start_client()
