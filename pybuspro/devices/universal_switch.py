import asyncio

from .control import _UniversalSwitch, _ReadStatusOfUniversalSwitch
from .device import Device
from ..helpers.enums import *


class UniversalSwitch(Device):
    def __init__(self, buspro, device_address, name):
        super().__init__(buspro, device_address, name)
        # device_address = (subnet_id, device_id, channel_number)

        self._buspro = buspro
        self._device_address = device_address[:2]
        _, _, self._switch_number = device_address
        self._switch_status = SwitchStatusOnOff.OFF
        self.register_telegram_received_cb(self._telegram_received_cb)
        self._call_read_current_status_of_universal_switch(run_from_init=True)

    def _telegram_received_cb(self, telegram):
        if telegram.operate_code == OperateCode.UniversalSwitchControlResponse:
            switch_number, switch_status = tuple(telegram.payload)
            if switch_number == self._switch_number:
                self._switch_status = switch_status
                self._call_device_updated()
        elif telegram.operate_code == OperateCode.ReadStatusOfUniversalSwitchResponse:
            if self._switch_number <= telegram.payload[0]:
                self._switch_status = telegram.payload[1]
                self._call_device_updated()

    async def set_on(self):
        await self._set(SwitchStatusOnOff.ON)

    async def set_off(self):
        await self._set(SwitchStatusOnOff.OFF)

    async def read_status(self):
        raise NotImplementedError

    @property
    def is_on(self):
        if self._switch_status == SwitchStatusOnOff.OFF:
            return False
        else:
            return True

    async def _set(self, switch_status):
        self._switch_status = switch_status

        us = _UniversalSwitch(self._buspro)
        us.subnet_id, us.device_id = self._device_address
        us.switch_number = self._switch_number
        us.switch_status = self._switch_status
        await us.send()

    def _call_read_current_status_of_universal_switch(self, run_from_init=False):

        async def read_current_state_of_universal_switch():
            if run_from_init:
                await asyncio.sleep(1)

            read_status_of_universal_switch = _ReadStatusOfUniversalSwitch(self._buspro)
            read_status_of_universal_switch.subnet_id, read_status_of_universal_switch.device_id = self._device_address
            read_status_of_universal_switch.switch_number = self._switch_number
            await read_status_of_universal_switch.send()

        asyncio.ensure_future(read_current_state_of_universal_switch(), loop=self._buspro.loop)
