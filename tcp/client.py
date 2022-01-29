import socket
import time
from random import random


def receive_data(sck: socket) -> bytes:
    data = b''
    try:
        while True:
            msg = sck.recv(4096)
            data += msg
            if not msg:
                break
    finally:
        return data

def client(host: str, port: int) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sck:
        sck.connect((host, port))
        print('Assigned to', sck.getsockname())
        data = ['I hear your heart beat to the beat of the drums\n',
            'Oh, what a shame that you came here with someone\n',
            'So while you\'re here in my arms\n',
            'Let\'s make the most of the night like we\'re gonna die young.']

        for elem in data:
            sck.sendall(bytes(elem, 'utf-8'))
            print(len(elem))


        #DEADLOCK
        reply = ''
        #while not reply:
            #reply=sck.recv(2048)
        reply = receive_data(sck)

        print(reply.decode())

        sck.close()
        print('Connection closed')


if __name__ == '__main__':
    for i in range(10):
        client(host='localhost', port=42069)