import socket
import select

MAX_MSG_LENGTH = 1024
SERVER_PORT = 5001
SERVER_IP = "0.0.0.0"


def print_client_sockets(client_sockets):
     for c in client_sockets:
         print("\t", c.getpeername())
def main():
    print("Settings up server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    print("Waiting for connections...")
    client_sockets = []
    while True:
        ready_to_read, ready_to_write, in_error = select.select([server_socket] + client_sockets, [], [])
        for client_socket in ready_to_read:
            if client_socket == server_socket:
                (client_socket, client_address) = server_socket.accept()
                print("New client joined!", client_address)
                client_sockets.append(client_socket)
            else:
                print("New data arrived!")
                data = client_socket.recv(MAX_MSG_LENGTH).decode()
                if data == "":
                    print("Client disconnected!")
                    client_sockets.remove(client_socket)
                    client_socket.close()
                else:
                    print(data)
                    client_socket.send(data.encode())


main()
