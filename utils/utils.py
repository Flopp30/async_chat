import json
from argparse import Namespace
from enum import Enum
import socket
from settings import ENCODING, DEFAULT_PORT, DEFAULT_IP_ADDRESS


class CustomEnum(Enum):

    def __str__(self):
        return str(str(self.value))


class Statuses(CustomEnum):
    # Basic notification
    BASE_NOTIFICATION = 100
    IMPORTANT_NOTIFICATION = 101

    # Success statuses
    OK = 200
    CREATED = 201
    ACCEPTED = 202

    # Client errors
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    INCORRECT_LOGIN_PASSWORD = 402
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    GONE = 410

    # Server errors
    SERVER_ERROR = 500


def send_message(sock: socket.socket, message: dict):
    message = json.dumps(message)
    encoded_message = message.encode(ENCODING)
    sock.send(encoded_message)


def make_presence() -> dict:
    # Формирование presence-сообщения
    request = {"action": "presence"}
    return request


def get_args(is_server: bool = True) -> Namespace:
    import argparse

    parser = argparse.ArgumentParser()
    if is_server:
        help_text = 'for'
    else:
        help_text = 'of'

    parser.add_argument('-a', "--addr", type=str,
                        default=DEFAULT_IP_ADDRESS,
                        help=f"IP-address {help_text} server (default {DEFAULT_IP_ADDRESS}"
                        )
    parser.add_argument('-p', "--port", type=int,
                        default=DEFAULT_PORT, nargs="?",
                        help=f"TCP-port {help_text} server (default {DEFAULT_PORT})")

    return parser.parse_args()
