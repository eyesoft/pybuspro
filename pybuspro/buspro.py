import asyncio

from pybuspro.transport.network_interface import NetworkInterface
from pybuspro.core.state_updater import StateUpdater

# ip, port = gateway_address
# subnet_id, device_id, channel = device_address


class Buspro:

    def __init__(self, gateway_address_send_receive, loop_=None):
        self.loop = loop_ or asyncio.get_event_loop()
        self.state_updater = None
        self.started = False
        self.network_interface = None

        self.callback = None
        self._telegram_received_cbs = []

        self.gateway_address_send_receive = gateway_address_send_receive

    def __del__(self):
        if self.started:
            try:
                task = self.loop.create_task(self.stop())
                self.loop.run_until_complete(task)
            except RuntimeError as exp:
                print(f"ERROR: Could not close loop, reason: {exp}")

    async def start(self, state_updater=False):     # , daemon_mode=False):
        self.network_interface = NetworkInterface(self, self.gateway_address_send_receive)
        await self.network_interface.start()
        self.network_interface.register_callback(self.callback)

        if state_updater:
            self.state_updater = StateUpdater(self)
            await self.state_updater.start()

        '''
        if daemon_mode:
            await self._loop_until_sigint()
        '''

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

    def register_telegram_received_cb_2(self, telegram_received_cb):
        self.callback = telegram_received_cb

    def register_telegram_received_cb(self, telegram_received_cb, device_address):
        self._telegram_received_cbs.append({'callback': telegram_received_cb, 'device_address': device_address})

    @staticmethod
    async def sync():
        # await self.callback("LOG: Sync() triggered from StateUpdater")
        # print("LOG: Sync() triggered from StateUpdater")
        pass

    async def _send_message(self, message):
        await self.network_interface.send_message(message)

    '''
    ''''''
    async def simple(self, callback=None):
        iterations = 15
        i = 0
        while True:
            i += 1

            telegram = Telegram(source_address=(1, 120, 10))
            telegram.payload = f"[{i}]"
            # print(telegram.payload)
            # print(telegram.source_address)
            # print(str(telegram))

            if callback is not None:
                await callback(telegram)

            for telegram_received_cb in self._telegram_received_cbs:
                device_address = telegram_received_cb['device_address']

                # Sender callback kun for oppgitt kanal
                if device_address[2] == i:
                    ret = await telegram_received_cb['callback'](f"{device_address} ==> {str(telegram)}")

            if i == iterations:
                break

            await asyncio.sleep(1)
    ''''''

    async def listen(self, callback=None):

        if not self._socket:
            print('Socket not created. Please run connect().')
            sys.exit()

        # now keep talking with the client
        while 1:

            # udp_address = ('192.168.1.15', 6000)
            # data = b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x0f\x01\x17\x00\x95\x001\x01J\x01d\x00\x03\xd7\xd1'

            # receive data from client (data, addr)
            data, udp_address = self._socket.recvfrom(1024)

            self.build_telegram(data)
    
            if callback:
                await callback(f"Received telegram from callback: {telegram}")

            ''''''
            for telegram_received_cb in self._telegram_received_cbs:
                device_address = telegram_received_cb['device_address']

                # Sender callback kun for oppgitt kanal
                if device_address[2] == i:
                    await telegram_received_cb['callback'](f"{device_address} ==> {str(telegram)}")
            ''''''

            break

        await self.disconnect()
   '''
