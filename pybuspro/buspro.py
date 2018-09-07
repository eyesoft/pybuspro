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

        self.callback_all_messages = None
        self._telegram_received_cbs = []

        self.gateway_address_send_receive = gateway_address_send_receive

    def __del__(self):
        if self.started:
            try:
                task = self.loop.create_task(self.stop())
                self.loop.run_until_complete(task)
            except RuntimeError as exp:
                print(f"ERROR: Could not close loop, reason: {exp}")

    async def start(self, state_updater=False):  # , daemon_mode=False):
        self.network_interface = NetworkInterface(self, self.gateway_address_send_receive)
        await self.network_interface.start()
        self.network_interface.register_callback(self._callback_all_messages)

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

    def _callback_all_messages(self, telegram):
        if self.callback_all_messages is not None:
            self.callback_all_messages(telegram)

        for telegram_received_cb in self._telegram_received_cbs:
            device_address = telegram_received_cb['device_address']

            # Sender callback kun for oppgitt kanal
            if device_address == telegram.target_address:
                telegram_received_cb['callback'](telegram)
                # telegram_received_cb['callback'](f"{device_address} ==> {str(telegram)}")

    async def _stop_network_interface(self):
        if self.network_interface is not None:
            await self.network_interface.stop()
            self.network_interface = None

    def register_telegram_received_all_messages_cb(self, telegram_received_cb):
        self.callback_all_messages = telegram_received_cb

    def register_telegram_received_device_cb(self, telegram_received_cb, device_address):
        self._telegram_received_cbs.append({'callback': telegram_received_cb, 'device_address': device_address})

    @staticmethod
    async def sync():
        # await self.callback("LOG: Sync() triggered from StateUpdater")
        # print("LOG: Sync() triggered from StateUpdater")
        raise NotImplementedError
