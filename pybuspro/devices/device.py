import asyncio
from ..core.telegram import Telegram
from ..helpers.enums import OperateCode


class Device(object):
    def __init__(self, buspro, device_address, name):
        # device_address = (subnet_id, device_id, ...)

        self._device_address = device_address[:2]
        self._buspro = buspro
        self._name = name
        self.device_updated_cbs = []

    @property
    def name(self):
        return self._name

    def register_telegram_received_cb(self, telegram_received_cb):
        self._buspro.register_telegram_received_device_cb(telegram_received_cb, self._device_address)

    def register_device_updated_cb(self, device_updated_cb):
        """Register device updated callback."""
        self.device_updated_cbs.append(device_updated_cb)

    def unregister_device_updated_cb(self, device_updated_cb):
        """Unregister device updated callback."""
        self.device_updated_cbs.remove(device_updated_cb)

    async def device_updated(self):
        for device_updated_cb in self.device_updated_cbs:
            await device_updated_cb(self)

    async def send_telegram(self, telegram):
        await self._buspro.network_interface.send_telegram(telegram)

        # Should only be called when we receive a response from the bus
        # await self.device_updated()

    def call_device_updated(self):
        asyncio.ensure_future(self.device_updated(), loop=self._buspro.loop)

    def _call_read_current_status_of_channels(self, run_from_init=False):
        asyncio.ensure_future(
            self._read_current_state(OperateCode.ReadStatusOfChannels, run_from_init), loop=self._buspro.loop)

    async def _read_current_state(self, operate_code, run_from_init=False):
        if run_from_init:
            await asyncio.sleep(1)
        telegram = Telegram()
        telegram.target_address = self._device_address
        telegram.payload = []
        telegram.operate_code = operate_code
        await self.send_telegram(telegram)
