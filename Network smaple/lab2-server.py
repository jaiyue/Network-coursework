import socket

class User:
    client_id = 0
    max_uses = 0
    times_used = 0
    def __init__(self, client_id, max_uses):
        self.client_id = client_id
        self.max_uses = max_uses

users = {}

def add_user(client_id, max_uses):
    users[client_id] = User(client_id, max_uses)

[add_user(x[0], x[1]) for x in [(100000, 3),(200000, 1), (300000, 4)]]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

CHUNK_LENGTH = 2048
ID_LENGTH = 6

server_address = ('', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
sock.listen()

def handle_connection(connection, client_address):
    try:
        print('connection from', client_address)
        message = ''
        try:
            client_id = int(connection.recv(ID_LENGTH).decode('UTF-8'))
        except ValueError:
            print ('Client did not send a numeric 6 digit client id')
            return
        if client_id not in users:
            print ('Attempted connection from unknown client id {}'.format(client_id))
            return
        user = users[client_id]
        if user.times_used >= user.max_uses:
            print ('User {} attempted to use this service too many times'.format(client_id))
            return
        user.times_used = user.times_used + 1
        while True:
            data = connection.recv(CHUNK_LENGTH)
            if len(data) == 0:
                print(message)
                return
            message = message + data.decode('UTF-8')
    finally:
        connection.close()

while True:
    print ('waiting for a connection')
    connection, client_address = sock.accept()
    handle_connection(connection, client_address)
    

