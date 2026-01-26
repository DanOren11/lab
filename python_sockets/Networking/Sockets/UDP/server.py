import socket

SERVER_IP = "0.0.0.0"
PORT = 8821
MAX_MSG_LENGTH = 1024

my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.bind((SERVER_IP, PORT))
while True:
    (client_message, my_address) = my_socket.recvfrom(MAX_MSG_LENGTH)
    data = client_message.decode()
    print("Client sent: " + data)
    if data == "quit":
        print("EXIT received. Server shutting down.")
        break
    response = "Super" + data
    my_socket.sendto(response.encode(), (SERVER_IP, my_address))
my_socket.close()
