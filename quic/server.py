import asyncio
import sys

from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.asyncio.server import QuicServer
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.connection import QuicConnection
from aioquic.quic.events import StreamDataReceived, QuicEvent
from aioquic.quic.packet import PACKET_TYPE_INITIAL
from aioquic.quic import events


def pull_dcid(data: bytes):
    if (data[0] & 0x80) != 0:
        long_header = data[0] & 0x80
        version = data[1:5]

    else:
        print("Not supportet version!")
        sys.exit(0)
    scid_length = data[5]
    scid = data[6:6 + scid_length]
    return scid


class Server(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quic = self._quic

    def quic_event_received(self, event: QuicEvent) -> None:
        print(event)
        if isinstance(event, StreamDataReceived):
            data = event.data
            print(data.decode())
            if event.end_stream:
                self.quic.send_stream_data(event.stream_id, b'Goodbye' ,end_stream=True)


if __name__ == '__main__':

    config = QuicConfiguration(is_client=False, alpn_protocols='coap')
    config.load_cert_chain("ssl_cert.pem", "ssl_key.pem")
    try:
        loop = asyncio.new_event_loop()
        transport, protocol = await loop.create_datagram_endpoint(lambda: QuicServer(configuration=config, create_protocol=Server), local_addr=('localhost', 5683))
        loop.run_until_complete(transport)
        loop.run_forever()
    except KeyboardInterrupt:
        print('Server was Shutdown by Keyboard interrupt!')
    finally:
        protocol.close()
