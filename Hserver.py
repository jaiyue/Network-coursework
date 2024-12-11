import socket
import sys
import select
import os

clients = {}
shared_files = os.getenv("SERVER_SHARED_FILES")

def server_start():
    try:
    #create socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = int(sys.argv[1]) if len(sys.argv) > 1 else 12300
        server_socket.bind(('localhost', port))
        print(f"Server is ready to receive on port {port}")
        server_socket.listen(5)
        server_socket.setblocking(0)  #set the socket to non-blocking mode

        connected_clients = [server_socket]
        while True:
            readable, writable, exceptional = select.select(connected_clients, [], connected_clients)
            
            for s in readable:
            #new client connection
                if s is server_socket:
                    client_socket, address = server_socket.accept()#accepts the connection
                    print(f"New client with ip: {address[0]} and Port: {address[1]}")

                    username = client_socket.recv(1024).decode()  #receive the username
                    connected_clients.append(client_socket)
                    clients[client_socket] = username
                    print(f"New client connected with username: {username}")

                    welcome_message = f"Welcome {username} to server {port}".encode()
                    client_socket.send(welcome_message)
                    boardcast_message(f"[{username}] has joined", client_socket)

                else:  #existing client
                    try:
                        data = s.recv(1024).decode()
                        if not data:  # 如果没有接收到数据，客户端已关闭连接
                            print(f"Client {clients[s]} disconnected unexpectedly.")
                            remove_client(s, connected_clients, server_socket)
                            
                        elif data.lower() == "/quit":  #exit server
                            remove_client(s, connected_clients, server_socket)
                            
                        elif data.lower() == "/file":  #access shared files
                            li, count = access_files()
                            s.send(f"{count} file(s) available: {li}".encode())
                            
                        elif data.startswith("/download"):  #download a file
                            filename = data.split(" ", 1)[1]
                            files = os.listdir(shared_files)
                            size = os.path.getsize(os.path.join(shared_files, filename))
                            username = clients[s]
                            if filename in files:
                                s.send(f"Download_File {username} {filename} {size} ".encode())
                                download(s, filename)
                            else:
                                s.send(f"File {filename} not found".encode())
                                
                        elif data.startswith("/boardcast"): #boardcast message to all users
                            username = clients[s]
                            message = f"[{username}]:" + data.split(" ", 1)[1]
                            boardcast_message(message, s)
                            print(f"Message broadcasted: {message}")
                            s.send("Message has been broadcasted.".encode())
                            
                        elif data.startswith("/unicast"):   #send private message to a user
                            sender = clients[s]
                            receiver = data.split(" ", 2)[1]
                            message = f"[{sender}]:" + data.split(" ", 2)[2]
                            check = 0
                            for client in clients:
                                if clients[client] == receiver:
                                    client.send(message.encode())
                                    check = 1
                                    break
                            if check == 0:
                                s.send("User not found".encode())
                                
                    except Exception as e:
                        print(f"Error processing data from {clients[s]}: {e}")
                        remove_client(s, connected_clients, server_socket)

            # error
            for s in exceptional:
                print(f"Exception on socket {s}. Closing connection.")
                remove_client(s, connected_clients, server_socket)

    except KeyboardInterrupt:
        print("Server terminated.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        server_socket.close()

def boardcast_message(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except Exception as e:
                print(f"Error sending message to client: {e}")

def remove_client(client_socket, connected_clients, server_socket):
    if client_socket in clients:
        username = clients[client_socket]
        print(f"Client {username} has disconnected.")
        boardcast_message(f"[{username}] has left", client_socket)
        client_socket.send("You have been disconnected from the server".encode())
        connected_clients.remove(client_socket)
        del clients[client_socket]
        client_socket.close()

def access_files():
    if not os.path.exists(shared_files):
        return "No shared files", 0
    else:
        count = len(os.listdir(shared_files))
        return os.listdir(shared_files), count

def download(s, filename):
    try:
        path = os.path.join(shared_files, filename)
        with open(path, "rb") as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                s.send(data)
        print(f"File {filename} sent successfully.")
    except Exception as e:
        print(f"Error sending file {filename}: {e}")

if __name__ == "__main__":
    server_start()
