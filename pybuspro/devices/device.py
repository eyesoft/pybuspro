class Device(object):
    def __init__(self, buspro, device_address):
        self._device_address = device_address
        self._buspro = buspro
    
    @property
    def name(self):
        adr = f"{self._device_address}"
        return adr

    def register_telegram_received_cb(self, telegram_received_cb):
        self._buspro.register_telegram_received_cb(telegram_received_cb, self._device_address)
