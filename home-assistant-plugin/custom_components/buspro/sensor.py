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
                                 ILLUMINANCE, TEMPERATURE, CONF_DEVICE_CLASS, CONF_SCAN_INTERVAL)
from homeassistant.core import callback
from homeassistant.helpers.entity import Entity

from ..buspro import DATA_BUSPRO

# from homeassistant.helpers.update_coordinator import (
#     CoordinatorEntity,
#     DataUpdateCoordinator,
#     UpdateFailed,
# )
# from datetime import timedelta

DEFAULT_CONF_UNIT_OF_MEASUREMENT = ""
DEFAULT_CONF_DEVICE_CLASS = "None"
DEFAULT_CONF_SCAN_INTERVAL = "None"
CONF_DEVICE = "device"

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES = {
    ILLUMINANCE,
    TEMPERATURE,
}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_DEVICES):
        vol.All(cv.ensure_list, [
            vol.All({
                vol.Required(CONF_ADDRESS): cv.string,
                vol.Required(CONF_NAME): cv.string,
                vol.Required(CONF_TYPE): vol.In(SENSOR_TYPES),
                vol.Optional(CONF_UNIT_OF_MEASUREMENT, default=DEFAULT_CONF_UNIT_OF_MEASUREMENT): cv.string,
                vol.Optional(CONF_DEVICE_CLASS, default=DEFAULT_CONF_DEVICE_CLASS): cv.string,
                vol.Optional(CONF_DEVICE, default=None): cv.string,
                vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_CONF_SCAN_INTERVAL): cv.string,
            })
        ])
})


# noinspection PyUnusedLocal
async def async_setup_platform(hass, config, async_add_entites, discovery_info=None):
    """Set up Buspro switch devices."""
    # noinspection PyUnresolvedReferences
    from ..pybuspro.devices import Sensor

    hdl = hass.data[DATA_BUSPRO].hdl
    devices = []

    for device_config in config[CONF_DEVICES]:
        address = device_config[CONF_ADDRESS]
        name = device_config[CONF_NAME]
        sensor_type = device_config[CONF_TYPE]
        unit_of_measurement = device_config[CONF_UNIT_OF_MEASUREMENT]
        device_class = device_config[CONF_DEVICE_CLASS]
        device = device_config[CONF_DEVICE]
        scan_interval = device_config[CONF_SCAN_INTERVAL]

        address2 = address.split('.')
        device_address = (int(address2[0]), int(address2[1]))

        _LOGGER.debug("Adding sensor '{}' with address {}, sensor type '{}' and device_class '{}'".format(
            name, device_address, sensor_type, device_class))

        sensor = Sensor(hdl, device_address, device=device, name=name)

        # async def async_update_data():
        #     # sensor.read_sensor_status()
        #     _LOGGER.info("async_update_data called...read_sensor_status")

        # coordinator = DataUpdateCoordinator(
        #     hass, _LOGGER, name=name,
        #     update_method=async_update_data(sensor),
        #     update_interval=timedelta(seconds=scan_interval)
        # )
        # await coordinator.async_config_entry_first_refresh()
        # await coordinator.async_refresh()

        devices.append(BusproSensor(hass, sensor, sensor_type, unit_of_measurement, device_class))

    async_add_entites(devices)


# noinspection PyAbstractClass
class BusproSensor(Entity):
    """Representation of a Buspro switch."""

    def __init__(self, hass, device, sensor_type, unit_of_measurement, device_class, scan_interval):
        self._hass = hass
        self._device = device
        self._unit_of_measurement = unit_of_measurement
        self._sensor_type = sensor_type
        self._device_class = device_class
        self.async_register_callbacks()

        self._should_poll = False
        if scan_interval > 0:
            self._should_poll = True

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
        """No polling needed within Buspro unless explicitly set."""
        return self._should_poll

    @property
    def name(self):
        """Return the display name of this light."""
        return self._device.name

    @property
    def available(self):
        """Return True if entity is available."""
        return self._hass.data[DATA_BUSPRO].connected

    @property
    def state(self):
        """Return the state of the sensor."""
        if self._sensor_type == TEMPERATURE:
            return self._device.temperature
        if self._sensor_type == ILLUMINANCE:
            return self._device.brightness

    @property
    def device_class(self):
        """Return the class of this sensor."""
        return self._device_class

    @property
    def unit_of_measurement(self):
        """Return the unit this state is expressed in."""
        return self._unit_of_measurement

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return None
