__init__:
self._devices = collections.defaultdict(list)
self._deviceCallbacks = collections.defaultdict(list)

register:
self._deviceCallbacks[callbackID].append((callback))

_callback_thread:
while self._running:
    packet = self._queue.get(True)
        cmd = packet['cmd']
        callback_id = '{} {}'.format(sensor, sid)
        for deviceCallback in self._deviceCallbacks.get(callback_id, ()):
            deviceCallback(model, json.loads(data))
    self._queue.task_done()

_listen_thread:
while self._running:
    data, addr = self.socket.recvfrom(self.SOCKET_BUFSIZE)
    payload = json.loads(data.decode("utf-8"))
    self._queue.put(payload)
self._queue.put({})  # empty item to ensure callback thread shuts down







"""
"""


def _create_mcast_socket(self):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.bind((self.MULTICAST_ADDRESS, self.MULTICAST_PORT))
    return sock

def listen(self):
    """Start listening."""

    _LOGGER.info('Creating Multicast Socket')
    self._mcastsocket = self._create_mcast_socket()
    self._listening = True
    thread = Thread(target=self._listen_to_msg, args=())
    self._threads.append(thread)
    thread.daemon = True
    thread.start()

def stop_listen(self):
    """Stop listening."""
    self._listening = False

    self._mcastsocket.close()
    self._mcastsocket = None

    for thread in self._threads:
        thread.join()

def _listen_to_msg(self):
    while self._listening:
        data, (ip_add, port) = self._mcastsocket.recvfrom(self.SOCKET_BUFSIZE)
        data = json.loads(data.decode("ascii"))
        cmd = data['cmd']
        self.hass.add_job(gateway.push_data, data)

self.devices = defaultdict(list)
self.ha_devices = defaultdict(list)

def gateway.push_data(self, data):
    """Push data broadcasted from gateway to device"""
    jdata = json.loads(data['data'])
    for device in self.ha_devices[sid]:
        device.push_data(jdata)


# HASS
def push_data(self, data):
    """Push from Hub"""
    self._parse_voltage(data)
    self.schedule_update_ha_state()

def _parse_voltage(self, data):
    percent = ((voltage - min_volt) / (max_volt - min_volt)) * 100
    self._device_state_attributes[ATTR_BATTERY_LEVEL] = round(percent)
