import socket
from U1.chatlib import *

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5678


def build_and_send_message(conn, code, data):
    full_msg = build_message(code, data)
    print("Sending:", full_msg)
    conn.sendall(full_msg.encode())


def recv_message_and_parse(conn):
    try:
        full_msg = conn.recv(2048).decode()
        return parse_message(full_msg)
    except Exception:
        return None, None


def connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))
    return sock


def login(conn):
    while True:
        username = input("Username: ")
        password = input("Password: ")
        build_and_send_message(
            conn,
            PROTOCOL_CLIENT["login_msg"],
            f"{username}#{password}"
        )
        cmd, _ = recv_message_and_parse(conn)
        if cmd == PROTOCOL_SERVER["login_ok_msg"]:
            print("Login successful")
            return
        print("Login failed")


def get_score(conn):
    build_and_send_message(conn, PROTOCOL_CLIENT["get_score_msg"], "")
    _, data = recv_message_and_parse(conn)
    print("Score:", data)


def get_highscore(conn):
    build_and_send_message(conn, PROTOCOL_CLIENT["get_highscore_msg"], "")
    _, data = recv_message_and_parse(conn)
    print("Highscores:")
    print(data.replace("#", "\n"))


def play_question(conn):
    build_and_send_message(conn, PROTOCOL_CLIENT["get_question_msg"], "")
    _, question = recv_message_and_parse(conn)

    parts = question.split("#")
    print(parts[0])
    for i in range(1, 5):
        print(f"{i}. {parts[i]}")

    answer = input("Your answer [1-4]: ")
    build_and_send_message(conn, PROTOCOL_CLIENT["get_answer_msg"], answer)

    _, result = recv_message_and_parse(conn)
    if result == "correct":
        print("Correct!")
    else:
        print("Wrong! Correct answer:", result.split("#")[1])

    get_score(conn)


def get_logged_users(conn):
    build_and_send_message(conn, PROTOCOL_CLIENT["logged_msg"], "")
    _, data = recv_message_and_parse(conn)
    print("Logged users:")
    print(data.replace("#", "\n"))


def logout(conn):
    build_and_send_message(conn, PROTOCOL_CLIENT["logout_msg"], "")
    conn.close()


def main():
    conn = connect()
    login(conn)

    while True:
        print("\n1.Score  2.Highscore  3.Play  4.Users  5.Logout")
        choice = input("Choose: ")

        if choice == "1":
            get_score(conn)
        elif choice == "2":
            get_highscore(conn)
        elif choice == "3":
            play_question(conn)
        elif choice == "4":
            get_logged_users(conn)
        elif choice == "5":
            logout(conn)
            break


if __name__ == "__main__":
    main()
