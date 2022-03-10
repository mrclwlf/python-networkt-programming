from ctypes import cast
import ssl

from aioquic.asyncio.protocol import QuicConnectionProtocol, QuicStreamHandler
from aioquic.quic import events
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.connection import QuicConnection, logger
import asyncio

from aioquic.quic.events import QuicEvent


class Client(QuicConnectionProtocol):
    def __init__(self,  *args, **kwargs):
        self.config = QuicConfiguration(is_client=True, alpn_protocols='coap', idle_timeout=7)
        self.config.verify_mode = ssl.CERT_NONE
        self.quic = QuicConnection(configuration=self.config)
        super().__init__(quic=self.quic)

        self._ack_waiter = None

    async def send_data(self, data: bytes) -> None:
        sid = self._quic.get_next_available_stream_id()
        stream_end = True
        self._quic.send_stream_data(sid, data, stream_end)
        waiter = self._loop.create_future()
        self._ack_waiter = waiter
        self.transmit()

        return await asyncio.shield(waiter)

    def quic_event_received(self, event: QuicEvent) -> None:
        print(event)
        if self._ack_waiter is not None:
            if isinstance(event, events.StreamDataReceived):
                response = event.data
                print(response.decode())
                logger.info(response)
                waiter = self._ack_waiter
                self._ack_waiter = None
                waiter.set_result(None)
            if isinstance(event, events.ConnectionTerminated):
                if event.error_code != 0:
                    print(event.error_code)
                    print(event.reason_phrase)
                    waiter = self._ack_waiter
                    self._ack_waiter = None
                    waiter.set_result(None)



async def main():
    loop = asyncio.get_running_loop()
    f = loop.create_future()
    transport, protocol = await loop.create_datagram_endpoint(lambda: Client(), remote_addr=('localhost', 42069))
    try:
        protocol.connect(('::1', 42069, 0, 0))
        await protocol.wait_connected()
        await protocol.send_data("MASSA".encode())
    finally:
        protocol.close()
        await protocol.wait_closed()
        transport.close()

if __name__ == '__main__':
    asyncio.run(main())