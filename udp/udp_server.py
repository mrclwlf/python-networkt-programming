import socket
import datetime

# print(socket.getservbyname('domain'))
# print(socket.getservbyname('coap'))
import sys

MAX_BYTES = 65535
PORT = 1069  # RND Port
HOST = '' # Listen on all


def server(address: tuple) -> None:
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sck.bind(address)
    print('Listing at {}'.format((sck.getsockname())))
    try:
        while True:
            data, address = sck.recvfrom(MAX_BYTES)
            print(f'Receiving data from client {address} at ' + str(datetime.datetime.now()) )
            print(f'Data: {data.decode()}')
            sck.sendto(b'Thank you for your request!', address)

    except KeyboardInterrupt:
        print('Keyboard Interrupt')
        sys.exit(0)


if __name__ == '__main__':
    server((HOST, PORT))
