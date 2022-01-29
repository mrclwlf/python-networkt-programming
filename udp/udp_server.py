import socket
import datetime

# print(socket.getservbyname('domain'))
# print(socket.getservbyname('coap'))
import sys

MAX_BYTES = 65535
PORT = 1069  # RND Port
HOST = ''  # Listen on all


def server(address: tuple) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sck:
        sck.bind(address)
        print('Listing at {}'.format((sck.getsockname())))
        total_requests = 0
        while True:
            data, address = sck.recvfrom(MAX_BYTES)
            total_requests += 1
            print(f'Receiving data from client {address} at ' + str(datetime.datetime.now()))
            print(f'Data: {data.decode()}')
            print(f'Total requests: {total_requests}')
            sck.sendto(b'Thank you for your request!', address)


if __name__ == '__main__':
    server((HOST, PORT))
