import asyncio

class Server(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        msg = data.decode()
        print(f'Received: {msg} from {addr}')
        data = b'Thanks for your request!'
        print(f'Send: {data.decode()} to {addr}')
        self.transport.sendto(data, addr)

if __name__ == '__main__':
    try:
        loop = asyncio.new_event_loop()
        t = loop.create_datagram_endpoint(lambda: Server(), local_addr=('127.0.0.1', 42069))
        loop.run_until_complete(t)
        loop.run_forever()
    except KeyboardInterrupt:
        print('Server was Shutdown by Keyboard interrupt!')
    finally:
        t.close()