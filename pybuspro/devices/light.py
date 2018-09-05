from pybuspro.devices.device import Device
from pybuspro.api.telegram import Telegram


class Light(Device):
    def __init__(self,  buspro, device_address):
        super().__init__(buspro, device_address)
        self._device_address = device_address
        self._buspro = buspro
        
    async def turn_on(self):
        telegram = Telegram(target_address=self._device_address, payload=100)
        await self._buspro.send_message(telegram)
        
    async def turn_off(self):
        telegram = Telegram(target_address=self._device_address, payload=0)
        await self._buspro.send_message(telegram)
        
    async def dim(self, intensity):
        telegram = Telegram(target_address=self._device_address, payload=intensity)
        await self._buspro.send_message(telegram)
