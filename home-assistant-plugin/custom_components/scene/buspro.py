"""
This component provides scene support for Buspro.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/...
"""

import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.scene import Scene, CONF_PLATFORM
from homeassistant.const import CONF_NAME
# from homeassistant.core import callback

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'buspro'

CONF_ADDRESS = 'address'
CONF_SCENE_NUMBER = 'scene_number'

DEFAULT_NAME = 'BUSPRO SCENE'

'''
DEVICE_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME): cv.string,
})

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_DEVICES): {cv.string: DEVICE_SCHEMA},
})
'''

PLATFORM_SCHEMA = vol.Schema({
    vol.Required(CONF_PLATFORM): 'buspro',
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_ADDRESS): cv.string,
    vol.Required(CONF_SCENE_NUMBER): cv.string
})


# noinspection PyUnusedLocal
def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up Buspro scene devices."""
    # noinspection PyUnresolvedReferences
    from ..pybuspro.devices import Scene

    hdl = hass.data[DOMAIN].hdl
    # devices = []

    name = config.get(CONF_NAME)
    address = config.get(CONF_ADDRESS).split('.')
    scene_number = config.get(CONF_SCENE_NUMBER).split('.')
    device_address = (int(address[0]), int(address[1]), int(scene_number[0]), int(scene_number[1]))

    _LOGGER.info("Appending scene with name '{}' and address '{}'".format(name, device_address))
    scene = Scene(hdl, device_address, name)
    add_devices([BusproScene(scene)])


# noinspection PyAbstractClass
class BusproScene(Scene):
    """Representation of a Buspro switch."""

    def __init__(self, device):
        self._device = device
        # self.async_register_callbacks()

    '''
    @callback
    def async_register_callbacks(self):
        """Register callbacks to update hass after device was changed."""

        # noinspection PyUnusedLocal
        async def after_update_callback(device):
            """Call after device was updated."""
            await self.async_update_ha_state()

        self._device.register_device_updated_cb(after_update_callback)
    '''

    @property
    def name(self):
        """Return the display name of this light."""
        return self._device.name

    async def async_activate(self):
        """Instruct the switch to turn off."""
        await self._device.run()
