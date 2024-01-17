import threading
import socket
import random

ENCODING = 'utf-8'
LOGGING = True
host = '0.0.0.0'# localhost
port = 38120

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if message.decode(ENCODING) == "ONLINE":
                client.send('\n###Online###'.encode(ENCODING))
                for nickname_send in nicknames:
                    client.send(f'{nickname_send}\n'.encode(ENCODING))
            elif LOGGING:
                with open("log.log", "a") as log:
                    log.write(message.decode(ENCODING) + "\n")
                broadcast(message)

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        client.send('NICK'.encode(ENCODING))

        nickname = client.recv(1024).decode(ENCODING)

        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}!')

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()



print("Server is listening...")
receive()
