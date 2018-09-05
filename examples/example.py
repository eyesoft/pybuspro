import asyncio

from pybuspro.buspro import Buspro
from pybuspro.devices.light import Light

# ip, port = gateway_address
# subnet_id, device_id, channel = device_address

GATEWAY_ADDRESS = ('192.168.1.15', 6000)


async def callback_all_messages(telegram):
    print(telegram)


async def first_callback(message):
    print(f"callback 1 received: {message}")


async def second_callback(message):
    print(f"callback 2 received: {message}")


async def main():

    # Now you want to start long_operation, but you don't want to wait it finished:
    # long_operation should be started, but second msg should be printed immediately.
    # Create task to do so:

    hdl = Buspro(GATEWAY_ADDRESS)
    await hdl.connect()

    light = Light(hdl, device_address=(1, 123, 11))
    light.register_telegram_received_cb(first_callback)
    # print(light.name)
    
    task = asyncio.ensure_future(hdl.start_listen(callback_all_messages))
    # task = asyncio.ensure_future(hdl.start())

    # await light.set_on()
    # await asyncio.sleep(2)
    # await light.set_off()
    # await asyncio.sleep(4)
    # await light.dim(75)

    await hdl.disconnect()

    # Now, when you want, you can await task finished:
    await task


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
