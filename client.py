import json
import socket

from settings import ENCODING, MAX_PACKAGE_LENGTH
from utils import send_message, Statuses, make_presence, get_args


def send_request(host, port, request) -> dict:
    # Отправка запроса на сервер
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    send_message(sock=client_socket, message=request)

    data = client_socket.recv(MAX_PACKAGE_LENGTH).decode(ENCODING)
    response = json.loads(data)
    client_socket.close()

    return response


def main():
    args = get_args(is_server=False)

    # Отправка presence-сообщения на сервер
    presence_request = make_presence()
    response = send_request(args.addr, args.port, presence_request)

    # Обработка ответа сервера
    if response["response"] == str(Statuses.OK):
        print("Server is available")
    else:
        print("Server is not available")


if __name__ == "__main__":
    main()
