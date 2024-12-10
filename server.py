import socket
import select
import os

clients = {}

def server_start():
    #create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 12300
    server_socket.bind(('localhost',port))
    print(f"The server is ready to receive,port number:{port}")
    server_socket.listen(5)
    
    server_socket.setblocking(0) #set the socket to non-blocking mode

    connected_clients = [server_socket]
    while True:
        readable, writable, exceptional = select.select(connected_clients,[],connected_clients)
        for s in readable:
            #new client connection
            if s is server_socket:
                client_socket,address = server_socket.accept() #accepts the connection
                print(f"New client with ip: {address[0]} and port{address[1]}")
                             
                username = client_socket.recv(1024).decode() #receive the username
                connected_clients.append(client_socket) 
                clients[client_socket] = username
                print(f"New client connected with username: {username}")
                
                welcome_message = f"welcome {username} to server {port}".encode()
                client_socket.send(welcome_message)
                boardcast_message(f"[{username}] has joined", client_socket)
            
            else: #existing client
                data = s.recv(1024).decode()
                if data.lower() == "/quit": #exit server
                    remove_client(s, connected_clients, server_socket)
                
                # elif data.lower() == "/file": #access shared files
                    
                #     print(f"Message {data} from {s.getpeername()}")
                
                elif data.startswith("/boardcast"): #boardcast message to all users
                    username = clients[s]
                    message = f"[{username}]:" + data.split(" ", 1)[1]
                    boardcast_message(message, s)
                    print("Already boardcasted message:",message)
                    s.send("Message has been boardcasted".encode())
                
                elif data.startswith("/unicast"): #send private message to a user
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
                    
                else:
                    print('closing', address)


def boardcast_message(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                print("Error sending message to client.", clients[client])


def remove_client(client_socket, connected_clients, server_socket):
    if client_socket in clients:
        username = clients[client_socket]
        print(f"Client {username} has disconnected")
        boardcast_message(f"[{username}] has left", client_socket)
        client_socket.send("You have been disconnected from the server".encode())
        connected_clients.remove(client_socket)
        del clients[client_socket]



if __name__ == "__main__":
    server_start()
        
        
        