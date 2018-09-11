configuration.yaml
=

Component
-
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

Light platform
-   
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
```

Configuration variables:

+ **running_time** _(int) (Optional)_: Default running time in seconds for all devices. Running time is 0 seconds if not set.
+ **devices** _(Required)_: A list of devices to set up
  + **X.X.X** _(Required)_: The address of the device on the format `<subnet ID>.<device ID>.<channel number>`
    + **name** _(string) (Required)_: The name of the device
    + **running_time** _(int) (Optional)_: The running time in seconds for the device. If omitted, the default running time for all devices is used.

Switch platform
-   
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
