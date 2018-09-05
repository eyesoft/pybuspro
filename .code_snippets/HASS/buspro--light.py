# Add your custom device specific code to the setup_platform method in light/buspro.py and switch/buspro.py

import custom_components.buspro as buspro

# https://developers.home-assistant.io/docs/en/creating_component_generic_discovery.html
# 'switch' will receive discovery_info={'optional': 'arguments'}
# as passed in above. 'light' will receive discovery_info=None
def setup_platform(hass, config, add_devices, discovery_info=None):
    """Your switch/light specific code."""
    # You can now use hass.data[buspro.DATA_BUSPRO]