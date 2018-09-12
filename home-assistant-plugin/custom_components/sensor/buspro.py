"""
This component provides sensor support for Buspro.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/...
"""

import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (CONF_NAME, CONF_DEVICES, CONF_ADDRESS, CONF_TYPE, CONF_UNIT_OF_MEASUREMENT,
                                 DEVICE_CLASS_ILLUMINANCE, DEVICE_CLASS_TEMPERATURE)
from homeassistant.core import callback
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'buspro'

SENSOR_TYPES = {
    DEVICE_CLASS_ILLUMINANCE,
    DEVICE_CLASS_TEMPERATURE,
}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_DEVICES):
        vol.All(cv.ensure_list, [
            vol.All({
                vol.Required(CONF_ADDRESS): cv.string,
                vol.Required(CONF_NAME): cv.string,
                vol.Required(CONF_TYPE): vol.In(SENSOR_TYPES),
                vol.Optional(CONF_UNIT_OF_MEASUREMENT, default=''): cv.string,
            })
        ])
})


# noinspection PyUnusedLocal
def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up Buspro switch devices."""
    # noinspection PyUnresolvedReferences
    from ..pybuspro.devices import Sensor

    hdl = hass.data[DOMAIN].hdl
    devices = []

    for device_config in config[CONF_DEVICES]:
        address = device_config[CONF_ADDRESS]
        name = device_config[CONF_NAME]
        sensor_type = device_config[CONF_TYPE]

        address2 = address.split('.')
        device_address = (int(address2[0]), int(address2[1]))

        _LOGGER.info("Adding sensor with name '{}', address {} and sensor type '{}'".format(
            name, device_address, sensor_type))

        sensor = Sensor(hdl, device_address, sensor_type, name)

        devices.append(BusproSensor(hass, sensor))

    add_devices(devices)


# noinspection PyAbstractClass
class BusproSensor(Entity):
    """Representation of a Buspro switch."""

    def __init__(self, hass, device):
        self._hass = hass
        self._device = device
        self.async_register_callbacks()

    @callback
    def async_register_callbacks(self):
        """Register callbacks to update hass after device was changed."""

        # noinspection PyUnusedLocal
        async def after_update_callback(device):
            """Call after device was updated."""
            await self.async_update_ha_state()

        self._device.register_device_updated_cb(after_update_callback)

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
        return self._hass.data[DOMAIN].connected

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._device.resolve_state()

    @property
    def unit_of_measurement(self):
        """Return the unit this state is expressed in."""
        return self._device.unit_of_measurement()

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return None
