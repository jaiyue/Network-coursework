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
    Server.py：
    - The server creates a socket, binds it to the specified port and ip, and listens for incoming connections.
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            port = int(sys.argv[1]) if len(sys.argv) > 1 else 12300
            server_socket.bind(('localhost', port))
            print(f"Server is ready to receive on port {port}")
            server_socket.listen(5)
    
    - The server uses the threading module to implement multithreading, with the main thread focusing on listening for new connections and 
    receiving requests from clients via the socket.accept() method.Once a new connection is made, the main thread creates a separate thread 
    for each client, with each subthread handling all of the individual client interactions,such as receiving messages, sending messages, 
    file requests, and broadcasting messages.This approach allows the sub-threads to run independently without blocking the main thread or 
    affecting the operation of other clients, thus enabling multiple connections to be processed concurrently.
            while True:
                client_socket, address = server_socket.accept()
                print(f"New client with ip: {address[0]} and Port: {address[1]}")
                thread = threading.Thread(target=handle_client, args=(client_socket,))
                thread.start()

    - The handle_client() function is responsible for receiving and processing client requests. It first receives the username 
    from the client and stores it in the clients dictionary. Then it continuously receives messages from the client and performs 
    different actions depending on the content of the message.
            def handle_client(client_socket):
                try:
                    username = client_socket.recv(1024).decode()  # Receive the username
                    clients[client_socket] = username
                    ...

    clinet.py：
    - The client creates a socket, connects to the server, and gets the username from the command to send to the server.
            username = sys.argv[1]
            ip = sys.argv[2]
            port = int(sys.argv[3])

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip, port))
            print(f"Connected successfully as {username} to {ip}:{port}")
            client_socket.send(username.encode())

    - The client uses the threading module to implement multithreading, with the main thread focusing on sending and receiving messages 
    and the subthread handling file requests and downloads. This approach allows the sub-threads to run independently without blocking the main thread or 
    affecting the operation of other clients, thus enabling multiple connections to be processed concurrently.
