"""
Support for Buspro devices.

For more details about this component, please refer to the documentation at
https://home-assistant.io/...
"""

import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from homeassistant.const import (CONF_HOST, CONF_PORT, CONF_NAME)
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




def setup(hass, config):
    """Setup the Buspro component. """

    host = config[DOMAIN][CONF_HOST]
    port = config[DOMAIN][CONF_PORT]
    name = config[DOMAIN][CONF_NAME]

    hass.data[DOMAIN] = "<buspro>"
    
    #load_platform(hass, 'light', DOMAIN, {'optional': 'arguments'})
    #load_platform(hass, 'light', DOMAIN, busprodevice, config)
    
    # Added via configuration.yaml light:
    #load_platform(hass, 'light', DOMAIN)
    
    load_platform(hass, 'sensor', DOMAIN)

    _LOGGER.info(f"Listening on {host}:{port} with alias '{name}'")

    return True

