import json
import threading
import time
from argparse import Namespace
from unittest import (
    TestCase,
    mock,
    main as unittest_main,
)
from socket import socket, AF_INET, SOCK_STREAM
from server import handle_request, start_server
from settings import MAX_PACKAGE_LENGTH, ENCODING, DEFAULT_PORT, DEFAULT_IP_ADDRESS
from utils import Statuses, send_message, get_args, make_presence


class TestServer(TestCase):
    def test_handle_request_presence(self):
        # Создаем фейковый сокет и запрос от клиента
        client_socket = mock.Mock()
        request = make_presence()

        # Вызываем функцию обработки запроса и получаем ответ
        handle_request(client_socket, request)
        response = json.loads(client_socket.send.call_args[0][0])

        # Проверяем, что ответ содержит код успешного выполнения
        self.assertEqual(response["response"], str(Statuses.OK))

    def test_handle_request_bad_request(self):
        # Создаем фейковый сокет и запрос от клиента
        client_socket = mock.Mock()
        request = {"action": "another_action"}

        # Вызываем функцию обработки запроса и получаем ответ
        handle_request(client_socket, request)
        response = json.loads(client_socket.send.call_args[0][0])

        # Проверяем, что ответ содержит код ошибки запроса
        self.assertEqual(response["response"], str(Statuses.BAD_REQUEST))

    def run_server_in_thread(self, host, port):
        self.server_thread = threading.Thread(target=start_server, args=(host, port))
        self.server_thread.start()
        time.sleep(1)

    def stop_server(self, host, port):
        sock = socket()
        sock.connect((host, port))
        sock.close()

    def test_start_server(self):
        host = DEFAULT_IP_ADDRESS
        port = DEFAULT_PORT + 1

        self.run_server_in_thread(host, port)

        with socket(AF_INET, SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))

            request = make_presence()
            encoded_request = json.dumps(request).encode(ENCODING)

            client_socket.send(encoded_request)
            response = client_socket.recv(MAX_PACKAGE_LENGTH).decode(ENCODING)
            self.stop_server(host, port)

            response = json.loads(response)

            self.assertEqual(response['response'], str(Statuses.OK))

    def test_get_args_server(self):
        args = get_args(is_server=True)
        self.assertIsInstance(args, Namespace)
        self.assertEqual(args.addr, DEFAULT_IP_ADDRESS)
        self.assertEqual(args.port, DEFAULT_PORT)

    def test_send_message(self):
        host = DEFAULT_IP_ADDRESS
        port = DEFAULT_PORT + 2
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen()

        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((host, port))

        message = {"text": "Hello, world!", "timestamp": 123456}
        send_message(client_socket, message)
        received_data = server_socket.accept()[0].recv(1024)
        decoded_data = received_data.decode(ENCODING)
        decoded_message = json.loads(decoded_data)
        server_socket.close()
        client_socket.close()
        self.assertEqual(decoded_message, message)


if __name__ == '__main__':
    unittest_main()
        