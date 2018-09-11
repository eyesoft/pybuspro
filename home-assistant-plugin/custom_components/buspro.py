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

SERVICE_BUSPRO_SEND = "send"
SERVICE_BUSPRO_ATTR_ADDRESS = "address"
SERVICE_BUSPRO_ATTR_PAYLOAD = "payload"

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_PORT): cv.port,
        vol.Optional(CONF_NAME, default=''): cv.string
    })
}, extra=vol.ALLOW_EXTRA)

SERVICE_BUSPRO_SEND_SCHEMA = vol.Schema({
    vol.Required(SERVICE_BUSPRO_ATTR_ADDRESS): cv.string,
    vol.Required(SERVICE_BUSPRO_ATTR_PAYLOAD): vol.Any(
        cv.positive_int, [cv.positive_int]),
})


async def async_setup(hass, config):
    """Setup the Buspro component. """

    hass.data[DOMAIN] = BusproModule(hass, config)
    await hass.data[DOMAIN].start()

    # load_platform(hass, 'light', DOMAIN, {'optional': 'arguments'})
    # load_platform(hass, 'light', DOMAIN, busprodevice, config)
    # Added via configuration.yaml light:
    # load_platform(hass, 'light', DOMAIN)
    # load_platform(hass, 'sensor', DOMAIN)
    # _LOGGER.info(f"Listening on {host}:{port} with alias '{name}'")

    hass.services.async_register(
        DOMAIN, SERVICE_BUSPRO_SEND,
        hass.data[DOMAIN].service_send_to_buspro_bus,
        schema=SERVICE_BUSPRO_SEND_SCHEMA)

    return True


class BusproModule:
    """Representation of Buspro Object."""

    def __init__(self, hass, config):
        """Initialize of Buspro module."""
        self.hass = hass
        self.config = config
        self.connected = False
        self.hdl = None

        host = config[DOMAIN][CONF_HOST]
        port = config[DOMAIN][CONF_PORT]
        # name = config[DOMAIN][CONF_NAME]
        # GATEWAY_ADDRESS_SEND_RECEIVE = (('192.168.1.15', 6000), ('', 6000))

        self.gateway_address_send_receive = ((host, port), ('', port))
        self.init_hdl()

    def init_hdl(self):
        """Initialize of Buspro object."""
        # noinspection PyUnresolvedReferences
        from .pybuspro.buspro import Buspro
        self.hdl = Buspro(self.gateway_address_send_receive, self.hass.loop)
        # self.hdl.register_telegram_received_all_messages_cb(self.telegram_received_cb)

    async def start(self):
        """Start Buspro object. Connect to tunneling device."""
        await self.hdl.start(state_updater=False)
        self.hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, self.stop)
        self.connected = True

    # noinspection PyUnusedLocal
    async def stop(self, event):
        """Stop Buspro object. Disconnect from tunneling device."""
        await self.hdl.stop()

    async def service_send_to_buspro_bus(self, call):
        """Service for sending an arbitrary Buspro message to the Buspro bus."""
        # noinspection PyUnresolvedReferences
        from .core.telegram import Telegram

        attr_payload = call.data.get(SERVICE_BUSPRO_ATTR_PAYLOAD)
        attr_address = call.data.get(SERVICE_BUSPRO_ATTR_ADDRESS)

        telegram = Telegram()
        telegram.payload = attr_payload
        telegram.target_address = attr_address

        await self.hdl.network_interface.send_telegram(telegram)

    '''
    def telegram_received_cb(self, telegram):
        #     """Call invoked after a KNX telegram was received."""
        #     self.hass.bus.fire('knx_event', {
        #         'address': str(telegram.group_address),
        #         'data': telegram.payload.value
        #     })
        # _LOGGER.info(f"Callback: '{telegram}'")
        return False
    '''
