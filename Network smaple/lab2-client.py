import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)

print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)
client_id = sys.argv[1]
message = sys.argv[2]
print('client id is {}'.format(client_id))
print ('sending {}'.format(message))
try:
    sock.sendall(client_id.encode('UTF-8'))
    sock.sendall(message.encode('UTF-8'))
finally:
    sock.close()