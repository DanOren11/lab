import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 8008))

data = ''
while data != 'Bye':
    mg = input("Enter a message: ")
    sock.send(mg.encode())
    data = sock.recv(1024).decode()
    print("The server sent: " + data)

sock.close()
