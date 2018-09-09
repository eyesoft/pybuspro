class Device(object):
    def __init__(self, buspro, device_address, name):
        self._device_address = device_address
        self._buspro = buspro
        self._name = name
        self.device_updated_cbs = []

    @property
    def name(self):
        return self._name

    def register_telegram_received_cb(self, telegram_received_cb):
        self._buspro.register_telegram_received_device_cb(telegram_received_cb, self._device_address)

    def register_device_updated_cb(self, device_updated_cb):
        """Register device updated callback."""
        self.device_updated_cbs.append(device_updated_cb)

    def unregister_device_updated_cb(self, device_updated_cb):
        """Unregister device updated callback."""
        self.device_updated_cbs.remove(device_updated_cb)

    async def device_updated(self):
        for device_updated_cb in self.device_updated_cbs:
            await device_updated_cb(self)

    async def send_telegram(self, telegram):
        await self._buspro.network_interface.send_telegram(telegram)
        await self.device_updated()
