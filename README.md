# Network-coursework

## Usage Instructions

### 1. Running the Server
To start the server:
```bash
python server.py [port]
```
- **port**: The port number the server will listen on (default is `12300`).

### 2. Running the Client
To start the client and connect to the server:
```bash
python client.py <username> <server_ip> <port>
```
- `<username>`: The username of the client (set during execution).
- `<server_ip>`: The IP address of the server.
- `<port>`: The port number the server is listening on (same as the server-side port).

### 3. Client Commands
Once connected, the client can use the following commands to interact with the server and other clients:

- `/quit`: Exit the chat room and disconnect from the server.
- `/broadcast <message>`: Broadcast a message to all connected clients.
- `/unicast <username> <message>`: Send a private message to a specific user.
- `/file`: Request the list of shared files available on the server.
- `/download <filename>`: Download a shared file to the local machine.

### 4. Shared Files and Download
- The server-side files are stored in a shared directory (environment variable `SERVER_SHARED_FILES`).
- The client can use the `/file` command to view the list of shared files and `/download <filename>` to download files.
- Downloaded files are saved in a folder named after the current username, with the same filename as the shared file.

### 5. Error and Exception Handling
- If the server disconnects, the client will automatically close.
- If the client fails to connect to the server, an error message will be displayed.
- Errors during communication between client and server are caught, and the connection is closed gracefully.

---

## Implementation Details

### 1. Server & Client Connection
**Requirement**: When a client connects, the server prints the connection details (IP and port), and the client receives a welcome message.

- **Server Side (server.py)**:
  - The server listens on a specified port and accepts incoming connections. It prints the IP and port of each client upon connection:
    ```python
    print(f"New client with IP: {address[0]} and Port: {address[1]}")
    ```
  - Each client connection is handled in a new thread:
    ```python
    threading.Thread(target=handle_client, args=(client_socket,)).start()
    ```

- **Client Side (client.py)**:
  - The client sends its username to the server and receives a welcome message:
    ```python
    welcome_message = f"Welcome {username} to the server".encode()
    client_socket.send(welcome_message)
    ```

### 2. Broadcasting & Unicasting Messages
**Requirement**: Clients can broadcast messages to all other clients or send private messages to specific clients.

- **Server Side (server.py)**:
  - **Broadcasting**:
    ```python
    def broadcast_message(message, sender_socket):
        for client in clients:
            if client != sender_socket:
                try:
                    client.send(message.encode())
                except Exception as e:
                    print(f"Error sending message to client: {e}")
    ```
  - **Unicasting**:
    ```python
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
    ```

### 3. Client Disconnecting & Server Handling
**Requirement**: If a client leaves (via `/quit` or unexpectedly), a message is broadcast to other clients.

- **Server Side (server.py)**:
  - The server removes the client from the list and broadcasts a disconnect message:
    ```python
    def remove_client(client_socket):
        if client_socket in clients:
            username = clients[client_socket]
            print(f"Client {username} has disconnected.")
            broadcast_message(f"[{username}] has left the chat.", client_socket)
            del clients[client_socket]
            client_socket.close()
    ```

### 4. File Sharing
**Requirement**: The server provides a "SharedFiles" folder. Clients can request access, view available files, and download them.

- **Server Side (server.py)**:
  - Listing shared files:
    ```python
    def access_files():
        if not os.path.exists(shared_files):
            return "No shared files"
        else:
            files = os.listdir(shared_files)
            return files, len(files)
    ```
  - Sending a file:
    ```python
    def download(client_socket, filename):
        try:
            path = os.path.join(shared_files, filename)
            with open(path, "rb") as file:
                while chunk := file.read(1024):
                    client_socket.send(chunk)
            print(f"File {filename} sent successfully.")
        except Exception as e:
            print(f"Error sending file {filename}: {e}")
    ```

- **Client Side (client.py)**:
  - Viewing files with `/file`:
    The server sends the list of files and their count.
  - Downloading files with `/download`:
    The client receives the file in chunks and saves it locally in a directory named after the username.

### 5. Error & Exception Handling
**Requirement**: Handle errors gracefully to prevent crashes.

- **Server Side (server.py)**:
  - Catch errors during communication and remove disconnected clients:
    ```python
    except Exception as e:
        print(f"Error handling client {clients.get(client_socket, 'unknown')}: {e}")
    finally:
        remove_client(client_socket)
    ```
  - Release resources when the server terminates:
    ```python
    finally:
        server_socket.close()
    ```

**Requirement**: Prevent clients from connecting without setting a username.
- **Client Side (client.py)**:
  - Check command-line arguments:
    ```python
    if len(sys.argv) < 4:
        print("Error: Missing arguments.\n"
              "Usage: python client.py [username] [server_ip] [port]")
        return
    ```

**Requirement**: Display errors if the server is unavailable or connection details are incorrect.
- Use try-except to handle connection errors:
    ```python
    try:
        client_socket.connect((ip, port))
    except socket.gaierror:
        print(f"Error: Invalid server IP or hostname: {ip}")
        return
    ```

