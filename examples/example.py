import asyncio
import random

from pybuspro.buspro import Buspro
from pybuspro.devices.light import Light
from pybuspro.devices.switch import Switch
from pybuspro.devices.scene import Scene

# ip, port = gateway_address
# subnet_id, device_id, channel = device_address

# GATEWAY_ADDRESS_SEND_RECEIVE = (('192.168.1.15', 6000), ('', 6000))
GATEWAY_ADDRESS_SEND_RECEIVE = (('10.120.1.66', 6000), ('10.120.1.66', 6000))


def callback_received_for_all_messages(telegram):
    print(f'Callback all messages: {telegram}')


async def main__send_and_receive_random_messages():
    loop__ = asyncio.get_event_loop()
    hdl = Buspro(GATEWAY_ADDRESS_SEND_RECEIVE, loop__)
    hdl.register_telegram_received_all_messages_cb(callback_received_for_all_messages)
    await hdl.start()

    async def send_random_message(hdl_):
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
            await hdl_.network_interface.send_message(random.choice(messages))
            await asyncio.sleep(2)

    await send_random_message(hdl)


async def main__turn_light_on_off():
    loop__ = asyncio.get_event_loop()
    hdl = Buspro(GATEWAY_ADDRESS_SEND_RECEIVE, loop__)
    hdl.register_telegram_received_all_messages_cb(callback_received_for_all_messages)
    await hdl.start()

    def callback_received_for_light(telegram):
        print(f'Callback light: {telegram}')

    # Lys kino
    light = Light(hdl, (1, 74, 1), "kino")
    light.register_telegram_received_cb(callback_received_for_light)

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


async def main__turn_light_on_off_with_device_updated_cb():
    loop__ = asyncio.get_event_loop()
    hdl = Buspro(GATEWAY_ADDRESS_SEND_RECEIVE, loop__)
    # hdl.register_telegram_received_all_messages_cb(callback_received_for_all_messages)
    await hdl.start()

    async def device_updated_callback(light_):
        print(f"AFTER UPDATE: {light_.current_brightness}")

    def callback_received_for_light(telegram):
        print(f'Callback light: {telegram}')

    # Lys kino
    light = Light(hdl, (1, 74, 1), "kino")
    light.register_device_updated_cb(device_updated_callback)
    light.register_telegram_received_cb(callback_received_for_light)

    await light.set_brightness(30)
    # light.read_current_state()

    await light.set_on(3)
    print(f"{light.current_brightness} {light.is_on}")


async def main__turn_switch_on_off():
    loop__ = asyncio.get_event_loop()
    hdl = Buspro(GATEWAY_ADDRESS_SEND_RECEIVE, loop__)
    hdl.register_telegram_received_all_messages_cb(callback_received_for_all_messages)
    await hdl.start()

    def callback_received_for_switch(telegram):
        print(f'Callback switch: {telegram}')

    # Lys kino
    switch = Switch(hdl, (1, 74, 1), "kino")
    switch.register_telegram_received_cb(callback_received_for_switch)

    await switch.set_on()
    print(f"{switch.is_on}")

    await asyncio.sleep(5)
    await switch.set_off()
    print(f"{switch.is_on}")


async def main__activate_scene():
    loop__ = asyncio.get_event_loop()
    hdl = Buspro(GATEWAY_ADDRESS_SEND_RECEIVE, loop__)
    hdl.register_telegram_received_all_messages_cb(callback_received_for_all_messages)
    await hdl.start()
    await hdl.network_interface.activate_scene([1, 74], [2, 4])

'''
async def main__run_scene():
    loop__ = asyncio.get_event_loop()
    hdl = Buspro(GATEWAY_ADDRESS_SEND_RECEIVE, loop__)
    hdl.register_telegram_received_all_messages_cb(callback_received_for_all_messages)
    await hdl.start()

    def callback_received_for_scene(telegram):
        print(f'Callback scene: {telegram}')

    # Scene kino
    scene = Scene(hdl, (1, 74, 1, 2), "kino")
    scene.register_telegram_received_cb(callback_received_for_scene)

    await scene.run()
'''

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(main__send_and_receive_random_messages())
    # loop.run_until_complete(main__turn_light_on_off())
    # loop.run_until_complete(main__turn_light_on_off_with_device_updated_cb())
    # loop.run_until_complete(main__turn_switch_on_off())
    # loop.run_until_complete(main__run_scene())
    loop.run_until_complete(main__activate_scene())
    loop.run_forever()
