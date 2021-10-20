# AUTONOMOUS-NOISE-UNIT

<img style="width:300px" src="https://fra1.digitaloceanspaces.com/sandreae-storage/anu-website/uploads/2020/11/09/636352e7-2062-4df9-8115-398165bd8b23.JPG"/>

Python scripts for running JackTrip on an RPi with OLED screen and rotary switch interface. Works with either the pisound or hifiberry audio interfaces in combination with the in development A-N-U RPi Hat (DIY setup also possible). In order to connect to other peers you will either need a JackTrip hubserver running elsewhere which all clients connect to, or to connect in peer-to-peer fasion you will need to have the relevent port-forwarding enabled on your router and know the other peers public ip address.

## Requirements
**[Raspberry Pi](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/)**
- audio interface ([pisound](https://blokas.io/pisound/) or [hifiberry DAC + ADC](https://www.hifiberry.com/shop/boards/hifiberry-dac-adc/))
- Micro SD card
- Custom ANU hat (or build your own)
  - 128x64 i2c OLED screen
  - rotary switch
- USB-C power cable

## Installation

### From disk img
You can use a tool like [raspberry pi imager](https://www.raspberrypi.com/software/) to build from our latest RPi image [here](https://github.com/noiseorchestra/autonomous-noise-unit/releases/download/2.0.0/anu.img.gz)

You would still need to satisfy the hardware requirements to get everything up and running. You can do this by building a custom hat with the required components or get in touch with us and we'd be happy to send you one of the PCBs we use for making up our own ANU. We have a few left.... Details of the completed devices can be seen [here](https://autonomousnoiseunit.co.uk/how-to-pisound) with a pisound interface and [here](https://autonomousnoiseunit.co.uk/how-to-hifiberry) with a hifiberry.

### Ansible scripts
If you want to see what's happening under the hood, the ansible playbooks [here](https://github.com/sandreae/anu-ansible) are a good place to start.

## Features
- Stand alone RPi based device for running JackTrip sessions
- Connect to a hub-server or peer using the OLED menu
- Configure JackTrip session parameters
- Monitor session audio levels

### ANU (on device) Menu Structure

- CONNECT
- LEVEL METER
- SETTINGS
    - INPUT: value
    - DEVICE INFO
    - ADVANCED OPTIONS
        - CHANNELS: value
        - QUEUE: value
        - IP: value
        - MODE: value
        - PEER: value
        - <-- BACK
    - UPDATE
    - SWITCH OFF
    - <-- BACK

## Status
This project is very much in development, it's currently in a working state and the main branch will remain that way, but there may be breaking changes.
