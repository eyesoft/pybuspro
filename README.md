pybuspro - A Buspro Library Written in Python
====================================================

Documentation
-------------

See documentation at: [https://home-assistant.io/](https://home-assistant.io/)


Home-Assistant Plugin
---------------------

pybuspro contains a Plugin for the [Home-Assistant](https://home-assistant.io/) automation plattform


Installation
-------

```commandline
pip3 install pybuspro
```


Example
-------

```python
"""Example for switching a light on and off."""
import asyncio


async def main():
    """Connect to Buspro bus, switch on light, wait 2 seconds and switch of off again."""
    buspro = Buspro(('192.168.0.1', 6000))
    await buspro.connect()
    
    light = Light(buspro, device_address=(1, 100, 9))
    await light.set_on()
    await asyncio.sleep(2)
    await light.set_off()
    
    await buspro.disconnect()


# pylint: disable=invalid-name
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
```

