pybuspro - A Buspro Library Written in Python
====================================================

Documentation
-------------

See documentation at: [https://home-assistant.io/](https://home-assistant.io/)


Home-Assistant Plugin
---------------------

pybuspro contains a Plugin for the [Home-Assistant](https://home-assistant.io/) automation plattform


Example
-------

```python
"""Example for switching a light on and off."""
import asyncio

async def main():
    """Connect to Buspro bus, switch on light, wait 2 seconds and switch of off again."""
    buspro = Buspro()
    await buspro.start()
    light = Light(buspro,
                  name='TestLight',
                  address='1.100.9')
    await light.set_on()
    await asyncio.sleep(2)
    await light.set_off()
    await buspro.stop()


# pylint: disable=invalid-name
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
```

