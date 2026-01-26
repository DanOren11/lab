import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1', 5001)
sock.connect(server_address)
while True:
    input("Enter a message")
    print("Sending message")

sock.close()
