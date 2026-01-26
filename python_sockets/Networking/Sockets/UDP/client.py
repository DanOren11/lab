import socket

SERVER_IP = "127.0.0.1"
PORT = 8821
MAX_MSG_LENGTH = 1024
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    message = input("Enter message (or EXIT to quit): ")
    my_socket.sendto(message.encode(), (SERVER_IP, PORT))
    if message == "EXIT":
        print("EXIT sent. Closing client.")
        break
    response, address = my_socket.recvfrom(MAX_MSG_LENGTH)
    print("Server replied:", response.decode())

my_socket.close()
