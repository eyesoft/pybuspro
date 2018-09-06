import asyncio
import logging
import signal

from sys import platform






class Buspro:
    def __init__(self, loop_=None):
        self._loop = loop_ or asyncio.get_event_loop()
        self.sigint_received = asyncio.Event()
        self.state_updater = None
        self.started = False
        self.callback = None

    def __del__(self):
        if self.started:
            try:
                task = self._loop.create_task(self.stop())
                self._loop.run_until_complete(task)
            except RuntimeError as exp:
                print(f"LOG: Could not close loop, reason: {exp}")

    async def start(self, state_updater=False, daemon_mode=False):

        if state_updater:
            self.state_updater = StateUpdater(self)
            await self.state_updater.start()

        if daemon_mode:
            await self._loop_until_sigint()

        self.started = True

    async def stop(self):
        self.started = False

    def register_telegram_received_cb(self, telegram_received_cb):
        self.callback = telegram_received_cb

    async def loop_until_sigint(self):
        def sigint_handler():
            self.sigint_received.set()
        if platform == "win32":
            print("LOG: Windows does not support signals")
        else:
            self._loop.add_signal_handler(signal.SIGINT, sigint_handler)
        print("LOG: Press Ctrl+C to stop")
        await self.sigint_received.wait()

    async def sync(self):
        await asyncio.sleep(1)
        await self.callback("...<TELEGRAM>...")


class StateUpdater:
    def __init__(self, buspro):
        self.buspro = buspro
        self.run_forever = True
        self.run_task = None

    async def start(self):
        self.run_task = self.buspro._loop.create_task(self.run())

    async def run(self):
        await asyncio.sleep(0)
        print("LOG: Starting StateUpdater")
        while True:
            await self.buspro.sync()
        pass









class HassBusproRepresentationInCustomComponent:
    def __init__(self, config=None):
        self.config = config
        self.connected = False

        self._init_buspro()
        self._register_callbacks()

    def _init_buspro(self):
        loop_ = asyncio.get_event_loop()    # HASS event loop
        self.buspro = Buspro(loop_=loop_)
        pass

    async def start(self):
        await self.buspro.start(state_updater=True)
        self.connected = True

    async def stop(self):
        await self.buspro.stop()
        self.connected = False

    async def telegram_received_cb(self, telegram):
        print(f"Telegram received: {telegram}")

    def _register_callbacks(self):
        self.buspro.register_telegram_received_cb(self.telegram_received_cb)











async def main():
    component = HassBusproRepresentationInCustomComponent()
    await component.start()

    await asyncio.sleep(3.5)
    print("LOG: Component started")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever()

'''
Emulerer HASS
main() kjører samme kall som HASS custom_component "async def async_setup(hass, config)" ville kjørt
HassBusproRepresentationInCustomComponent starter API og StateUpdater
'''