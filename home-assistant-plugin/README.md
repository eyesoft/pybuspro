# Configuration of Buspro plug-in

##configuration.yaml







####Component

To enable the use of the Buspro component in your installation, add the following to your configuration.yaml file:

```yaml
buspro:
  host: IP_ADDRESS
  port: PORT
  name: "My Buspro installation"
```

Configuration variables:

+ **host** _(string) (Required)_: The ip address of your Buspro Ethernet gateway
+ **port** _(int) (Required)_: The UDP port to your Buspro Ethernet gateway
+ **name** _(string) (Optional)_: The name of the installation








####Light platform
   
To use your Buspro light in your installation, add the following to your configuration.yaml file: 

```yaml
light:
  - platform: buspro
    running_time: 3
    devices:
      1.89.1:
        name: Living Room Light
        running_time = 5
      1.89.2:
        name: Front Door Light
        dimmable = False
```

Configuration variables:

+ **running_time** _(int) (Optional)_: Default running time in seconds for all devices. Running time is 0 seconds if not set.
+ **devices** _(Required)_: A list of devices to set up
  + **X.X.X** _(Required)_: The address of the device on the format `<subnet ID>.<device ID>.<channel number>`
    + **name** _(string) (Required)_: The name of the device
    + **running_time** _(int) (Optional)_: The running time in seconds for the device. If omitted, the default running time for all devices is used.
    + **dimmable** _(boolean) (Optional)_: Is the device dimmable? Default is True. 






####Switch platform

To use your Buspro switch in your installation, add the following to your configuration.yaml file: 

```yaml
switch:
  - platform: buspro
    devices:
      1.89.1:
        name: Living Room Switch
      1.89.2:
        name: Front Door Switch
```

Configuration variables:

+ **devices** _(Required)_: A list of devices to set up
  + **X.X.X** _(Required)_: The address of the device on the format `<subnet ID>.<device ID>.<channel number>`
    + **name** _(string) (Required)_: The name of the device






####Sensor platform

To use your Buspro sensor in your installation, add the following to your configuration.yaml file: 

```yaml
sensor:
  - platform: buspro
    devices:
      - address: 1.74
        name: Living Room
        type: temperature
        unit_of_measurement: °C
      - address: 1.74
        name: Front Door
        type: illuminance
        unit_of_measurement: lux
```

Configuration variables:

+ **devices** _(Required)_: A list of devices to set up
  + **address** _(string) (Required)_: The address of the sensor device on the format `<subnet ID>.<device ID>`
  + **name** _(string) (Required)_: The name of the device
  + **type** _(string) (Required)_: Type of sensor to monitor. Available sensors: 'temperature', 'illuminance'.
  + **unit_of_measurement** _(string) (Optional)_: text to be displayed as unit of measurement






####Binary sensor platform

To use your Buspro binary sensor in your installation, add the following to your configuration.yaml file: 

```yaml
sensor:
  - platform: buspro
    devices:
      - address: 1.74
        name: Living Room
        type: motion
        device_class: motion
      - address: 1.74
        name: Front Door
        type: dry_contact_1
```

Configuration variables:

+ **devices** _(Required)_: A list of devices to set up
  + **address** _(string) (Required)_: The address of the sensor device on the format `<subnet ID>.<device ID>`
  + **name** _(string) (Required)_: The name of the device
  + **type** _(string) (Required)_: Type of sensor to monitor. Available sensors: 'motion', 'dry_contact_1', 'dry_contact_2'.
  + **device_class** _(string) (Optional)_: HASS device class e.g., "motion".







####Climate platform

To use your Buspro panel climate control in your installation, add the following to your configuration.yaml file: 

```yaml
climate:
  - platform: buspro
    devices:
      - address: 1.74
        name: Living Room
      - address: 1.74
        name: Front Door
``

Configuration variables:

+ **devices** _(Required)_: A list of devices to set up
  + **address** _(string) (Required)_: The address of the sensor device on the format `<subnet ID>.<device ID>`
  + **name** _(string) (Required)_: The name of the device








    
---
##Services

####Sending an arbitrary message:
```
Domain: buspro
Service: send_message
Service Data: {"address": [1,74], "operate_code": [4,78], "payload": [1,100,0,3]}
```
####Activating a scene:
```
Domain: buspro
Service: activate_scene
Service Data: {"address": [1,74], "scene_address": [3,5]}
```
####Setting an universal switch:
```
Domain: buspro
Service: set_universal_switch
Service Data: {"address": [1,74], "switch_number": 100, "status": 1}
```
