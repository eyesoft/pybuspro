from pybuspro.transport.udp_client import UDPClient


class NetworkInterface:
    def __init__(self, buspro, gateway_address_receive, gateway_address_send):
        self.buspro = buspro
        self.gateway_address_receive = gateway_address_receive
        self.gateway_address_send = gateway_address_send
        self.udp_client = None
        self.callback = None
        self._init_udp_client()

    def _init_udp_client(self):
        self.udp_client = UDPClient(self.buspro, self.gateway_address_receive, self.gateway_address_send)
        self.udp_client.register_callback(self._udp_request_received)

    def register_callback(self, callback):
        self.callback = callback

    def _udp_request_received(self, telegram):
        if self.callback is not None:
            self.callback(telegram)

    async def start(self):
        await self.udp_client.start()

    async def stop(self):
        if self.udp_client is not None:
            await self.udp_client.stop()
            self.udp_client = None

    async def send_message(self, message):
        await self.udp_client.send_message(message)
