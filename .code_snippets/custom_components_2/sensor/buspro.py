"""
This component provides sensor support for Buspro.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/...
"""

import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity

from random import randint

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'buspro'


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up Buspro sensor devices."""
    _LOGGER.info("starting setup_platform")
    
    data = hass.data[DOMAIN]
    devices = []
    
    devices.append(BusproSensor())
    add_entities(devices)
    
    
   

   
class BusproSensor(Entity):
    """Representation of a Buspro light."""

    def __init__(self):
        """Initialize an AwesomeLight."""
        self._state = None
        self._name = "Sensor name"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS
        
    def update(self):
        """Fetch new state data for this light."""
        temp = randint(5, 30)
        self._state = temp
        _LOGGER.info("update() is called")
		
