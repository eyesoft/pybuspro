from pybuspro.devices.device import Device
from pybuspro.core.telegram import Telegram
from pybuspro.core.enums import OperateCode


class Light(Device):
    def __init__(self, buspro, device_address):
        super().__init__(buspro, device_address)

        self._device_address = device_address
        self._device_address = device_address[:2]
        _, _, self._channel = device_address
        self._buspro = buspro

        self._state = False
        self._brightness = 0

        # print(self._device_address)
        # print(self._channel)

    async def set_on(self, running_time_seconds=0):
        intensity = 100
        await self._set(intensity, running_time_seconds)

    async def set_off(self, running_time_seconds=0):
        intensity = 0
        await self._set(intensity, running_time_seconds)

    async def set_brightness(self, intensity, running_time_seconds=0):
        await self._set(intensity, running_time_seconds)

    async def read_status(self):
        raise NotImplementedError

    @property
    def brightness(self):
        return self._brightness

    @property
    def is_on(self):
        if self._brightness == 0:
            return False
        else:
            return True

    async def _set(self, intensity, running_time_seconds):
        self._brightness = intensity

        running_time_minutes = 0

        telegram = Telegram()
        telegram.target_address = self._device_address
        telegram.payload = self._integer__list_to_hex(
            [self._channel, intensity, running_time_minutes, running_time_seconds])
        telegram.target_address = self._device_address
        telegram.operate_code_hex = OperateCode.SingleChannelLightingControl.value

        # When we have sent the command we should wait for the response via callback and set
        # the properties regarding state
        # DeviceCallback

        await self._buspro.network_interface.send_telegram(telegram)

    @staticmethod
    def _integer__list_to_hex(list_):
        hex_ = bytearray(list_)
        return hex_
