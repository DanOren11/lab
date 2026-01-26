import socket
from fileinput import close

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(('0.0.0.0', 8888))
sock.listen()
print("Server is listening")
(socket_client, client_address) = sock.accept()
print("Client is listening")

while True:
    data = socket_client.recv(1024).decode()
    print("Client sent : " + data)
    if data == 'Quit':
        print("Closing client socket now ....")
        socket_client.send("Bye".encode())
        break
    client_data = (data + "!!!!!!").upper()
    socket_client.send(client_data.encode())

sock.close()
socket_client.close()
