"""
This component provides light support for Buspro.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/...
"""

import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.light import Light, PLATFORM_SCHEMA, SUPPORT_BRIGHTNESS, ATTR_BRIGHTNESS
from homeassistant.const import (CONF_NAME, CONF_DEVICES)
from homeassistant.core import callback

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'buspro'

DEVICE_SCHEMA = vol.Schema({
    vol.Optional("running_time", default=0): cv.string,
    vol.Required(CONF_NAME): cv.string,
})

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional("running_time", default=0): cv.string,
    vol.Required(CONF_DEVICES): {cv.string: DEVICE_SCHEMA},
})


# noinspection PyUnusedLocal
def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up Buspro light devices."""
    # noinspection PyUnresolvedReferences
    from ..pybuspro.devices import Light

    # _LOGGER.info("starting setup_platform")

    hdl = hass.data[DOMAIN].hdl
    devices = []

    platform_delay_time = int(config["running_time"])

    for address, device_config in config[CONF_DEVICES].items():
        name = device_config[CONF_NAME]
        device_delay_time = int(device_config["running_time"])

        if device_delay_time == 0:
            device_delay_time = platform_delay_time

        adress2 = address.split('.')
        device_address = (int(adress2[0]), int(adress2[1]), int(adress2[2]))
        # _LOGGER.info(f"Appending light with name '{name}' and address '{device_address}'")

        light = Light(hdl, device_address, name)

        devices.append(BusproLight(hass, light, device_delay_time))

    add_devices(devices)


# noinspection PyAbstractClass
class BusproLight(Light):
    """Representation of a Buspro light."""

    def __init__(self, hass, device, delay_time):
        self._hass = hass
        self._device = device
        self._state = False
        self._brightness = 0
        self._delay_time = delay_time
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
    def brightness(self):
        """Return the brightness of the light."""
        brightness = self._device.current_brightness / 100 * 255
        return brightness

    @property
    def supported_features(self):
        """Flag supported features."""
        flags = 0
        if self._device.supports_brightness:
            flags |= SUPPORT_BRIGHTNESS
        return flags

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._device.is_on

    async def async_turn_on(self, **kwargs):
        """Instruct the light to turn on."""
        self._state = True
        brightness = int(kwargs.get(ATTR_BRIGHTNESS, 255) / 255 * 100)
        self._brightness = kwargs.get(ATTR_BRIGHTNESS, 255)
        await self._device.set_brightness(brightness, self._delay_time)
        # _LOGGER.info("turn_on() is called")

    async def async_turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        self._brightness = 0
        self._state = False
        await self._device.set_off(self._delay_time)
