import threading
import socket

host = '127.0.0.1'  #local host
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

#lists fr clients and their nicknames
clients = []
nicknames = []

#sending message to the connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

#handling messages from client side
def handle(client):
    while True:
        try:
            #broadcasting messages
            message = client.recv(1024)
            broadcast(message)

        except:
            #removing and closing clients
            index = client.index(client)
            clients.remove(client)
            client.close()
            #as we are removing the client so we also have to remove their nickname as they both have same index in their list
            nickname = nicknames[index]

            #broadcasting the client's name, as they left the convo/chat
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break

#recieving and listening function
def receive():
    while True:
        #accepting connection request
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        #asking nickname from client 
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the cleint is {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is listening...")
receive()

