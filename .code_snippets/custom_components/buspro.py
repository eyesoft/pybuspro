"""
Support for Buspro devices.

For more details about this component, please refer to the documentation at
https://home-assistant.io/...
"""

from uuid import uuid4

import asyncio
import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from homeassistant.const import (CONF_HOST, CONF_PORT, CONF_NAME)
from homeassistant.const import (
    STATE_ALARM_ARMED_AWAY, STATE_ALARM_ARMED_HOME, STATE_ALARM_DISARMED,
    STATE_ALARM_TRIGGERED, EVENT_HOMEASSISTANT_STOP)
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.discovery import load_platform
	
_LOGGER = logging.getLogger(__name__)

DOMAIN = 'buspro'
DEPENDENCIES = []

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
      vol.Required(CONF_HOST): cv.string,
      vol.Required(CONF_PORT): cv.port,
      vol.Optional(CONF_NAME, default=''): cv.string
    })
}, extra=vol.ALLOW_EXTRA)




async def async_setup(hass, config):
    """Setup the Buspro component. """

    _LOGGER.info("STARTING...")
    
    host = config[DOMAIN][CONF_HOST]
    port = config[DOMAIN][CONF_PORT]
    name = config[DOMAIN][CONF_NAME]




    
    
    controller = Hdlbus('192.168.1.15', 6000, hass.loop)
    hass.data[DOMAIN] = controller
   
    result = await controller.connect()
    if not result:
        return False







        
    async def _close():
        controller.close()

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, _close())
    
    _LOGGER.info("CONNECTED...")
    
    #load_platform(hass, 'light', DOMAIN, {'optional': 'arguments'})
    #load_platform(hass, 'light', DOMAIN, busprodevice, config)
    
    # Added via configuration.yaml light:
    #load_platform(hass, 'light', DOMAIN)
    
    load_platform(hass, 'sensor', DOMAIN)

    _LOGGER.info(f"Listening on {host}:{port} with alias '{name}'")

    
    
    # hass.async_create_task(discovery.async_load_platform(
        # hass, 'light', DOMAIN, {'gateway': gateway_id}, hass_config))
    # hass.async_create_task(discovery.async_load_platform(
        # hass, 'sensor', DOMAIN, {'gateway': gateway_id}, hass_config))   
    
    
    
    
    return True

    
    






            
    

    
class Hdlbus:
    
    def __init__(self, ip, port, loop=None):
        self._value = "_value_"
       
    @property
    def value(self):
        return self._value
        
    async def connect(self):
        return True
        
    def close(self):
        return True
        
        
    async def observe(self, callback=None, err_callback=None, duration=0):
        pass
        