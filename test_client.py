import threading
import time
import unittest
from argparse import Namespace
from socket import socket, AF_INET, SOCK_STREAM

from server import start_server
from client import send_request
from settings import DEFAULT_IP_ADDRESS, DEFAULT_PORT
from utils import make_presence, Statuses, get_args


class TestClient(unittest.TestCase):
    host = DEFAULT_IP_ADDRESS
    port = DEFAULT_PORT

    def run_server_in_thread(self, host, port):
        self.server_thread = threading.Thread(target=start_server, args=(host, port))
        self.server_thread.start()
        time.sleep(1)

    def stop_server(self, host, port):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((host, port))
        sock.close()

    def test_send_request(self):
        self.run_server_in_thread(self.host, self.port)
        message = make_presence()
        response = send_request(self.host, self.port, request=message)
        self.stop_server(self.host, self.port)

        self.assertEqual(response['response'], str(Statuses.OK))

    def test_get_args_client(self):
        args = get_args(is_server=False)
        self.assertIsInstance(args, Namespace)
        self.assertEqual(args.addr, DEFAULT_IP_ADDRESS)
        self.assertEqual(args.port, DEFAULT_PORT)

    def test_make_presence(self):
        self.assertEqual(make_presence(), {"action": "presence"})


if __name__ == '__main__':
    unittest.main()
