# https://www.binarytides.com/python-socket-server-code-example/


# https://github.com/home-assistant/home-assistant/blob/master/homeassistant/components/pilight.py
# https://github.com/DavidLP/pilight/blob/master/pilight/pilight.py

    pilight_client = pilight.Client(host=host, port=port)
    pilight_client.start()
    pilight_client.stop()
    pilight_client.send_code(data={"protocol": [ "kaku_switch" ], "id": 1,"unit": 0,"off": 1})    
    
    def handle_received_code(data):
        """Run when RF codes are received."""
        # Unravel dict of dicts to make event_data cut in automation rule
        # possible
        data = dict({'protocol': data['protocol'], 'uuid': data['uuid']}, **data['message'])

        # No whitelist defined, put data on event bus
        if not whitelist:
            hass.bus.fire(EVENT, data)
            
        # Check if data matches the defined whitelist
        elif all(str(data[key]) in whitelist[key] for key in whitelist):
            hass.bus.fire(EVENT, data)

    pilight_client.set_callback(handle_received_code)
    
    

###########################    
    
# https://github.com/home-assistant/home-assistant/blob/master/homeassistant/components/satel_integra.py
# https://github.com/c-soft/satel_integra

@asyncio.coroutine
def async_setup(hass, config):

    controller = AsyncSatel(host, port, zones, hass.loop, partition)
    result = yield from controller.connect()
    controller.close() 

    @callback
    def alarm_status_update_callback(status):
        _LOGGER.debug("Alarm status callback, status: %s", status)
        hass_alarm_status = STATE_ALARM_DISARMED        
        _LOGGER.debug("Sending hass_alarm_status: %s...", hass_alarm_status)
        async_dispatcher_send(hass, SIGNAL_PANEL_MESSAGE, hass_alarm_status)
        
    @callback
    def zones_update_callback(status):
        """Update zone objects as per notification from the alarm."""
        _LOGGER.debug("Zones callback , status: %s", status)
        async_dispatcher_send(hass, SIGNAL_ZONES_UPDATED, status[ZONES])

    # Create a task instead of adding a tracking job, since this task will
    # run until the connection to satel_integra is closed.
    hass.loop.create_task( controller.keep_alive() )
    hass.loop.create_task( controller.monitor_status( alarm_status_update_callback, zones_update_callback ) )

    return True
    
        
  
  
  
  
@asyncio.coroutine
def async_setup_platform(hass, config, async_add_entities, discovery_info=None):  
    device = SatelIntegraBinarySensor(zone_num, zone_name, zone_type)
    
class SatelIntegraBinarySensor(BinarySensorDevice):
    """Representation of an Satel Integra binary sensor."""
    
    @asyncio.coroutine
    def async_added_to_hass(self):
        """Register callbacks."""
        async_dispatcher_connect(self.hass, SIGNAL_ZONES_UPDATED, self._zones_updated)

    @property
    def should_poll(self):
        """No polling needed."""
        return False
        
    @callback
    def _zones_updated(self, zones):
        """Update the zone's state, if needed."""
        if self._zone_number in zones and self._state != zones[self._zone_number]:
            self._state = zones[self._zone_number]
            self.async_schedule_update_ha_state()
            
            
            
            
            
            