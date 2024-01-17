import socket
import threading
import datetime
import os

ENCODEING = 'utf-8'

nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 38120))

stop_thread = False
EXIT = False

def receive():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode(ENCODEING)
            if message == 'NICK':
                client.send(nickname.encode(ENCODEING))
            else:
                print(message)
        except:
            print("An error occured!")
            client.close()
            break

def write():
    while True:
        if stop_thread:
            break
        msg = input("> ")
        if msg == '/clear' or msg == '/c':
            if os.name == "posix":
                os.system('clear')
            elif os.name in ("nt", "dos", "ce"):
                os.system('CLS')
            else:
                print('\n' * 100)
        elif msg == '/online' or msg == '/o':
            client.send('ONLINE'.encode(ENCODEING))
        else:
            message = f'[{datetime.datetime.now().strftime("%Y-%m-%d %X")}] {nickname}: {msg}'
            client.send(message.encode(ENCODEING))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
