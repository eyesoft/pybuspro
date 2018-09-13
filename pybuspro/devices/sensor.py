import asyncio

# from ..helpers.generics import Generics
from .control import _ReadSensorStatus, _ReadStatusOfUniversalSwitch, _ReadStatusOfChannels
from .device import Device
from ..helpers.enums import *


class Sensor(Device):
    def __init__(self, buspro, device_address, universal_switch_number=None, channel_number=None, name=""):
        super().__init__(buspro, device_address, name)

        self._buspro = buspro
        self._device_address = device_address
        self._universal_switch_number = universal_switch_number
        self._channel_number = channel_number
        self._name = name

        self._current_temperature = None
        self._brightness = None
        self._motion_sensor = None
        self._sonic = None
        self._dry_contact_1_status = None
        self._dry_contact_2_status = None
        self._universal_switch_status = OnOffStatus.OFF
        self._channel_status = 0

        self.register_telegram_received_cb(self._telegram_received_cb)
        self._call_read_current_status_of_sensor(run_from_init=True)

    def _telegram_received_cb(self, telegram):
        if telegram.operate_code == OperateCode.ReadSensorStatusResponse:
            success_or_fail, self._current_temperature, brightness_high, brightness_low, self._motion_sensor, \
                self._sonic, self._dry_contact_1_status, self._dry_contact_2_status = tuple(telegram.payload)

            if success_or_fail == SuccessOrFailure.Success:
                self._brightness = brightness_high + brightness_low
                self._call_device_updated()

        elif telegram.operate_code == OperateCode.BroadcastSensorStatusResponse:
            self._current_temperature, brightness_high, brightness_low, self._motion_sensor, \
                self._sonic, self._dry_contact_1_status, self._dry_contact_2_status = tuple(telegram.payload)

            self._brightness = brightness_high + brightness_low
            self._call_device_updated()

        elif telegram.operate_code == OperateCode.ReadStatusOfUniversalSwitchResponse:
            _, self._universal_switch_status = tuple(telegram.payload)
            self._call_device_updated()

        elif telegram.operate_code == OperateCode.BroadcastStatusOfUniversalSwitch:
            if self._universal_switch_number <= telegram.payload[0]:
                self._universal_switch_status = telegram.payload[self._universal_switch_number]
                self._call_device_updated()

        elif telegram.operate_code == OperateCode.ReadStatusOfChannelsResponse:
            #print("ReadStatusOfChannelsResponse telegram: {}".format(telegram))
            #print("Channel_number: {}".format(self._channel_number))
            #print("Name: {}".format(self._name))
            if self._channel_number <= telegram.payload[0]:
                self._channel_status = telegram.payload[self._channel_number]
                self._call_device_updated()

        elif telegram.operate_code == OperateCode.SingleChannelControlResponse:
            if self._channel_number == telegram.payload[0]:
                # if telegram.payload[1] == SuccessOrFailure.Success::
                self._channel_status = telegram.payload[2]
                self._call_device_updated()

    async def read_sensor_status(self):
        if self._universal_switch_number is not None:
            rsous = _ReadStatusOfUniversalSwitch(self._buspro)
            rsous.subnet_id, rsous.device_id = self._device_address
            rsous.switch_number = self._universal_switch_number
            await rsous.send()
        elif self._channel_number is not None:
            rsoc = _ReadStatusOfChannels(self._buspro)
            rsoc.subnet_id, rsoc.device_id = self._device_address
            await rsoc.send()
        else:
            rss = _ReadSensorStatus(self._buspro)
            rss.subnet_id, rss.device_id = self._device_address
            await rss.send()

    @property
    def temperature(self):
        if self._current_temperature is None:
            return 0
        return self._current_temperature - 20

    @property
    def brightness(self):
        if self._brightness is None:
            return 0
        return self._brightness

    @property
    def movement(self):
        if self._motion_sensor == 1:
            return True
        else:
            return False

    @property
    def dry_contact_1_is_on(self):
        if self._dry_contact_1_status == 1:
            return True
        else:
            return False

    @property
    def dry_contact_2_is_on(self):
        if self._dry_contact_2_status == 1:
            return True
        else:
            return False

    @property
    def universal_switch_is_on(self):
        if self._universal_switch_status == 1:
            return True
        else:
            return False

    @property
    def single_channel_is_on(self):
        if self._channel_status > 0:
            return True
        else:
            return False

    def _call_read_current_status_of_sensor(self, run_from_init=False):

        async def read_current_status_of_sensor():
            if run_from_init:
                await asyncio.sleep(1)
            await self.read_sensor_status()

        asyncio.ensure_future(read_current_status_of_sensor(), loop=self._buspro.loop)
