import socket

def start_client():
    serverName = ""
    serverPort = 8800
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    message = input("Input lowercase sentence: ")

    clientSocket.sendto(message.encode(), (serverName, serverPort))
    modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
    print(modifiedMessage.decode())
    clientSocket.close()

if __name__ == "__main__":
    start_client()
