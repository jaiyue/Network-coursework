import socket

def server_start():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 12345
    server_socket.bind(('localhost',port))
    print(f"The server is ready to receive,portnumber:{port}")
    server_socket.listen(5)
    while True:
        c,address = server_socket.accept()
        print(f"New client with ip: {address[0]} and port{address[1]}")
        welcome_message = f"welcome to server {port}".encode()
        c.send(welcome_message)
        server_socket.close()

if __name__ == "__main__":
    server_start()
        
        
        