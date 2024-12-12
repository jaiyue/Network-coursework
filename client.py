import socket
import sys
import threading
import os

def client_start():
    client_socket = None  
    try:
        if len(sys.argv) < 4:
            print("Error: Missing arguments.\n"
                "Usage: python client.py [username] [server_ip] [port]")
            return
        username = sys.argv[1]  # Get the username
        ip = sys.argv[2]  # Get the server IP address
        port = int(sys.argv[3])  # Get the server port

        # Create the client socket and connect to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((ip, port))
        except socket.gaierror:
            print(f"Error: Invalid server IP or hostname: {ip}")
            return
        print(f"Connected successfully as {username} to {ip}:{port}")
        client_socket.send(username.encode())  # Send the username to the server

        welcome_message = client_socket.recv(1024).decode()  # Receive welcome message from server
        print(f"[server]: {welcome_message}")
        print("Use '/quit' to exit the chat room,\n"
        "'/boardcast' to broadcast a message,\n"
        "'/unicast [username]' (no square bracket) to send a message to [username],\n"
        "'/file' to request shared folder,\n"
        "'/download [filename]' to download a file.\n"
        )
        # Use a separate thread to handle receiving messages
        receive_thread = threading.Thread(target=handle_receive, args=(client_socket,), daemon=True)
        receive_thread.start()

        # Main thread handles sending messages
        while True:
            user_input = input( "Enter your command: ")  # Prompt the user for input
            
            if user_input.lower() == "/quit":  # If user types "/quit", exit the program
                print("Exiting...")
                client_socket.send(user_input.encode()) 
                client_socket.close()
                break
            else:
                client_socket.send(user_input.encode())  # Send user input to the server

    except KeyboardInterrupt:
        print("\nClient terminated.")  
    except Exception as e:
        print(f"Unexpected error: {e}") 
    finally:
        try:
            client_socket.close()  
        except Exception:
            pass

def handle_receive(client_socket):
    try:
        while True:
            message = client_socket.recv(1024).decode()  # Receive message from server
            if not message:
                print("Server closed the connection.")  
                break
            if message.startswith("Download_File"):  
                receive_file(client_socket, message)  
            else:
                print(message) 
    except Exception as e:
        print(f"Error receiving message: {e}") 
    finally:
        try:
            client_socket.close()  
        except Exception:
            pass

def receive_file(client_socket, message):
    try:
        username = message.split(" ", 4)[1]  
        filename = message.split(" ", 4)[2] 
        size = int(message.split(" ", 4)[3])  
        print(f"Preparing to download {filename} ({size} bytes).")

        if not os.path.exists(username):  # Create a directory for the username if it doesn't exist
            os.makedirs(username)
        file_path = os.path.join(username, filename)  # Set the file path to save the file

        # Open the file and receive data in chunks
        with open(file_path, "wb") as f:
            total_received = 0
            while total_received < size:
                chunk = client_socket.recv(min(1024, size - total_received))  # Receive data in chunks
                if not chunk:
                    break
                f.write(chunk)
                total_received += len(chunk)
        print(f"Downloaded {filename} successfully to {file_path}.")  # Confirmation of successful download

    except Exception as e:
        print(f"Error during file download: {e}")  # Handle errors during file download

if __name__ == "__main__": 
    client_start() 
