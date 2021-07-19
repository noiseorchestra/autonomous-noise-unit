# AUTONOMOUS-NOISE-UNIT
Python scripts for running JackTrip on an RPi with OLED screen and rotary switch interface. Works with either the pisound or hifiberry audio interfaces in combination with the in development A-N-U RPi Hat (DIY setup also possible). In order to connect to other peers you will either need a JackTrip hubserver running elsewhere which all clients connect to, or to connect in peer-to-peer fasion you will need to have the relevent port-forwarding enabled on your router and know the other peers public ip address.

## Requirements
**[Raspberry Pi](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/) with [Raspbian](https://www.raspberrypi.org/downloads/raspberry-pi-os/) based OS**
- audio interface ([pisound](https://blokas.io/pisound/) or [hifiberry DAC + ADC](https://www.hifiberry.com/shop/boards/hifiberry-dac-adc/))
- Micros SD card
- USB-C power cable
- 128x64 i2c OLED screen *
- rotary switch *

**we're working on an A-N-U Hat which would replace these in a neat way.*

**Python3**
*including pip3 and setup-tools*

**[JACK](https://jackaudio.org/)**
API for making and managing audio connections between software and hardware devices. Should be installed with Real-Time priority enabled.

**[JackTrip](https://github.com/jacktrip/jacktrip)**
High quality low latency audio transfer over the internet.

**[jack_meter](https://www.aelius.com/njh/jackmeter/)**
A simple in terminal level meter.

**OLED and Rotary Switch dependencies**
The OLED screen and rotary switch hardware have several dependencies which can be install like this:

```shell
$ sudo apt-get install -y python3-dev python-smbus i2c-tools python3-pil libopenjp2-7-dev python3-rpi.gpio
```

## Installation
Once you have JACK and JackTrip installed and necessary RPi audio interface and periferals attached (but not configured), you can complete setting up your RPi and installing the remaining requirements in one of 2 ways.

### Manual installation
Full manual installation requires you to setup your audio interface and periferals and install the remaining requirements (jack_meter and OLED dependencies). You can then clone this repo and install python dependencies using pip.

```shell
$ ssh pi@<rpi-address>.local
$ sudo apt-get install -y git
$ git clone https://github.com/noiseorchestra/autonomous-noise-unit.git
$ pip3 install -r autonomous-noise-unit/requirements.txt
$ cp default-config.ini config.ini
```

Then to run the script:

```shell
$ python3 autonomous-noise-unit/noisebox.py
```

### Install Script

Alternatively, use this [install script](https://github.com/noiseorchestra/autonomous-noise-unit-install) to clone the repo, install the remaining dependencies and setup the RPi & periferals automatically. It will enable the main script to run on startup so you can use your A-N-U as a stand alone headless system. We only recommend doing this if you want a dedicated unit, don't run this this on top of an existing RPi system. This also gives you the option of configuring a Telegraf server for monitoring RPi metrics as well as setting up a mesh VPN which can be used for remote access and making peer-to-peer connections between different A-N-U peers (this feature is experimental).

```shell
$ ssh pi@<rpi-address>.local
$ sudo apt-get install -y git
$ git clone https://github.com/noiseorchestra/autonomous-noise-unit-install.git
$ sudo bash autonomous-noise-unit-install/start.sh
```

### Initial Configuration
Once you have installed the scrip you need to edit the config.ini to match your desired JackTrip and JACK session settings. This includes setting the hub-server and peer IP addresses.

```shell
$ sudo cp autonomous-noise-unit/default-config.ini autonomous-noise-unit/config.ini
```

## Features
- Stand alone RPi based device for running JackTrip sessions
- Connect to a hub-server or peer using the OLED menu
- Monitor audio levels

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
