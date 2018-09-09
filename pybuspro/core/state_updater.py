import asyncio


class StateUpdater:
    def __init__(self, buspro, sleep=10):
        self.buspro = buspro
        self.run_forever = True
        self.run_task = None
        self.sleep = sleep

    async def start(self):
        self.run_task = self.buspro.loop.create_task(self.run())

    async def run(self):
        await asyncio.sleep(0)
        # print(f"LOG: Starting StateUpdater with {self.sleep} seconds interval")

        while True:
            await asyncio.sleep(self.sleep)
            await self.buspro.sync()
