import socket
import sys
import select
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
        client_socket.setblocking(0)

        while True:
            r, w, e = select.select([client_socket, sys.stdin], [], [])
            for s in r:
                if s == sys.stdin:
                    message = input("")
                    try:
                        client_socket.send(message.encode())
                        if message.lower() == "/quit":
                            print("Exiting...")
                            client_socket.close()
                            return
                    except (BrokenPipeError, ConnectionResetError):
                        print("Error: Connection to server lost.")
                        return
                else:
                    try:
                        message = client_socket.recv(1024).decode()
                        if not message:
                            print("Server closed the connection.")
                            client_socket.close()
                            return
                        if message.startswith("Download_File"):
                            receive_file(client_socket, message)
                        else:
                            print(message)
                    except (BlockingIOError, ConnectionResetError) as e:
                        print(f"Error: {e}")
                        return
            for s in e:
                if s == client_socket:
                    print("Error: Connection to server lost or connection reset.")
                    client_socket.close()
                    return
                
    except KeyboardInterrupt:
        print("Client terminated.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        client_socket.close()

def receive_file(client_socket, message):
    try:
        username  =  message.split(" ",4)[1]
        filename = message.split(" ",4)[2]
        size = int(message.split(" ",4)[3])
        print(f"Preparing to download {filename} ({size} bytes).")

        if not os.path.exists(username):
            os.makedirs(username)
        file_path = os.path.join(username, filename)

        client_socket.setblocking(1)
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
    finally:
        client_socket.setblocking(0)

if __name__ == "__main__":
    client_start()