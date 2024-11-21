import socket

def client_start():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 12345
    client_socket.connect(('localhost',port))
    print("Connect successfully")
    welcome_message = client_socket.recv(1024).decode()
    print(f"message from server: {welcome_message}")
    client_socket.close()

if __name__ == "__main__":
    client_start()