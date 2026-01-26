import socket

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to localhost on port 8820
server_socket.bind(('127.0.0.1', 8820))

# Listen for incoming connections
server_socket.listen(1)
print("Server is listening on 127.0.0.1:8820")

while True:
    # Wait for a client to connect
    client_socket, client_address = server_socket.accept()
    print("Connected to:", client_address)

    # Receive data from the client
    data = client_socket.recv(1024).decode()
    print("Client sent:", data)

    # Send a response back to the client
    client_socket.send("hello from server".encode())

    # Close connection
    client_socket.close()
