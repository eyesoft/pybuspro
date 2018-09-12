import asyncio

from .control import _ReadFloorHeatingStatus, _ControlFloorHeatingStatus
from .device import Device
from ..helpers.enums import *
from ..helpers.generics import Generics


class ControlFloorHeatingStatus:
    def __init__(self):
        self.temperature_type = None
        self.status = None
        self.mode = None
        self.normal_temperature = None
        self.day_temperature = None
        self.night_temperature = None
        self.away_temperature = None


class Climate(Device):
    def __init__(self, buspro, device_address, name=""):
        super().__init__(buspro, device_address, name)

        self._buspro = buspro
        self._device_address = device_address

        self._temperature_type = None
        self._status = None
        self._mode = None
        self._current_temperature = None
        self._normal_temperature = None
        self._day_temperature = None
        self._night_temperature = None
        self._away_temperature = None

        self.register_telegram_received_cb(self._telegram_received_cb)
        self._call_read_current_heating_status(run_from_init=True)

    def _telegram_received_cb(self, telegram):
        if telegram.operate_code == OperateCode.ReadFloorHeatingStatusResponse:
            self._temperature_type, self._current_temperature, self._status, self._mode, self._normal_temperature, \
                self._day_temperature, self._night_temperature, self._away_temperature = tuple(telegram.payload)

            self._call_device_updated()

        elif telegram.operate_code == OperateCode.ControlFloorHeatingStatusResponse:
            success_or_fail, self._temperature_type, self._status, self._mode, self._normal_temperature, \
                self._day_temperature, self._night_temperature, self._away_temperature = tuple(telegram.payload)

            if success_or_fail == SuccessOrFailure.Success:
                self._call_device_updated()

    async def read_heating_status(self):
        rfhs = _ReadFloorHeatingStatus(self._buspro)
        rfhs.subnet_id, rfhs.device_id = self._device_address
        await rfhs.send()

    def _telegram_received_control_heating_status_cb(self, telegram, floor_heating_status):

        if telegram.operate_code == OperateCode.ReadFloorHeatingStatusResponse:
            self.unregister_telegram_received_cb(
                self._telegram_received_control_heating_status_cb, floor_heating_status)

            temperature_type, current_temperature, status, mode, normal_temperature, day_temperature, night_temperature, \
                away_temperature = tuple(telegram.payload)

            if hasattr(floor_heating_status, 'temperature_type'):
                if floor_heating_status.temperature_type is not None:
                    temperature_type = floor_heating_status.temperature_type
            if hasattr(floor_heating_status, 'status'):
                if floor_heating_status.status is not None:
                    status = floor_heating_status.status
            if hasattr(floor_heating_status, 'mode'):
                if floor_heating_status.mode is not None:
                    mode = floor_heating_status.mode
            if hasattr(floor_heating_status, 'normal_temperature'):
                if floor_heating_status.normal_temperature is not None:
                    normal_temperature = floor_heating_status.normal_temperature
            if hasattr(floor_heating_status, 'day_temperature'):
                if floor_heating_status.day_temperature is not None:
                    day_temperature = floor_heating_status.day_temperature
            if hasattr(floor_heating_status, 'night_temperature'):
                if floor_heating_status.night_temperature is not None:
                    night_temperature = floor_heating_status.night_temperature
            if hasattr(floor_heating_status, 'away_temperature'):
                if floor_heating_status.away_temperature is not None:
                    away_temperature = floor_heating_status.away_temperature

            cfhs_ = _ControlFloorHeatingStatus(self._buspro)
            cfhs_.subnet_id, cfhs_.device_id = self._device_address
            cfhs_.temperature_type = temperature_type
            cfhs_.status = status
            cfhs_.mode = mode
            cfhs_.normal_temperature = normal_temperature
            cfhs_.day_temperature = day_temperature
            cfhs_.night_temperature = night_temperature
            cfhs_.away_temperature = away_temperature

            async def send_control_floor_heating_status(cfhs__):
                await cfhs__.send()

            asyncio.ensure_future(send_control_floor_heating_status(cfhs_), loop=self._buspro.loop)

    async def control_heating_status(self, floor_heating_status: ControlFloorHeatingStatus):
        self.register_telegram_received_cb(self._telegram_received_control_heating_status_cb, floor_heating_status)
        rfhs = _ReadFloorHeatingStatus(self._buspro)
        rfhs.subnet_id, rfhs.device_id = self._device_address
        await rfhs.send()

    def _call_read_current_heating_status(self, run_from_init=False):

        async def read_current_heating_status():
            if run_from_init:
                await asyncio.sleep(1)

            rfhs = _ReadFloorHeatingStatus(self._buspro)
            rfhs.subnet_id, rfhs.device_id = self._device_address
            await rfhs.send()

        asyncio.ensure_future(read_current_heating_status(), loop=self._buspro.loop)

    @property
    def unit_of_measurement(self):
        generics = Generics()
        return generics.get_enum_value(TemperatureType, self._temperature_type)

    @property
    def is_on(self):
        if self._status == 1:
            return True
        else:
            return False

    @property
    def mode(self):
        return self._mode

    @property
    def temperature(self):
        return self._current_temperature

    @property
    def day_temperature(self):
        return self._day_temperature

    @property
    def night_temperature(self):
        return self._night_temperature

    @property
    def away_temperature(self):
        return self._away_temperature
