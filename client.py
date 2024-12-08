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
    print(f"[server]: {welcome_message}")

    print("Use '/quit' to exit the chat room,\n\
'/boardcast' to boardcast message,\n\
'/unicast [username]' (no square bracket) to send message to [username],\n\
'/files' to to request shared folder.")
    client_socket.setblocking(0)

    while True:
        r,w,e = select.select([client_socket, sys.stdin], [], [])
        for s in r:
            if s == sys.stdin:
                message = input("")
                client_socket.send(message.encode())
                if message.lower() == "/quit":
                    print("Exit...")
                    client_socket.close()
                    return
                
            else:
                message = client_socket.recv(1024).decode()
                print(f"{message}")
                
                
                
if __name__ == "__main__":
    client_start()