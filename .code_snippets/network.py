import asyncio
import logging
import signal
import socket

from sys import platform


class UDPClientFactory(asyncio.DatagramProtocol):

    def __init__(self, data_received_callback=None):
        self.transport = None
        self.data_received_callback = data_received_callback

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        print(f'RECEIVED: {data}')
        if self.data_received_callback is not None:
            self.data_received_callback(data)

    def error_received(self, exc):
        print('Error received: %s', exc)

    def connection_lost(self, exc):
        print('closing transport %s', exc)


class Main:
    def __init__(self):
        self.transport = None

    def data_received_callback(self, message):
        print(f"Callback: {message}")


    @staticmethod
    def create_multicast_sock(address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setblocking(False)

        '''
        sock.setsockopt(
            socket.SOL_IP,
            socket.IP_MULTICAST_IF,
            socket.inet_aton(own_ip))
        sock.setsockopt(
            socket.SOL_IP,
            socket.IP_ADD_MEMBERSHIP,
            socket.inet_aton(remote_addr[0]) +
            socket.inet_aton(own_ip))
        sock.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_MULTICAST_TTL, 2)
        sock.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_MULTICAST_IF,
            socket.inet_aton(own_ip))
        '''

        # I have no idea why we have to use different bind calls here
        # - bind() with multicast addr does not work with gateway search requests
        #   on some machines. It only works if called with own ip. It also doesn't
        #   work on Mac OS.
        # - bind() with own_ip does not work with ROUTING_INDICATIONS on Gira
        #   knx router - for an unknown reason.
        # if bind_to_multicast_addr:
        sock.bind(address)
        # else:
        #    sock.bind((own_ip, 0))
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)
        return sock


    async def main(self):
        loop = asyncio.get_event_loop()

        udp_client_factory = UDPClientFactory(data_received_callback=self.data_received_callback)

        '''
        (transport, _) = await loop.create_datagram_endpoint(
            lambda: udp_client_factory,
            remote_addr=('192.168.1.15', 6000))
        '''

        sock = self.create_multicast_sock(('', 6000))
        (transport, _) = await loop.create_datagram_endpoint(
            lambda: udp_client_factory, sock=sock)

        self.transport = transport


async def main():
    main_ = Main()
    await main_.main()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever()

