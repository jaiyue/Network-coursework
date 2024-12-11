import socket
import sys
import threading
import os

def client_start():
    try:
        username = sys.argv[1]
        ip = sys.argv[2]
        port = int(sys.argv[3])

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, port))
        print(f"Connected successfully as {username} to {ip}:{port}")
        client_socket.send(username.encode())

        welcome_message = client_socket.recv(1024).decode()
        print(f"[server]: {welcome_message}")

        print("Use '/quit' to exit the chat room,\n\
'/boardcast' to broadcast a message,\n\
'/unicast [username]' (no square bracket) to send a message to [username],\n\
'/file' to request shared folder,\n\
'/download [filename]' to download a file.")

        # Start threads for input handling and receiving messages
        threading.Thread(target=handle_send, args=(client_socket,), daemon=True).start()
        threading.Thread(target=handle_receive, args=(client_socket,), daemon=True).start()

        while True:
            pass  # Keep main thread alive to allow background threads to run

    except KeyboardInterrupt:
        print("Client terminated.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        client_socket.close()

def handle_send(client_socket):
    try:
        while True:
            message = input("")
            if message.lower() == "/quit":
                print("Exiting...")
                client_socket.send(message.encode())
                client_socket.close()
                break
            client_socket.send(message.encode())
    except Exception as e:
        print(f"Error sending message: {e}")

def handle_receive(client_socket):
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                print("Server closed the connection.")
                client_socket.close()
                break
            if message.startswith("Download_File"):
                receive_file(client_socket, message)
            else:
                print(message)
    except Exception as e:
        print(f"Error receiving message: {e}")

def receive_file(client_socket, message):
    try:
        username = message.split(" ", 4)[1]
        filename = message.split(" ", 4)[2]
        size = int(message.split(" ", 4)[3])
        print(f"Preparing to download {filename} ({size} bytes).")

        if not os.path.exists(username):
            os.makedirs(username)
        file_path = os.path.join(username, filename)

        with open(file_path, "wb") as f:
            total_received = 0
            while total_received < size:
                chunk = client_socket.recv(min(1024, size - total_received))
                if not chunk:
                    break
                f.write(chunk)
                total_received += len(chunk)
        print(f"Downloaded {filename} successfully to {file_path}.")

    except Exception as e:
        print(f"Error during file download: {e}")

if __name__ == "__main__":
    client_start()
