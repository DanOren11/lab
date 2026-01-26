# Protocol Constants

CMD_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4  # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10 ** LENGTH_FIELD_LENGTH - 1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

PROTOCOL_CLIENT = {
    "login_msg": "LOGIN",
    "logout_msg": "LOGOUT",
    "get_score_msg": "SCORE",
    "get_highscore_msg": "HIGHSCORE",
    "get_question_msg": "QUESTION",
    "get_answer_msg": "ANSWER",
    "get_connected_users_msg":"CONNECTED_USERS",
}

PROTOCOL_SERVER = {
    "login_ok_msg": "LOGIN_OK",
    "login_failed_msg": "ERROR",
    "get_score_msg": "SCORE",
    "get_highscore_msg": "HIGHSCORE",
    "logout_msg": "LOGOUT",
    "get_question_msg": "QUESTION",
    "get_answer_msg": "ANSWER",
    "get_connected_users_msg": "CONNECTED_USERS",

}
ERROR_RETURN = Exception("failed to login")


def build_message(cmd, data):
    if not isinstance(cmd, str) or not isinstance(data, str):
        return None, None
    if len(cmd) > CMD_FIELD_LENGTH:
        return None, None
    if len(data) > MAX_DATA_LENGTH:
        return None, None
    cm_fields = cmd.ljust(CMD_FIELD_LENGTH)
    data_length = str(len(data)).zfill(LENGTH_FIELD_LENGTH)
    full_message = f"{cm_fields}{DELIMITER}{data_length}{DELIMITER}{data}"
    if len(full_message) > MAX_MSG_LENGTH:
        return None, None

    return full_message


def parse_message(data):
    try:
        cmd_fields = data[:CMD_FIELD_LENGTH]
        delimiter1 = data[CMD_FIELD_LENGTH]
        length_field = data[CMD_FIELD_LENGTH + 1: CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH]
        delimiter2 = data[CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH]

        if delimiter1 != DELIMITER or delimiter2 != DELIMITER:
            return None

        msg_length = int(length_field)
        msg_start = MSG_HEADER_LENGTH
        msg_end = MSG_HEADER_LENGTH + msg_length
        msg = data[msg_start:msg_end]

        cmd = cmd_fields.strip()
        return cmd, msg
    except Exception:
        return None


def split_data(msg, expected_fields):
    try:
        if not isinstance(msg, str) or not isinstance(expected_fields, int):
            return None
        if expected_fields <= 0:
            return None
        fields = msg.split(DATA_DELIMITER)
        if len(fields) != expected_fields:
            return None

        return fields
    except Exception:
        return None


def join_data(msg_fields):
    try:
        if not isinstance(msg_fields, list):
            return None
        msg = DATA_DELIMITER.join(msg_fields)
        return msg
    except Exception:
        return None
