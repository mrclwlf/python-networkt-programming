import asyncio
HOST = '127.0.0.1'
PORT = 42069

class Client(asyncio.Protocol):
    def __init__(self, msg: str, con_lost):
        self.msg = msg
        self.transport = None
        self.con_lost = con_lost

    def connection_made(self, transport):
        self.transport = transport
        print(f'Send message to {HOST} : {PORT}')
        self.transport.sendto(self.msg.encode(), (HOST, PORT))

    def connection_lost(self, exc):
        print("Connection ended")
        self.con_lost.set_result(True)

    def datagram_received(self, data, adadr):
        print(data.decode())
        self.transport.sendto(b'sjkdfaf', (HOST,PORT))
        self.transport.close()



async def main():
    loop = asyncio.get_running_loop()
    con_lost = loop.create_future()
    transport, protocol = await loop.create_datagram_endpoint(lambda: Client(msg='Hello!', con_lost=con_lost), remote_addr=(HOST,PORT))

    try:
        await con_lost
    finally:
        transport.close()


if __name__ == '__main__':
    asyncio.run(main())
