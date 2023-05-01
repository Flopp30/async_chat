import json
import socket

from settings import DEFAULT_PORT, DEFAULT_IP_ADDRESS, ENCODING, MAX_PACKAGE_LENGTH, MAX_CONNECTION_COUNT
from utils import Statuses, send_message, get_args


def handle_request(client_socket, request):
    # Обработка запроса от клиента
    response = {}  # Инициализация ответа
    if request["action"] == "presence":
        response["response"] = str(Statuses.OK)
    else:
        response["response"] = str(Statuses.BAD_REQUEST)
    send_message(client_socket, response)


def start_server(host=DEFAULT_IP_ADDRESS, port=DEFAULT_PORT):
    # Запуск сервера
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(MAX_CONNECTION_COUNT)

    while True:
        client_socket, address = server_socket.accept()
        data = client_socket.recv(MAX_PACKAGE_LENGTH).decode(ENCODING)
        request = json.loads(data)
        handle_request(client_socket, request)
        client_socket.close()


def main():
    args = get_args(is_server=True)

    start_server(args.addr, args.port)


if __name__ == "__main__":
    main()
