import socket
import select

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
            #new client connected
            if s is server_socket:
                client_socket,address = server_socket.accept() #accepts the connection
                print(f"New client with ip: {address[0]} and port{address[1]} and {client_socket}")
                             
                username = client_socket.recv(1024).decode() #receive the username
                connected_clients.append(client_socket) 
                clients[client_socket] = username
                print(f"New client connected with username: {username}")
                
                welcome_message = f"welcome {username} to server {port}".encode()
                client_socket.send(welcome_message)
                boardcast_message(f"{username} has joined", server_socket)
            '''    
            else:
                data = input.recv(1024)
                if data: #vaild message 未完成
                    print(f"Message {data} from {s.getpeername()}")
                    
                else:
                    print('closing', address)
'''

def boardcast_message(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                print("Error sending message to client.")


def remove_client(client_socket, connected_clients, server_socket):
    if client_socket in clients:
        username = clients[client_socket]
        print(f"Client {username} has disconnected")
        client_socket.close()
        connected_clients.remove(client_socket)
        del clients[client_socket]
        boardcast_message(f"{username} has left", server_socket)


if __name__ == "__main__":
    server_start()
        
        
        