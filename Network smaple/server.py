import socket

def start_server():
    serverPort = 8800
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    serverSocket.bind(("", serverPort))
    print("The server is ready to receive")
    while True: 
        message, clientAddress = serverSocket.recvfrom(1024)
        modifiedMessage = message.decode().upper() 
        serverSocket.sendto(modifiedMessage.encode(), clientAddress)

if __name__=="__main__":
    start_server()

