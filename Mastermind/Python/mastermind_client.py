#!/usr/bin/env python3
#
import sys
import socket


class MastermindClient:
    """
        A simple command-line client for the Mastermind game
    """

    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((host, int(port)))
        except socket.error as err:
            print(
                f'Error connecting to server: {err.strerror}', file=sys.stderr)
            exit(1)

    def loop(self):
        for line in sys.stdin:
            self.socket.send(line.encode('utf-8'), 1024)
            response = self.socket.recv(1024).decode('utf-8').strip()
            print(response)
            if response == '4 4':
                break


def main():
    if len(sys.argv) < 3:
        print(
            "Please enter [host address] and [port] as arguments", file=sys.stderr)
        exit(1)
    client = MastermindClient(sys.argv[1], sys.argv[2])
    client.loop()


if __name__ == '__main__':
    main()
