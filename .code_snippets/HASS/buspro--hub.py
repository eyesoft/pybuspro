"""
Support for Buspro devices.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/buspro

:home-assistant/homeassistant/components/buspro.py
"""

import asyncio
import logging
import socket

import voluptuous as vol

from homeassistant.core import callback
from homeassistant.const import (
    STATE_ALARM_ARMED_AWAY, STATE_ALARM_ARMED_HOME, STATE_ALARM_DISARMED, STATE_ALARM_TRIGGERED, 
	EVENT_HOMEASSISTANT_START, EVENT_HOMEASSISTANT_STOP)
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.util.json import json

#  REQUIREMENTS = ['buspro==0.1.0']

_LOGGER = logging.getLogger(__name__)

DEFAULT_PORT = 9999

DOMAIN = 'buspro'

BUSPRO_CONFIG_FILE = 'buspro.conf'

DATA_BUSPRO = 'buspro'

SIGNAL_PANEL_MESSAGE = 'buspro.panel_message'

SIGNAL_ZONES_UPDATED = 'buspro.zones_updated'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_DEVICE_HOST): cv.string,
        vol.Optional(CONF_DEVICE_PORT, default=DEFAULT_PORT): cv.port
    }),
}, extra=vol.ALLOW_EXTRA)
















async def async_setup(hass, config):
    """Set up the Buspro component."""
    conf = config.get(DOMAIN)

    host = conf.get(CONF_DEVICE_HOST)
    port = conf.get(CONF_DEVICE_PORT)

    #  from buspro.buspro import AsyncBuspro	#  inkluderer api
	#  from buspro import Buspro

    busproClient = Buspro(host, port, hass.loop)

    hass.data[DATA_BUSPRO] = busproClient

	_LOGGER.debug("connecting to busproClient")
	
    result = await busproClient.connect()

    if not result:
        return False

			
		
    
    async def _close():
        busproClient.close()
		
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, _close())

	
	
	
    task_light = hass.async_create_task(async_load_platform(hass, 'light', DOMAIN, conf, config))
    task_switch = hass.async_create_task(async_load_platform(hass, 'switch', DOMAIN, conf, config))
		
    await asyncio.wait([task_light, task_switch], loop=hass.loop)
		
		


	
	
	
    @callback
    def callback_1(status):
        """Send status update received from alarm to home assistant."""
		state = STATE_ALARM_DISARMED
        if status == AlarmState.ARMED_MODE0:
            state = STATE_ALARM_ARMED_AWAY

        async_dispatcher_send(hass, SIGNAL_PANEL_MESSAGE, state)
		
		
		
		
    @callback
    def callback_2(status):
        """Update zone objects as per notification from the alarm."""
        async_dispatcher_send( hass, SIGNAL_ZONES_UPDATED, status[ZONES] )

		
		
		
    # Create a task instead of adding a tracking job, since this task will
    # run until the connection to satel_integra is closed.
    hass.loop.create_task( buspro.monitor_status( callback_1, callback_2 ) )

	
	
    return True
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
def buspro_update_event_broker(hass, buspro):
    """
    Dispatch SIGNAL_NEST_UPDATE to devices when nest stream API received data.
    Runs in its own thread.
    """
    _LOGGER.debug("listening buspro.update_event")

    while hass.is_running:
        buspro.update_event.wait()

        if not hass.is_running:
            break

        buspro.update_event.clear()
        _LOGGER.debug("dispatching buspro data update")
        dispatcher_send(hass, SIGNAL_NEST_UPDATE)

    _LOGGER.debug("stop listening buspro.update_event")

	
	
async def _______async_setup(hass, config):
    """Set up the Buspro component."""
    conf = config.get(DOMAIN)

    host = conf.get(CONF_DEVICE_HOST)
    port = conf.get(CONF_DEVICE_PORT)

	from buspro import Buspro

    busproClient = Buspro(host, port, hass.loop)

	_LOGGER.debug("proceeding with setup")
	
    hass.data[DATA_BUSPRO] = BusproDevice(hass, conf, busproClient)

	if not await hass.async_add_job(hass.data[DATA_BUSPRO].initialize):
		return False
	
	
	for component in 'climate', 'light', 'sensor', 'binary_sensor', 'switch':
	hass.async_create_task(hass.config_entries.async_forward_entry_setup(
		entry, component))
	

		
			
	@callback
	def start_up(event):
		"""Start Buspro update event listener."""
		threading.Thread(
			name='Buspro update listener',
			target=buspro_update_event_broker,
			args=(hass, busproClient)
		).start()

	hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, start_up)

	@callback
	def shut_down(event):
		"""Stop Buspro update event listener."""
		buspro.update_event.set()

	hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, shut_down)

	_LOGGER.debug("async_setup_buspro is done")

	return True		
	
	
	
class BusproDevice:
	"""Structue Buspro functions for hass."""

	def __init__(self, hass, conf, busproClient):
		"""Init Buspro Devices."""
		self.hass = hass
		self.busproClient = busproClient
		
	def initialize(self):
		"""Inititalize Buspro."""
		result = await self.busproClient.connect()

		if not result:
			return False
		
		return True
		

		