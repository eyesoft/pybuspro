"""
This component provides light support for Buspro.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/...
"""

import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from homeassistant.core import callback
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

 
 

async def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    """Set up Buspro light devices."""
    _LOGGER.info("starting setup_platform")
   
    bus = hass.data[DOMAIN]
    devices = []
   
    for address, device_config in config[CONF_DEVICES].items():
        name = device_config[CONF_NAME]
        _LOGGER.info(f"Appending light with name '{name}' and address '{address}' -- {bus.value}")
        devices.append(BusproLight(name, bus))
        
    async_add_devices(devices)
   
   
   
   
   

   
class BusproLight(Light):
    """Representation of a Buspro light."""

    def __init__(self, name, bus):
        """Initialize a BusproLight."""
        self._brightness = 0
        self._supported_features = SUPPORT_BRIGHTNESS
        self._name = name
        self._state = False
        self._bus = bus
        self._light = None
        #self._api = api
        
        light = bus
        self._refresh(light)

        
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

        
        
        
    def _refresh(self, light):
        """Refresh the light data."""
        self._light = light

        # Caching of LightControl and light object
        # self._available = light.reachable
        # self._light_control = light.light_control
        # self._light_data = light.light_control.lights[0]
        # self._name = light.name
        # self._features = SUPPORTED_FEATURES

        
        
        
    async def async_added_to_hass(self):
        _LOGGER.info("__async_added_to_hass_____________________")
        self._async_start_observe()
        
    @callback
    def _async_start_observe(self, exc=None):
        # """Start observation of light."""
        cmd = self._light.observe(callback=self._observe_update, err_callback=self._async_start_observe, duration=0)
        #self.hass.async_add_job(self._api(cmd))
        
    @callback
    def _observe_update(self, tradfri_device):
        # """Receive new state data for this light."""
        self._refresh(tradfri_device)
        self.async_schedule_update_ha_state()        
        

        
        
        
        
        
    # async def async_update(self):
        # _LOGGER.info("UPDATE IS CALLED")
        
        
    #def update(self):
        # BLIR IKKE KALT DERSOM should_poll = FALSE
        # """Fetch new state data for this light."""
        #_LOGGER.info("UPDATE IS CALLED")
		
