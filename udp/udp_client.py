import datetime
import random
import socket
import sys
import time

MAX_BYTES = 65535
PORT = 1069  # RND Port
HOST = '127.0.0.1'


def client(host: str, port: int, msg: str = 'Hello World!') -> None:
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    msg = bytes(msg, 'utf-8')
    for x in range(10):
        time.sleep(random.random())
        sck.sendto(msg, (host, port))
        data, address = sck.recvfrom(MAX_BYTES)
        print(f'{x+1}. Server replied: {data.decode()} {datetime.datetime.now()}')


if __name__ == '__main__':
    client(host=HOST, port=PORT)
