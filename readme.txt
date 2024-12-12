# Network and System Coursework- README

## Usage Instructions

### 1. Running the Server
To start the server:
    python server.py [port]

- port: The port number the server will listen on (This can be set depending on when the command is entered, but the default is ’12300‘).


### 2. Running the Client
To start the client and connect to the server:
    python client.py <username> <server_ip> <port>

- `<username>`: The username of the client. (username will be set when run the client.py)
- `<hostname>`: The IP address of the server.
- `<port>`: The port number the server is listening on (same as the server-side port).


### 3. Client Commands
Once connected, the client can use the following commands to interact with the server and other clients: (There are tips on the client)

- `/quit`: Exit the chat room and disconnect from the server.
- `/boardcast <message>`: Broadcast a message to all connected clients.
- `/unicast <username> <message>`: Send a private message to a specific user.
- `/file`: Request the list of shared files available on the server.
- `/download <filename>`: Download a shared file to the local machine.


### 4. Shared Files and Download
- The server-side files are made available through a shared directory (environment variable SERVER_SHARED_FILES). 
- The client can use the /file command to view the list of shared files and use the /download <filename> command to download the files locally. 
- The downloaded files are saved in a folder named with the current user name, 
- and the file name is the same as the file name of the shared file on the server side.


### 5. Error and Exception Handling
- If the server disconnects, the client will automatically close.
- If the client fails to connect to the server, an error message will be displayed.
- If any errors occur during communication between the client and server, they will be caught, and the connection will be closed.

How to achieve:

### 1. Server & Client Connection
**Requirement**: When a client connects, the server should print the connection details (IP and port), and the client should receive a welcome message.

- **Server Side (server.py)**:
  - The server listens on a specified port and accepts incoming connections. It prints the IP and port of each client upon connection using 
        `print(f"New client with ip: {address[0]} and Port: {address[1]}")`.
  - Once a client connects, the server creates a new thread to handle that client's interactions using `threading.
        Thread(target=handle_client, args=(client_socket,))`.

- **Client Side (client.py)**:
    - The client will get and send the username from the command to the server, and will then receive a welcome message from the server. 
    The welcome message will be sent back to the client via `client_socket.send(welcome_message)`.        
        `welcome_message = f"Welcome {username} to server".encode()` in the `handle_client` function. 

### 2. Broadcasting & Unicasting Messages
**Requirement**: Clients should be able to broadcast messages to all other clients or send private messages (unicast) to specific clients.

- **Server Side (server.py)**:
    - Broadcast**: The function `boardcast_message(message, sender_socket)` sends a message to all connected clients except the sender.
    Finds all clients except the sender by looping through them and sends the message one by one.
        for client in clients:
            if client != sender_socket:
                try:
                    client.send(message.encode())
                except Exception as e:
                    print(f"Error sending message to client: {e}")

    - **Unicasting**: The function `send_private_message(receiver, message, sender_socket)` sends a message to a specific client identified by their username. 
    The function loops through the `clients` dictionary and finds the appropriate user by the supplied username to find the target client socket. 
    To send a specific message to a specific client via the target client socket
            def send_private_message(receiver, message, sender_socket):
                for client in clients:
                    if clients[client] == receiver:
                        try:
                            client.send(message.encode())
                            return
                        except Exception as e:
                            print(f"Error sending private message: {e}")
                            return
                sender_socket.send("User not found.".encode())

### 3. Client Disconnecting & Server Handling
**Requirement**: If a client leaves (either via the `/quit` command or unexpectedly), a message should be broadcast to other clients indicating that the client has left.

- **Server Side (server.py)**:
    - When a client disconnects, the server calls `remove_client(client_socket)`, which removes the client from the `clients` dictionary, 
    closes the corresponding socket and sends a message to the other clients indicating that the client has left.    
        def remove_client(client_socket):
            if client_socket in clients:
                username = clients[client_socket]
                print(f"Client {username} has disconnected.")
                boardcast_message(f"[{username}] has left the chat.", client_socket)
                del clients[client_socket]
                client_socket.close()

### 4. File Sharing
**Requirement**: The server should have a "SharedFiles" folder. Clients should be able to request access to this folder, view the list of available files, and download them.

- **Server Side (server.py)**:
    - The `access_files()` function checks if the "SharedFiles" folder exists and returns a list of available files along with their count. The server sends this information back to the client.
        def access_files():
            if not os.path.exists(shared_files):
                return "No shared files"
            else:
                files = os.listdir(shared_files)
                return files, len(files)
  
    - When a client requests to download a file, the server checks if the file exists in the "SharedFiles" folder and sends the file size and content to the client.
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
    

- **Client Side (client.py)**:
    - Clients can use the `/file` command to request access to the shared files, which will trigger the server to send the list of files and their count.
    - Clients can download files using the `/download` command. The client will receive the file in chunks and save it to a directory named after the username.
        def receive_file(client_socket, message):
            try:
                username = message.split(" ", 4)[1]  
                filename = message.split(" ", 4)[2] 
                ...

### 5. Error & Exception Handling
**Requirement**: Handle any errors, ensuring that the server does not crash if a client disconnects unexpectedly and that appropriate error messages are displayed.

- **Server Side (server.py)**:
    - Exception handling is implemented in multiple places to catch errors, such as client disconnections or file-related errors. 
    If an error occurs, the server deletes the client's letter in clients, closes the client in question and prints a message and continues to run.        
        except Exception as e:
            print(f"Error handling client {clients.get(client_socket, 'unknown')}: {e}")
        finally:
            remove_client(client_socket)

    - Additionally, when the server terminates, the socket is closed properly to release resources:
        finally:
            server_socket.close()

**Requirement**: The server should not allow any client to transmit messages without having first set a username.
- **Client Side (client.py)**:
    -Before the client creates a socket, the command is checked for compliance, and if any of the parameters are missing, an error is reported.(sys.argv[1] is mandatory to become username)
        if len(sys.argv) < 4:
                print("Error: Missing arguments.\n"
                    "Usage: python client.py [username] [server_ip] [port]")
                return

**Requirement**: If the server is not available or port/hostname are wrong, an error message detailing the issue should be printed.
    - Use the try-except statement to catch errors that occur during the connection process and print detailed error messages.
        try:
            client_socket.connect((ip, port))
        except socket.gaierror:
            print(f"Error: Invalid server IP or hostname: {ip}")
            return
