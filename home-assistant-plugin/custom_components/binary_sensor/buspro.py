"""
This component provides binary sensor support for Buspro.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/...
"""

import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.binary_sensor import (PLATFORM_SCHEMA, BinarySensorDevice)
from homeassistant.const import (CONF_NAME, CONF_DEVICES, CONF_ADDRESS, CONF_TYPE, CONF_DEVICE_CLASS)
from homeassistant.core import callback

from ..buspro import DATA_BUSPRO

_LOGGER = logging.getLogger(__name__)

DEFAULT_CONF_DEVICE_CLASS = "None"

CONF_MOTION = 'motion'
CONF_DRY_CONTACT_1 = 'dry_contact_1'
CONF_DRY_CONTACT_2 = 'dry_contact_2'
CONF_UNIVERSAL_SWITCH = 'universal_switch'
CONF_SINGLE_CHANNEL = 'single_channel'

SENSOR_TYPES = {
    CONF_MOTION,
    CONF_DRY_CONTACT_1,
    CONF_DRY_CONTACT_2,
    CONF_UNIVERSAL_SWITCH,
    CONF_SINGLE_CHANNEL,
}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_DEVICES):
        vol.All(cv.ensure_list, [
            vol.All({
                vol.Required(CONF_ADDRESS): cv.string,
                vol.Required(CONF_NAME): cv.string,
                vol.Required(CONF_TYPE): vol.In(SENSOR_TYPES),
                vol.Optional(CONF_DEVICE_CLASS, default=DEFAULT_CONF_DEVICE_CLASS): cv.string,
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
        device_class = device_config[CONF_DEVICE_CLASS]
        universal_switch_number = None
        channel_number = None

        address2 = address.split('.')
        device_address = (int(address2[0]), int(address2[1]))

        if sensor_type == CONF_UNIVERSAL_SWITCH:
            universal_switch_number = int(address2[2])
            _LOGGER.debug("Adding binary sensor '{}' with address {}, universal_switch_number {}, sensor type '{}' "
                          "and device class '{}'".format(name, device_address, universal_switch_number, sensor_type,
                                                         device_class))
        elif sensor_type == CONF_SINGLE_CHANNEL:
            channel_number = int(address2[2])
            _LOGGER.debug("Adding binary sensor '{}' with address {}, channel_number {}, sensor type '{}' and "
                          "device class '{}'".format(name, device_address, channel_number, sensor_type, device_class))
        else:
            _LOGGER.debug("Adding binary sensor '{}' with address {}, sensor type '{}' and device class '{}'".
                          format(name, device_address, sensor_type, device_class))

        sensor = Sensor(hdl, device_address, universal_switch_number=universal_switch_number,
                        channel_number=channel_number, name=name, delay_read_current_state_seconds=1)

        devices.append(BusproBinarySensor(hass, sensor, sensor_type, device_class))

    async_add_entites(devices)


# noinspection PyAbstractClass
class BusproBinarySensor(BinarySensorDevice):
    """Representation of a Buspro switch."""

    def __init__(self, hass, device, sensor_type, device_class):
        self._hass = hass
        self._device = device
        self._device_class = device_class
        self._sensor_type = sensor_type
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
        return self._hass.data[DATA_BUSPRO].connected

    @property
    def device_class(self):
        """Return the class of this sensor."""
        return self._device_class

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        if self._sensor_type == CONF_MOTION:
            # _LOGGER.info("----> {}".format(self._device.movement))
            return self._device.movement
        if self._sensor_type == CONF_DRY_CONTACT_1:
            # _LOGGER.info("----> {}".format(self._device.dry_contact_1_is_on))
            return self._device.dry_contact_1_is_on
        if self._sensor_type == CONF_DRY_CONTACT_2:
            return self._device.dry_contact_2_is_on
        if self._sensor_type == CONF_UNIVERSAL_SWITCH:
            return self._device.universal_switch_is_on
        if self._sensor_type == CONF_SINGLE_CHANNEL:
            return self._device.single_channel_is_on
