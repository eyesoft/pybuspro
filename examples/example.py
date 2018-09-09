import asyncio
import random

from pybuspro.buspro import Buspro
from pybuspro.devices.light import Light

# ip, port = gateway_address
# subnet_id, device_id, channel = device_address

GATEWAY_ADDRESS_SEND_RECEIVE = (('192.168.1.15', 6000), ('', 6000))
# GATEWAY_ADDRESS_SEND_RECEIVE = (('10.120.1.66', 6000), ('10.120.1.66', 6000))


def callback_all_messages(telegram):
    print(f'Callback all messages: {telegram}')


def callback_light(telegram):
    print(f'Callback light: {telegram}')


async def first_callback(message):
    print(f"callback 1 received: {message}")


async def second_callback(message):
    print(f"callback 2 received: {message}")


async def main():

    # Now you want to start long_operation, but you don't want to wait it finished:
    # long_operation should be started, but second msg should be printed immediately.
    # Create task to do so:

    loop_ = asyncio.get_event_loop()
    hdl = Buspro(GATEWAY_ADDRESS_SEND_RECEIVE, loop_)
    # hdl._register_telegram_received_cb_2(callback_all_messages)

    # await hdl.connect()

    light = Light(hdl, device_address=(1, 123, 11), name="name of light")
    light.register_telegram_received_cb(first_callback)
    # print(light.name)

    task = asyncio.ensure_future(hdl.start())
    # task = asyncio.ensure_future(hdl.start_listen(callback_all_messages))
    # task = asyncio.ensure_future(hdl.start())

    '''
    await hdl._send_message(b'\0x01')
    await asyncio.sleep(2)
    await hdl._send_message(b'\0x02')
    await asyncio.sleep(2)
    await hdl._send_message(b'\0x03')
    await asyncio.sleep(2)
    await hdl._send_message(b'\0x04')
    '''

    # await light.set_on()
    # await asyncio.sleep(2)
    # await light.set_off()
    # await asyncio.sleep(4)
    # await light.dim(75)

    # await hdl.disconnect()

    # Now, when you want, you can await task finished:
    await task


async def send_random_message(hdl):
    messages = [
        b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\r\x012\x014\x00\x02\x01H\x01\t\x8d\x1b',
        b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x0f\x01(\x014\x001\x01J\x04\x00\x00\x03\xc4c',
        b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x0f\x012\x014\x001\x01\x83\x05d\x00\x00\t\xdb',
        b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x0e\x01J\x02`\x002\xff\xff\x04\xf8\x00\x96\xb3',
        b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x0f\x01H\x02`\x00\x03\xff\xff\x01\t\x06\x05\xc6g',
        b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x10\x01\x83\x00\x11\x002\xff\xff\x05\xf8d\x06\x10)(',
        b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x11\x01d\x04S\xdaD\xff\xff\x12\t\x05\x11\x1c\x00^\x05',
        b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x0f\x01\x82\x00\x11\xef\xff\xff\xff\x01\xfe\x06\x00u8',
        b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x11\x01)\x014\xe3\xe5\xff\xff\x01\x1f\x00\x00\xf8A\xac4',
        b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x11\x011\x014\xe3\xe5\xff\xff\x01\x1f\x00\x00\xf8A\xb1\xda',
        b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x11\x01n\x0b\xe9\xdaD\xff\xff\x12\x07\x13\x11\x18\x00\x87\xf8',
        b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x11\x01\x83\x00\x11\xef\xff\xff\xff\x03\xfe\xfe\xff\x06\x10\\\n',
        b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x14\x01(\x014\x16G\xff\xff2\x00\x19\x00\x00\x00\x00\x00\x00\xfbC',
        b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x14\x011\x014\x16G\xff\xff3\x00\x00\x00\x00\x00\x00\x00\x00\x96|',
        b'\xc0\xa8\x01\x0fHDLMIRACLE\xaa\xaa\x14\x01)\x014\x16G\xff\xff3\x00\x00\x00\x00\x00\x00\x00\x00\xa4\xf3',
    ]

    while True:
        await hdl.network_interface.send_message(random.choice(messages))
        await asyncio.sleep(2)


async def main2():
    loop__ = asyncio.get_event_loop()
    hdl = Buspro(GATEWAY_ADDRESS_SEND_RECEIVE, loop__)
    hdl.register_telegram_received_all_messages_cb(callback_all_messages)
    await hdl.start()
    # await send_random_message(hdl)


async def main3():
    loop__ = asyncio.get_event_loop()
    hdl = Buspro(GATEWAY_ADDRESS_SEND_RECEIVE, loop__)
    hdl.register_telegram_received_all_messages_cb(callback_all_messages)
    await hdl.start()

    # Lys kino
    light = Light(hdl, (1, 74, 1), "kino")
    light.register_telegram_received_cb(callback_light)

    # await light.set_off(0)

    await light.set_on(3)
    print(f"{light.current_brightness} {light.is_on}")

    await asyncio.sleep(5)
    await light.set_off()
    print(f"{light.current_brightness} {light.is_on}")

    await asyncio.sleep(5)
    await light.set_brightness(20, 5)
    print(f"{light.current_brightness} {light.is_on}")

    await asyncio.sleep(10)
    await light.set_off()

    # light2 = Light(hdl, (1, 100, 1))
    # light2.register_telegram_received_cb(callback_light)

    # await light2.set_brightness(10, 0)
    # print(f"{light.brightness} {light.is_on}")

    # await send_random_message(hdl)


async def after_update_callback(light):
    print(f"AFTER UPDATE: {light.current_brightness}")

async def main4():
    loop__ = asyncio.get_event_loop()
    hdl = Buspro(GATEWAY_ADDRESS_SEND_RECEIVE, loop__)
    # hdl.register_telegram_received_all_messages_cb(callback_all_messages)
    await hdl.start()

    # Lys kino
    light = Light(hdl, (1, 74, 1), "kino")
    light.register_device_updated_cb(after_update_callback)

    # await light.set_brightness(30)
    # light.read_current_state()
    light.register_telegram_received_cb(callback_light)


    # await light.set_on(3)
    # print(f"{light.current_brightness} {light.is_on}")




if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(main2())
    # loop.run_until_complete(main3())
    loop.run_until_complete(main4())
    loop.run_forever()
