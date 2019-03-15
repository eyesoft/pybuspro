"""
This component provides sensor support for Buspro.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/...
"""

import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.climate import (PLATFORM_SCHEMA, ClimateDevice)
from homeassistant.components.climate.const import (SUPPORT_OPERATION_MODE, SUPPORT_TARGET_TEMPERATURE, STATE_HEAT)
from homeassistant.const import (CONF_NAME, CONF_DEVICES, CONF_ADDRESS, TEMP_CELSIUS, ATTR_TEMPERATURE, STATE_OFF)
from homeassistant.core import callback

# from homeassistant.helpers.entity import Entity
from ..buspro import DATA_BUSPRO
# noinspection PyUnresolvedReferences
from pybuspro.devices.climate import ControlFloorHeatingStatus
# noinspection PyUnresolvedReferences
from pybuspro.helpers.enums import OnOffStatus

_LOGGER = logging.getLogger(__name__)

CONF_SUPPORTS_OPERATION_MODE = "supports_operation_mode"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_DEVICES):
        vol.All(cv.ensure_list, [
            vol.All({
                vol.Required(CONF_ADDRESS): cv.string,
                vol.Required(CONF_NAME): cv.string,
                vol.Optional(CONF_SUPPORTS_OPERATION_MODE, default=True): cv.boolean,
            })
        ])
})


# noinspection PyUnusedLocal
async def async_setup_platform(hass, config, async_add_entites, discovery_info=None):
    """Set up Buspro switch devices."""
    # noinspection PyUnresolvedReferences
    from pybuspro.devices import Climate

    hdl = hass.data[DATA_BUSPRO].hdl
    devices = []

    for device_config in config[CONF_DEVICES]:
        address = device_config[CONF_ADDRESS]
        name = device_config[CONF_NAME]
        supports_operation_mode = device_config[CONF_SUPPORTS_OPERATION_MODE]

        address2 = address.split('.')
        device_address = (int(address2[0]), int(address2[1]))

        _LOGGER.debug("Adding climate '{}' with address {}".format(name, device_address))

        climate = Climate(hdl, device_address, name)

        devices.append(BusproClimate(hass, climate, supports_operation_mode))

    async_add_entites(devices)


# noinspection PyAbstractClass
class BusproClimate(ClimateDevice):
    """Representation of a Buspro switch."""

    def __init__(self, hass, device, supports_operation_mode):
        self._hass = hass
        self._device = device
        self._target_temperature = self._device.target_temperature
        self._is_on = self._device.is_on
        self._supports_operation_mode = supports_operation_mode
        self.async_register_callbacks()

    @callback
    def async_register_callbacks(self):
        """Register callbacks to update hass after device was changed."""

        # noinspection PyUnusedLocal
        async def after_update_callback(device):
            """Call after device was updated."""
            self._target_temperature = device.target_temperature
            self._is_on = device.is_on
            await self.async_update_ha_state()

        self._device.register_device_updated_cb(after_update_callback)

    @property
    def supported_features(self):
        """Return the list of supported features."""
        support = SUPPORT_TARGET_TEMPERATURE
        if self._supports_operation_mode:
            support |= SUPPORT_OPERATION_MODE
        return support

    @property
    def should_poll(self):
        """No polling needed within Buspro."""
        return False

    @property
    def name(self):
        """Return the display name of this light."""
        return self._device.name

    @property
    def available(self):
        """Return True if entity is available."""
        return self._hass.data[DATA_BUSPRO].connected

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._device.temperature

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        target_temperature = self._target_temperature
        if target_temperature is None:
            target_temperature = self._device.target_temperature

        return target_temperature

    @property
    def current_operation(self):
        """Return current operation."""
        is_on = self._is_on
        if is_on is None:
            is_on = self._device.is_on

        if is_on:
            return STATE_HEAT
        else:
            return STATE_OFF

    @property
    def operation_list(self):
        """List of available operation modes."""
        return [STATE_HEAT, STATE_OFF]

    @property
    def target_temperature_step(self):
        """Return the supported step of target temperature."""
        return 1

    async def async_set_operation_mode(self, operation_mode):
        """Set operation mode."""

        if operation_mode == STATE_HEAT:
            self._is_on = True
            climate_control = ControlFloorHeatingStatus()
            climate_control.status = OnOffStatus.ON.value
            await self._device.control_heating_status(climate_control)
            await self.async_update_ha_state()

        elif operation_mode == STATE_OFF:
            self._is_on = False
            climate_control = ControlFloorHeatingStatus()
            climate_control.status = OnOffStatus.OFF.value
            await self._device.control_heating_status(climate_control)
            await self.async_update_ha_state()

        else:
            _LOGGER.error("Unrecognized operation mode: %s", operation_mode)
            return

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return

        self._target_temperature = temperature
        climate_control = ControlFloorHeatingStatus()
        climate_control.normal_temperature = int(temperature)
        await self._device.control_heating_status(climate_control)

        await self.async_update_ha_state()
