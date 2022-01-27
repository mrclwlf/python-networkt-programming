import socket
import sys


def receive_data(sck: socket) -> bytes:
    data = b''
    try:
        while True:
            msg = sck.recv(4096)
            data += msg
            if not msg:
                break
    #except sck.settimeout(1):
       #print('Timeout')
    finally:
        return data

def server(host: str, port: int) -> None:
    sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sck.bind((host, port))
    sck.listen(1)
    print('Listening at', sck.getsockname())
    while True:
        sc, address = sck.accept()
        print('Accepted a connection from ', address)
        print('Socket name: ', sc.getsockname())
        print('Socket peer: ', sc.getpeername())
        data = receive_data(sc)
        print(data.decode('utf-8'))
        sc.sendall(b'Thanks for your request')
        sc.close()
        print('Connection closed')


if __name__ == '__main__':
    server('localhost', 42069)
