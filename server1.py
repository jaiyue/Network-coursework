import socket

def server_start():
    # 创建一个 TCP 套接字
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    port = 12345
    s.bind(('localhost', port))  # 绑定到指定的地址和端口
    s.listen(5)  # 监听连接
    print(f"The server is ready to receive, port number: {port}")
    
    while True:
        client_socket, client_address = s.accept()  # 接受客户端连接
        print(f"New client {client_address[0]} with IP: {client_address[0]} and port: {client_address[1]}")
        
        # 发送欢迎消息
        welcome_message = f"Welcome to the server on port {port}".encode()
        client_socket.send(welcome_message)
        
        # 关闭与当前客户端的连接
        client_socket.close()

if __name__ == "__main__":
    server_start()
