from binascii import hexlify

from .device import Device
from ..core.telegram import Telegram
from ..core.enums import *


class Light(Device):
    def __init__(self, buspro, device_address, name):
        super().__init__(buspro, device_address, name)

        # self._device_address = device_address
        self._device_address = device_address[:2]
        _, _, self._channel = device_address
        # self._buspro = buspro
        # self._state = False
        self._brightness = 0
        # self._support_brightness = True
        self.register_telegram_received_cb(self.telegram_received_cb)

    def telegram_received_cb(self, telegram):
        print(f"Telegram received: {telegram}")

        if telegram.operate_code == OperateCode.SingleChannelControlResponse:
            channel, success, brightness = tuple(telegram.payload)
            if channel == self._channel:
                print(f"## SINGLE CHANNEL RESPONSE: {brightness}")
                self._brightness = brightness



        elif telegram.operate_code == OperateCode.ReadStatusOfChannelsResponse:
            if self._channel <= telegram.payload[0]:
                brightness_2 = telegram.payload[self._channel]
                print(f"## READ STATUS RESPONSE: {brightness_2}")
                self._brightness = brightness_2

    def telegram_received_cb_2(self, telegram):
        if telegram.operate_code == OperateCode.SingleChannelControlResponse:
            channel, success, brightness = tuple(telegram.payload)
            if channel == self._channel:
                # if hex(success) == SuccessOrFailure.Success.value:
                self._brightness = brightness
                # self.device_updated()
                # else:
                #     print("s")

    async def read_current_state(self):
        telegram = Telegram()
        telegram.target_address = self._device_address
        telegram.payload = []
        telegram.operate_code = OperateCode.ReadStatusOfChannels
        await self.send_telegram(telegram)

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

        running_time_minutes = 0

        telegram = Telegram()
        telegram.target_address = self._device_address
        telegram.payload = [self._channel, intensity, running_time_minutes, running_time_seconds]
        telegram.operate_code = OperateCode.SingleChannelControl

        await self.send_telegram(telegram)

    '''
    @staticmethod
    def _integer_list_to_hex(list_):
        hex_ = bytearray(list_)
        return hex_
    '''
