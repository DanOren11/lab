##############################################################################
# server.py
##############################################################################

import socket
from U1.chatlib import *

# GLOBALS
users = {}
questions = {}
logged_users = {}  # addr -> username

ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"


# ================= HELPER SOCKET METHODS =================

def build_and_send_message(conn, code, msg):
    full_msg = build_message(code, msg)
    print("[SERVER]", full_msg)
    conn.sendall(full_msg.encode())


def recv_message_and_parse(conn):
    try:
        full_msg = conn.recv(2048).decode()
        if full_msg == "":
            return None, None
        print("[CLIENT]", full_msg)
        cmd, data = parse_message(full_msg)
        return cmd, data
    except Exception:
        return None, None


# ================= DATA LOADERS =================

def load_questions():
    return {
        2313: {
            "question": "How much is 2+2",
            "answers": ["3", "4", "2", "1"],
            "correct": 2
        },
        4122: {
            "question": "What is the capital of France?",
            "answers": ["Lion", "Marseille", "Paris", "Montpellier"],
            "correct": 3
        }
    }


def load_user_database():
    return {
        "test": {"password": "test", "score": 0, "questions_asked": []},
        "yossi": {"password": "123", "score": 50, "questions_asked": []},
        "master": {"password": "master", "score": 200, "questions_asked": []}
    }


# ================= SOCKET CREATOR =================

def setup_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    sock.listen()
    print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")
    return sock


def send_error(conn, error_msg):
    build_and_send_message(
        conn,
        PROTOCOL_SERVER["error_msg"],
        error_msg
    )


# ================= MESSAGE HANDLING =================

def handle_logout_message(conn):
    addr = conn.getpeername()
    if addr in logged_users:
        del logged_users[addr]
    conn.close()


def handle_login_message(conn, data):
    global users, logged_users

    try:
        username, password = data.split("#")
    except ValueError:
        send_error(conn, "Bad login format")
        return

    if username not in users:
        send_error(conn, "User does not exist")
        return

    if users[username]["password"] != password:
        send_error(conn, "Wrong password")
        return

    logged_users[conn.getpeername()] = username
    build_and_send_message(
        conn,
        PROTOCOL_SERVER["login_ok_msg"],
        ""
    )
def handle_logged_message(conn):
    usernames = list(logged_users.values())

    build_and_send_message(
        conn,
        PROTOCOL_SERVER["logged_msg"],
        "#".join(usernames)
    )

def handle_getscore_message(conn, username):
    score = str(users[username]["score"])
    build_and_send_message(
        conn,
        PROTOCOL_SERVER["get_score_msg"],
        score
    )

def handle_highscore_message(conn):
    sorted_users = sorted(
        users.items(),
        key=lambda item: item[1]["score"],
        reverse=True
    )

    highscores = [
        f"{username}:{data['score']}"
        for username, data in sorted_users
    ]

    build_and_send_message(
        conn,
        PROTOCOL_SERVER["get_highscore_msg"],
        "#".join(highscores)
    )



def handle_client_message(conn, cmd, data):
    addr = conn.getpeername()
    is_logged = addr in logged_users

    if not is_logged and cmd != PROTOCOL_CLIENT["login_msg"]:
        send_error(conn, "User not logged in")
        return True

    if cmd == PROTOCOL_CLIENT["login_msg"]:
        handle_login_message(conn, data)

    elif cmd == PROTOCOL_CLIENT["logout_msg"]:
        handle_logout_message(conn)
        return False

    elif cmd == PROTOCOL_CLIENT["get_score_msg"]:
        username = logged_users[addr]
        handle_getscore_message(conn, username)

    elif cmd == PROTOCOL_CLIENT["get_highscore_msg"]:
        handle_highscore_message(conn)

    elif cmd == PROTOCOL_CLIENT["logged_msg"]:
        handle_logged_message(conn)

    else:
        send_error(conn, "Unknown command")

    return True

# ================= MAIN =================

def main():
    global users, questions

    print("Welcome to Trivia Server!")

    users = load_user_database()
    questions = load_questions()

    server_socket = setup_socket()

    while True:
        conn, addr = server_socket.accept()
        print("Client connected:", addr)

        connected = True
        while connected:
            cmd, data = recv_message_and_parse(conn)
            if cmd is None:
                print("Client disconnected unexpectedly")
                break

            connected = handle_client_message(conn, cmd, data)

        conn.close()
        print("Connection closed:", addr)


if __name__ == "__main__":
    main()
