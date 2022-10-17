#!/usr/bin/env python3
#
import socket
import sys
import logging
import threading

from mastermind_player import MastermindPlayer


class MastermindServer:
    """
        Implement a simple TCP server for the Mastermind game
    """

    def __init__(self, listen_address, port):
        logging.basicConfig(level=logging.DEBUG)
        self.listen_address = listen_address
        self.port = int(port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.listen_address, self.port))

    def accept_client(self, connection_socket, addr):
        logging.debug(f'Accepted connection from: {addr}')
        player = MastermindPlayer()
        with connection_socket as s:
            while True:
                data = s.recv(100).decode('utf-8').strip()
                if len(data) == 0:
                    break
                logging.debug(f'received: {data}')
                (done, grade) = player.grade(data)
                s.send(grade.encode('utf-8'))
                if done:
                    break

        connection_socket.close()
        logging.debug(f'Closed connection from: {addr}')

    def listen(self):
        logging.debug(f'Listening on {self.listen_address} port {self.port}')
        self.socket.listen()
        try:
            while True:
                conn, addr = self.socket.accept()
                t = threading.Thread(
                    target=self.accept_client, args=(conn, addr), daemon=True)
                t.start()
        except KeyboardInterrupt:
            print("Killed, exiting", file=sys.stderr)
        finally:
            self.socket.close()


def main():
    if len(sys.argv) < 3:
        print("Please enter [listen address] and [port] as arguments", file=sys.stderr)
        exit(1)
    server = MastermindServer(sys.argv[1], sys.argv[2])
    server.listen()


if __name__ == '__main__':
    main()
