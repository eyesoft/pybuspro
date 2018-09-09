import asyncio
import socket


class UDPClient:

    class UDPClientFactory(asyncio.DatagramProtocol):

        def __init__(self, buspro, data_received_callback=None):
            self.buspro = buspro
            self.transport = None
            self.data_received_callback = data_received_callback

        def connection_made(self, transport):
            self.transport = transport

        def datagram_received(self, data, address):
            if self.data_received_callback is not None:
                self.data_received_callback(data, address)

        def error_received(self, exc):
            print('ERROR: Error received: %s', exc)

        def connection_lost(self, exc):
            print('ERROR: closing transport %s', exc)

    def __init__(self, buspro, gateway_address_send_receive, callback):
        self.buspro = buspro
        self.gateway_address_send_receive = gateway_address_send_receive
        self.callback = callback
        self.transport = None

    # def register_callback(self, callback):
    #     self.callback = callback

    def _data_received_callback(self, data, address):
        self.callback(data, address)

    def _create_multicast_sock(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setblocking(False)

        _, gateway_address_receive = self.gateway_address_send_receive
        sock.bind(gateway_address_receive)

        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)
        return sock

    async def _connect(self):
        try:
            udp_client_factory = \
                UDPClient.UDPClientFactory(self.buspro, data_received_callback=self._data_received_callback)
            sock = self._create_multicast_sock()
            (transport, _) = await self.buspro.loop.create_datagram_endpoint(lambda: udp_client_factory, sock=sock)

            self.transport = transport
        except Exception as ex:
            print(f"ERROR: Could not connect: {ex}")

    async def start(self):
        await self._connect()

    async def stop(self):
        self.transport.close()

    async def send_message(self, message):
        gateway_address_send, _ = self.gateway_address_send_receive
        self.transport.sendto(message, gateway_address_send)
