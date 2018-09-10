from .device import Device
from ..core.telegram import Telegram
from ..helpers.enums import *


class Scene(Device):
    def __init__(self, buspro, device_address, name):
        super().__init__(buspro, device_address, name)
        # device_address = (subnet_id, device_id, area_number, scene_number)

        self._device_address = device_address[:2]
        _, _, self._area_number, self._scene_number = device_address
        self.register_telegram_received_cb(self._telegram_received_cb)
        # self._call_read_current_status_of_channels(run_from_init=True)

    def _telegram_received_cb(self, telegram):
        '''
        if telegram.operate_code == OperateCode.SingleChannelControlResponse:
            channel, success, brightness = tuple(telegram.payload)
            if channel == self._channel:
                self._brightness = brightness
                self.call_device_updated()
        elif telegram.operate_code == OperateCode.ReadStatusOfChannelsResponse:
            if self._channel <= telegram.payload[0]:
                self._brightness = telegram.payload[self._channel]
                self.call_device_updated()
        '''

        # Litt usikker på dette kallet
        if telegram.operate_code == OperateCode.SceneControlResponse:
            self._call_read_current_status_of_channels()

    async def run(self):
        telegram = Telegram()
        telegram.target_address = self._device_address
        telegram.payload = [self._area_number, self._scene_number]
        telegram.operate_code = OperateCode.SceneControl

        await self.send_telegram(telegram)
