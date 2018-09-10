from .device import Device
from ..core.telegram import Telegram
from ..helpers.enums import *
from ..helpers.generics import Generics


class Light(Device):
    def __init__(self, buspro, device_address, name):
        super().__init__(buspro, device_address, name)

        self._device_address = device_address[:2]
        _, _, self._channel = device_address
        self._brightness = 0
        self.register_telegram_received_cb(self.telegram_received_cb)
        self._call_read_current_status_of_channels(run_in_init=True)

    def telegram_received_cb(self, telegram):
        if telegram.operate_code == OperateCode.SingleChannelControlResponse:
            channel, success, brightness = tuple(telegram.payload)
            if channel == self._channel:
                self._brightness = brightness
                self.call_device_updated()
        elif telegram.operate_code == OperateCode.ReadStatusOfChannelsResponse:
            if self._channel <= telegram.payload[0]:
                brightness_2 = telegram.payload[self._channel]
                self._brightness = brightness_2
                self.call_device_updated()
        elif telegram.operate_code == OperateCode.SceneControlResponse:
            self._call_read_current_status_of_channels()

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
        return True

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

        generics = Generics()
        (minutes, seconds) = generics.calculate_minutes_seconds(running_time_seconds)

        telegram = Telegram()
        telegram.target_address = self._device_address
        telegram.payload = [self._channel, intensity, minutes, seconds]
        telegram.operate_code = OperateCode.SingleChannelControl

        await self.send_telegram(telegram)
