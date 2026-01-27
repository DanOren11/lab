import datetime
import random
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 8008))
sock.listen()
print("Server is listening !")
(client_socket, client_address) = sock.accept()
print("Client is listening !")

while True:
    data = client_socket.recv(1024).decode()
    client_data = data
    if data == 'Quit':
        print("Closing client socket now ....")
        client_socket.send("Bye".encode())
        break
    if data == 'name':
        client_data = "I dont have one"
    if data == 'time':
        time = str(datetime.datetime.now())
        client_data = "Time: " + time
    if data == 'rand':
        client_data = str(random.randint(1, 10))

    client_socket.send(client_data.encode())

client_socket.close()
sock.close()
