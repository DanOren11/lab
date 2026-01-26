import socket
import random
from U1.chatlib import build_message, parse_message

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5678

users = {}
questions = {}
logged_users = {}

PROTOCOL_SERVER = {
    "login_ok_msg": "LOGIN_OK",
    "login_failed_msg": "LOGIN_FAILED",
    "get_score_msg": "YOUR_SCORE",
    "get_highscore_msg": "ALL_SCORES",
    "logged_msg": "LOGGED_USERS",
    "get_question_msg": "QUESTION",
    "get_answer_msg": "ANSWER"
}

PROTOCOL_CLIENT = {
    "login_msg": "LOGIN",
    "logout_msg": "LOGOUT",
    "get_score_msg": "MY_SCORE",
    "get_highscore_msg": "HIGHSCORE",
    "logged_msg": "LOGGED",
    "get_question_msg": "GET_QUESTION",
    "get_answer_msg": "SEND_ANSWER"
}


def load_users():
    return {
        "test": {"password": "test", "score": 0},
        "dan": {"password": "dan", "score": 0},
        "admin": {"password": "admin", "score": 0}
    }


def load_questions():
    return {
        1: {
            "question": "How much is 1+1?",
            "answers": ["1", "2", "3", "4"],
            "correct": "2"
        },
        2: {
            "question": "Capital of France?",
            "answers": ["Berlin", "Paris", "Rome", "Madrid"],
            "correct": "2"
        }
    }


def build_and_send_message(conn, code, data):
    msg = build_message(code, data)
    conn.sendall(msg.encode())


def recv_message_and_parse(conn):
    try:
        msg = conn.recv(2048).decode()
        return parse_message(msg)
    except Exception:
        return None, None


def handle_question_message(conn, username):
    question = random.choice(list(questions.values()))
    users[username]["last_question"] = question
    formatted_question = (
        f"{question['question']}#"
        f"{question['answers'][0]}#"
        f"{question['answers'][1]}#"
        f"{question['answers'][2]}#"
        f"{question['answers'][3]}"
    )
    build_and_send_message(conn, PROTOCOL_SERVER["get_question_msg"], formatted_question)


def handle_answer_message(conn, username, data):
    question = users[username].get("last_question")
    correct = question["correct"]

    if data == correct:
        users[username]["score"] += 5
        build_and_send_message(conn, PROTOCOL_SERVER["get_answer_msg"], "correct")
    else:
        build_and_send_message(
            conn,
            PROTOCOL_SERVER["get_answer_msg"],
            f"wrong#{correct}"
        )


def handle_client(conn):
    addr = conn.getpeername()

    while True:
        cmd, data = recv_message_and_parse(conn)
        if cmd is None:
            break

        if cmd == PROTOCOL_CLIENT["login_msg"]:
            username, password = data.split("#")
            if username in users and users[username]["password"] == password:
                logged_users[addr] = username
                build_and_send_message(conn, PROTOCOL_SERVER["login_ok_msg"], "")
            else:
                build_and_send_message(conn, PROTOCOL_SERVER["login_failed_msg"], "")

        elif cmd == PROTOCOL_CLIENT["logout_msg"]:
            logged_users.pop(addr, None)
            break

        elif cmd == PROTOCOL_CLIENT["get_score_msg"]:
            username = logged_users.get(addr)
            if not username:
                build_and_send_message(conn, PROTOCOL_SERVER["login_failed_msg"], "")
                return
            build_and_send_message(
                conn,
                PROTOCOL_SERVER["get_score_msg"],
                str(users[username]["score"])
            )

        elif cmd == PROTOCOL_CLIENT["get_highscore_msg"]:
            scores = [
                f"{u}:{d['score']}" for u, d in users.items()
            ]
            build_and_send_message(
                conn,
                PROTOCOL_SERVER["get_highscore_msg"],
                "#".join(scores)
            )

        elif cmd == PROTOCOL_CLIENT["logged_msg"]:
            build_and_send_message(
                conn,
                PROTOCOL_SERVER["logged_msg"],
                "#".join(logged_users.values())
            )

        elif cmd == PROTOCOL_CLIENT["get_question_msg"]:
            username = logged_users.get(addr)
            if not username:
                build_and_send_message(conn, PROTOCOL_SERVER["login_failed_msg"], "")
                return
            handle_question_message(conn, username)

        elif cmd == PROTOCOL_CLIENT["get_answer_msg"]:
            username = logged_users.get(addr)
            if not username:
                build_and_send_message(conn, PROTOCOL_SERVER["login_failed_msg"], "")
                return
            handle_answer_message(conn, username, data)

    conn.close()


def main():
    global users, questions

    users = load_users()
    questions = load_questions()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen()

    print("Server running")

    while True:
        conn, _ = server.accept()
        handle_client(conn)


if __name__ == "__main__":
    main()
