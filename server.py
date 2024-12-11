import socket
import threading
import os
import sys

clients = {}
shared_files = os.getenv("SERVER_SHARED_FILES")

def server_start():
    try:
        # Create socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = int(sys.argv[1]) if len(sys.argv) > 1 else 12300
        server_socket.bind(('localhost', port))
        server_socket.listen(5)
        print(f"Server is ready to receive on port {port}")
        
        while True:
            client_socket, address = server_socket.accept()
            print(f"New client with ip: {address[0]} and Port: {address[1]}")
            
            # Create a new thread for each client
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()
            
    except KeyboardInterrupt:
        print("\nServer terminated.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        for client in clients:
            remove_client(client)
        server_socket.close()

def handle_client(client_socket):
    try:
        username = client_socket.recv(1024).decode()  # Receive the username
        clients[client_socket] = username
        print(f"New client connected: {username}")
        
        welcome_message = f"Welcome {username} to server".encode()
        client_socket.send(welcome_message)
        boardcast_message(f"[{username}] has joined the chat.", client_socket)

        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            
            if data.lower() == "/quit":  # Exit server
                remove_client(client_socket)
                break
            
            elif data.lower() == "/file":  # Access shared files
                li, count = access_files()
                client_socket.send(f"{count} file(s) available: {li}".encode())
            
            elif data.startswith("/download"):  # Download a file
                filename = data.split(" ", 1)[1]
                files = os.listdir(shared_files)
                size = os.path.getsize(os.path.join(shared_files, filename))
                if filename in files:
                    client_socket.send(f"Download_File {username} {filename} {size}".encode())
                    download(client_socket, filename)
                else:
                    client_socket.send(f"File {filename} not found".encode())
            
            elif data.startswith("/boardcast"):  # Broadcast message
                message = f"[{username}] " + data.split(" ", 1)[1]
                boardcast_message(message, client_socket)
                print(f"Broadcasted message: {message}")
            
            elif data.startswith("/unicast"):  # Send private message
                receiver = data.split(" ", 2)[1]
                message = f"[{username}] " + data.split(" ", 2)[2]
                send_private_message(receiver, message, client_socket)
            
    except Exception as e:
        print(f"Error handling client {clients.get(client_socket, 'unknown')}: {e}")
    finally:
        remove_client(client_socket)

def boardcast_message(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except Exception as e:
                print(f"Error sending message to client: {e}")

def send_private_message(receiver, message, sender_socket):
    for client, name in clients.items():
        if name == receiver:
            try:
                client.send(message.encode())
                return
            except Exception as e:
                print(f"Error sending private message: {e}")
                return
    sender_socket.send("User not found.".encode())

def remove_client(client_socket):
    if client_socket in clients:
        username = clients[client_socket]
        print(f"Client {username} has disconnected.")
        boardcast_message(f"[{username}] has left the chat.", client_socket)
        del clients[client_socket]
        client_socket.close()

def access_files():
    if not os.path.exists(shared_files):
        return "No shared files"
    else:
        files = os.listdir(shared_files)
        return files, len(files)

def download(client_socket, filename):
    try:
        path = os.path.join(shared_files, filename)
        with open(path, "rb") as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                client_socket.send(data)
        print(f"File {filename} sent successfully.")
    except Exception as e:
        print(f"Error sending file {filename}: {e}")

if __name__ == "__main__":
    server_start()
