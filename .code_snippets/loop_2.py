"""
Emulerer HASS
main() kjorer samme kall som HASS custom_component "async def async_setup(hass, config)" ville kjort
HassBusproRepresentationInCustomComponent starter API og StateUpdater
"""

import socket
import asyncio
import logging
import signal

from sys import platform


GATEWAY_ADDRESS_RECEIVE = ('10.120.1.66', 6000)
GATEWAY_ADDRESS_SEND = ('10.120.1.66', 6000)





class Buspro:
    def __init__(self, loop_=None):
        self.loop = loop_ or asyncio.get_event_loop()
        self.sigint_received = asyncio.Event()
        self.state_updater = None
        self.started = False
        self.callback = None
        self.network_interface = None

    def __del__(self):
        if self.started:
            try:
                task = self.loop.create_task(self.stop())
                self.loop.run_until_complete(task)
            except RuntimeError as exp:
                print(f"LOG: Could not close loop, reason: {exp}")

    async def start(self, state_updater=False, daemon_mode=False):

        self.network_interface = NetworkInterface(self, GATEWAY_ADDRESS_RECEIVE, GATEWAY_ADDRESS_SEND)
        await self.network_interface.start()

        if state_updater:
            self.state_updater = StateUpdater(self)
            await self.state_updater.start()

        if daemon_mode:
            await self.loop_until_sigint()

        self.started = True

        # await asyncio.sleep(5)
        # await self.network_interface.send_message(b'\0x01')

    async def stop(self):
        await self._stop_network_interface()
        self.started = False

    async def _stop_network_interface(self):
        if self.network_interface is not None:
            await self.network_interface.stop()
            self.network_interface = None

    def register_telegram_received_cb(self, telegram_received_cb):
        self.callback = telegram_received_cb

    async def loop_until_sigint(self):
        def sigint_handler():
            self.sigint_received.set()
        if platform == "win32":
            print("LOG: Windows does not support signals")
        else:
            self.loop.add_signal_handler(signal.SIGINT, sigint_handler)
        print("LOG: Press Ctrl+C to stop")
        await self.sigint_received.wait()

    async def sync(self):
        await self.callback("LOG: Sync() triggered from StateUpdater")







class StateUpdater:
    def __init__(self, buspro):
        self.buspro = buspro
        self.run_forever = True
        self.run_task = None

    async def start(self):
        self.run_task = self.buspro.loop.create_task(self.run())

    async def run(self):
        await asyncio.sleep(0)
        print("LOG: Starting StateUpdater")

        while True:
            await self.buspro.sync()
            await asyncio.sleep(5)









class NetworkInterface:
    def __init__(self, buspro, gateway_address_receive, gateway_address_send):
        self.gateway_address_receive = gateway_address_receive
        self.gateway_address_send = gateway_address_send
        self.interface = None
        self.buspro = buspro

    async def start(self):
        self.interface = Routing(self.buspro, self.gateway_address_receive, self.gateway_address_send, telegram_received_callback=self.telegram_received)
        await self.interface.start()

    def telegram_received(self, telegram):
        print(f"__{telegram}__")

    async def stop(self):
        if self.interface is not None:
            await self.interface.stop()
            self.interface = None

    async def send_message(self, message):
        await self.interface.send_message(message)







class Routing:
    def __init__(self, buspro, gateway_address_receive, gateway_address_send, telegram_received_callback=None):
        self.buspro = buspro
        self.gateway_address_receive = gateway_address_receive
        self.gateway_address_send = gateway_address_send
        self.telegram_received_callback = telegram_received_callback

        self.udp_client = None
        self.init_udp_client()

    def init_udp_client(self):
        self.udp_client = UDPClient(self.buspro, self.gateway_address_receive, self.gateway_address_send)
        self.udp_client.register_callback(self.routing_request_received)

    def routing_request_received(self, telegram):
        if self.telegram_received_callback is not None:
            self.telegram_received_callback(telegram)

    async def start(self):
        await self.connect_udp()

    async def connect_udp(self):
        await self.udp_client.connect()

    async def stop(self):
        await self.disconnect(True)

    async def disconnect(self, ignore_error=False):
        await self.udp_client.stop()

    async def send_message(self, message):
        await self.udp_client.send_message(message)






class UDPClient:

    class UDPClientFactory(asyncio.DatagramProtocol):

        def __init__(self, buspro, data_received_callback=None):
            self.buspro = buspro
            self.transport = None
            self.data_received_callback = data_received_callback

        def connection_made(self, transport):
            self.transport = transport

        def datagram_received(self, data, addr):
            if self.data_received_callback is not None:
                self.data_received_callback(data)

        def error_received(self, exc):
            print('Error received: %s', exc)

        def connection_lost(self, exc):
            print('closing transport %s', exc)

    def __init__(self, buspro, gateway_address_receive, gateway_address_send):
        self.buspro = buspro
        self.gateway_address_receive = gateway_address_receive
        self.gateway_address_send = gateway_address_send
        self.callback = None
        self.transport = None

    def register_callback(self, callback):
        self.callback = callback

    def data_received_callback(self, telegram):
        print(f"___{telegram}___")

    def create_multicast_sock(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setblocking(False)
        sock.bind(self.gateway_address_receive)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)
        return sock

    async def connect(self):
        try:
            udp_client_factory = UDPClient.UDPClientFactory(self.buspro, data_received_callback=self.data_received_callback)
            sock = self.create_multicast_sock()
            (transport, _) = await self.buspro.loop.create_datagram_endpoint(
                lambda: udp_client_factory, sock=sock)

            self.transport = transport
        except Exception as ex:
            print(f"ERROR: Could not connect: {ex}")

    async def stop(self):
        self.transport.close()

    async def send_message(self, message):
        self.transport.sendto(message, self.gateway_address_send)
















class HassBusproRepresentationInCustomComponent:
    def __init__(self, config=None):
        self.config = config
        self.connected = False

        self._init_buspro()
        self._register_callbacks()

    def _init_buspro(self):
        loop_ = asyncio.get_event_loop()    # HASS event loop
        self.buspro = Buspro(loop_=loop_)
        pass

    async def start(self):
        await self.buspro.start(state_updater=True)
        self.connected = True

    async def stop(self):
        await self.buspro.stop()
        self.connected = False

    async def telegram_received_cb(self, telegram):
        print(f"Telegram received: {telegram}")

    def _register_callbacks(self):
        self.buspro.register_telegram_received_cb(self.telegram_received_cb)









async def main():
    component = HassBusproRepresentationInCustomComponent()
    await component.start()

    await asyncio.sleep(3.5)
    print("LOG: Component started 3.5 seconds ago")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever()
