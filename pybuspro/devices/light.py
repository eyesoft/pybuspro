from .device import Device
from ..core.telegram import Telegram
from ..core.enums import OperateCode, DeviceType


class Light(Device):
    def __init__(self, buspro, device_address, name):
        super().__init__(buspro, device_address, name)

        self._device_address = device_address
        self._device_address = device_address[:2]
        _, _, self._channel = device_address
        self._buspro = buspro
        self._state = False
        self._brightness = 0
        self._support_brightness = True

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
    def supports_brightness(self):
        return self._support_brightness

    @property
    def current_brightness(self):
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

        operate_code = OperateCode.SingleChannelLightingControl
        source_device_type = DeviceType.PyBusPro

        telegram = Telegram()
        telegram.target_address = self._device_address
        telegram.payload = [self._channel, intensity, running_time_minutes, running_time_seconds]
        # telegram.operate_code_hex = OperateCode.SingleChannelLightingControl.value
        telegram.operate_code = operate_code
        telegram.source_device_type = source_device_type

        # When we have sent the command we should wait for the response via callback and set
        # the properties regarding state
        # DeviceCallback

        await self.send_telegram(telegram)

    @staticmethod
    def _integer_list_to_hex(list_):
        hex_ = bytearray(list_)
        return hex_
