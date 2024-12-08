import socket
import sys
import select

def client_start():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 12300
    client_socket.connect(('localhost',port))
    
    username = sys.argv[1]
    ip = sys.argv[2]
    print("Connect successfully", username, ip)
    client_socket.send(username.encode())
    
    welcome_message = client_socket.recv(1024).decode()
    print(f"message from server: {welcome_message}")

    while True:
        r,w,e = select.select([client_socket, sys.stdin], [], [])
        for s in r:
            if s == client_socket:
                message = client_socket.recv(1024).decode()
                print(f"message from server: {message}")
            else:
                message = input("Enter message: ")
                client_socket.send(message.encode())
                
                
                
if __name__ == "__main__":
    client_start()