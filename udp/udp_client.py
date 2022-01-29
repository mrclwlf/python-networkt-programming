import datetime
import random
import socket
import time

MAX_BYTES = 65535
PORT = 1069
HOST = '127.0.0.1'


def client(host: str, port: int, msg: str = 'Hello World!') -> None:
    if type(msg) is not str:
        msg = str(msg)
    msg = bytes(msg, 'utf-8')
    waiting_time = 0.5

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sck:
        sck.connect((host, port))
        sck.settimeout(waiting_time)

        while True:
            sck.send(msg)
            time.sleep(random.random())

            try:
                data = sck.recv(MAX_BYTES)
                print(f'Server {sck.getpeername()} replied: {data.decode()} {datetime.datetime.now()}')

            except socket.timeout:
                waiting_time *= 2  # exponential backoff
                if waiting_time > 2.0:
                    raise RuntimeError('Server is down!')

            else:
                break


if __name__ == '__main__':
    for x in range(15):
        client(host=HOST, port=PORT, msg=random.random())
