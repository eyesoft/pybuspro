"""
Support for Buspro devices.

For more details about this component, please refer to the documentation at
https://home-assistant.io/...
"""

import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.const import (CONF_HOST, CONF_PORT, CONF_NAME)
from homeassistant.const import (
    EVENT_HOMEASSISTANT_STOP)

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'buspro'
DEPENDENCIES = []
GATEWAY_ADDRESS_SEND_RECEIVE = (('192.168.1.15', 6000), ('', 6000))

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_PORT): cv.port,
        vol.Optional(CONF_NAME, default=''): cv.string
    })
}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass, config):
    """Setup the Buspro component. """

    host = config[DOMAIN][CONF_HOST]
    port = config[DOMAIN][CONF_PORT]
    name = config[DOMAIN][CONF_NAME]

    hass.data[DOMAIN] = BusproModule(hass, config)
    await hass.data[DOMAIN].start()

    # load_platform(hass, 'light', DOMAIN, {'optional': 'arguments'})
    # load_platform(hass, 'light', DOMAIN, busprodevice, config)

    # Added via configuration.yaml light:
    # load_platform(hass, 'light', DOMAIN)

    # load_platform(hass, 'sensor', DOMAIN)

    # _LOGGER.info(f"Listening on {host}:{port} with alias '{name}'")

    return True


class BusproModule:
    """Representation of Buspro Object."""

    def __init__(self, hass, config):
        """Initialize of Buspro module."""
        self.hass = hass
        self.config = config
        self.connected = False
        self.init_hdl()

    def init_hdl(self):
        """Initialize of Buspro object."""
        from .pybuspro.buspro import Buspro
        self.hdl = Buspro(GATEWAY_ADDRESS_SEND_RECEIVE, self.hass.loop)
        self.hdl.register_telegram_received_all_messages_cb(self.telegram_received_cb)

    async def start(self):
        """Start Buspro object. Connect to tunneling device."""
        await self.hdl.start(state_updater=False)
        self.hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, self.stop)
        self.connected = True
        # _LOGGER.info(f"Started")

    async def stop(self, event):
        """Stop Buspro object. Disconnect from tunneling device."""
        await self.hdl.stop()

    def telegram_received_cb(self, telegram):
        #     """Call invoked after a KNX telegram was received."""
        #     self.hass.bus.fire('knx_event', {
        #         'address': str(telegram.group_address),
        #         'data': telegram.payload.value
        #     })
        # _LOGGER.info(f"Callback: '{telegram}'")
        return False
