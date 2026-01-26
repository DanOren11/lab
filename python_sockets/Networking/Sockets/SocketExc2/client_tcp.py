import socket

socket_a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_a.connect(('127.0.0.1', 8080))
data = ''
while data != 'Bye':
    mg = input("Enter a message: \n")
    socket_a.send(mg.encode())
    data = socket_a.recv(1024).decode()
    print("The Serer sent " + data)

socket_a.close()
