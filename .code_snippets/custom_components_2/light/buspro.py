"""
This component provides light support for Buspro.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/...
"""

import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from homeassistant.components.light import Light, PLATFORM_SCHEMA, SUPPORT_BRIGHTNESS, ATTR_BRIGHTNESS
from homeassistant.const import (CONF_NAME, CONF_DEVICES, CONF_API_KEY, CONF_HOST, CONF_PORT)

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'buspro'



DEVICE_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME): cv.string,
})

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_DEVICES): {cv.string: DEVICE_SCHEMA}, 
 })

 
 

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up Buspro light devices."""
    _LOGGER.info("starting setup_platform")
   
    data = hass.data[DOMAIN]
    devices = []
   
    for address, device_config in config[CONF_DEVICES].items():
        name = device_config[CONF_NAME]
        _LOGGER.info(f"Appending light with name '{name}' and address '{address}'")
        devices.append(BusproLight(name))
        
    add_devices(devices)
   
   

   
class BusproLight(Light):
    """Representation of a Buspro light."""

    def __init__(self, name):
        """Initialize a BusproLight."""
        self._brightness = 0
        self._supported_features = SUPPORT_BRIGHTNESS
        self._name = name
        self._state = False
     
    # @callback
    # def async_register_callbacks(self):
        # """Register callbacks to update hass after device was changed."""
        # async def after_update_callback(device):
            # """Call after device was updated."""
            # await self.async_update_ha_state()
        # self.device.register_device_updated_cb(after_update_callback)     
     
    @property
    def should_poll(self):
        """No polling needed within Buspro."""
        return False
        
    @property
    def name(self):
        """Return the display name of this light."""
        return self._name

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._state

    @property
    def brightness(self):
        """Return the brightness of the light."""
        return self._brightness

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_BRIGHTNESS
     
    def turn_on(self, **kwargs):
        """Turn on the light."""
        self._brightness = kwargs.get(ATTR_BRIGHTNESS, 255)
        self._state = True
        _LOGGER.info("turn_on() is called")

    def turn_off(self, **kwargs):
        """Turn off the light."""
        self._state = False
        self._brightness = 0
        _LOGGER.info("turn_off() is called")

    # def update(self):
        # """Fetch new state data for this light."""
        # _LOGGER.info("update() is called")
		
