# weather_station
This repository contains a collection of scripts and code for a arduino based weather station approach for the FACT Weatherstation as wel as some documentation.


# Hardware

We use an arduino micro controler (Uno or Mega) to read the signals from the several sensors wich are described in the following. The arduino will send the collected raw data via serial to a raspberrPi which will do further computions on the recieved Data, e.g., Wind direction, Dew Point etc.

## Sensors

### Temperatur Sensor: DHT22
The DHT22 is a basic, low-cost digital temperature and humidity sensor. It uses a capacitive humidity sensor and a thermistor to measure the surrounding air, and spits out a digital signal on the data pin (no analog input pins needed)

For details see: https://www.adafruit.com/product/385
Documentation: https://www.sparkfun.com/datasheets/Sensors/Temperature/DHT22.pdf
Ardunio Library for the DHT22: https://github.com/adafruit/DHT-sensor-library

The design for our weatherstation is based un this instruction: http://fluuux.de/2012/10/arduino-temperatur-und-luftfeuchtigkeit-mit-dem-dht22-prufen/


### Rainsensor: Hydreon RG 11
Manual: http://rainsensors.com/2015/documents/rg-11_instructions.pdf
Tipping bucket example: http://cactus.io/hookups/weather/rain/hydreon/hookup-arduino-to-hydreon-rg-11-rain-sensor

In tipping bucket mode 0.01mm the Sensor produces a 100ms pulse for each detected bucket switch.

### Rainsensor: Kemo M152
https://www.kemo-electronic.de/de/Haustechnik/Garten/M152-Regensensor-12-V-DC.php

### Windsensors:

Readout code on basis of: https://github.com/chiemseesurfer/arduinoWeatherstation
http://maxoberberger.net/projects/arduino-weatherstation/
datasheets: https://www.argentdata.com/files/80422_datasheet.pdf

#### Anemometer
The Anemometer measures via closing contact. 2.4 km/h windspeed cause the contact to close once per second.

#### Wind Vane:
For the wind vane a a 15k resistor is used resulting in the following directions, 0° points away from the Anemometer:

| Direction / Degrees | Resistance R_i / kOhms| Voltage U_i/ V (U_0=5v, R_0=15k) |
| --- | ---   |--- |
|0    | 33    |3.56|
|22.5 |6.57   |1.63|
|45   |8.2    |1.88|
|67.5 |0.891  |0.31|
|90   |1      |0.34|
|112.5|0.688  |0.24|
|135  |2.2    |0.70|
|157.5|1.41   |0.46|
|180  |3.9    |1.12|
|202.5|3.14   |0.94|
|225  |16     |2.71|
|247.5|14.12  |2.51|
|270  |120    |4.52|
|292.5|42.12  |3.80|
|135  |64.9   |4.16|
|337.5|21.88  |3.09|


voltages = {4.52, 3.80, 4.16, 3.09, 3.56, 1.63, 1.88, 0.31, 0.34, 0.24, 0.70, 0.46, 1.12, 0.94, 2.71, 2.51}

directions = {0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5, 180, 202.5, 225, 247.5, 270, 292.5, 315, 337.5}

From the Resistance you can calculate the expected direction voltage as follows:

U_i = U_0 / (R_0/R_i + 1)

## Pin-Allocation
The following is the pin-allocation for arduino mega

| Pin  | Sensor Name| Pin Mode |
| --- | ---   | ---   |
| 2   | wind_speed | interrupt |
| 3   | RG11_1 | interrupt |
| 18   | RG11_2 | interrupt |
| 19   | M152 | interrupt |
| A0  | winf_direction | analoge |
| 8   | DHT22_0 (onboard) | std. digital |
| 9   | DHT22_1 (external | std. digital |
|10   | DHT22_2 (optional)| std. digital |
|11   | DHT22_3 (optional) | std. digital |
|12   | DHT22_4 (optional) | std. digital |


# Software

## usefull Comandlines

arduino --verify weatherstation.ino

arduino --upload weatherstation.ino

## Required Arduino Software version

## Required Arduno Libraries:

### DHT Library
We used version 1.2.3 from: https://github.com/adafruit/DHT-sensor-library

Installed via the arduino package manager

### PciManager
We used version 2.1.0 from: https://github.com/prampec/arduino-pcimanager

Installed via the arduino package manager

### Arduinojson
We used version 5.6.4 from: https://github.com/bblanchon/ArduinoJson

Installed via the arduino package manager

-------------------------------------

# README in yellow box

# RG11 Rain sensor readout Box

MAGIC and FACT are collaborating in utilizing RG11 rain sensors as an add on for the existing weather stations at the ORM on la palma.

## Two RG11 sensors - two SUBD connectors
Two RG11 sensors exist, which are physically identical, but have different settings. It is not yet fully clear, which setting works best, or if maybe combining both measurements gives the best results. The sensors are labelled:

 - "RG11_1" and
 - "RG11_2"

The readout box has two corresponding SUBD-9 male connectors:

This side of the box should be connected to the sensor "RG11_1". Let's call this side the "one-side".

One-side:
<img src="https://cloud.githubusercontent.com/assets/8200858/24101400/8144cc04-0d78-11e7-95a9-7ad0621f1fc4.jpg" width="120">

This side of the box should be connected to the sensor "RG11_2". Let's call it the "two-side".

Two-side:
<img src="https://cloud.githubusercontent.com/assets/8200858/24101401/8145f566-0d78-11e7-8015-11604c0e50a1.jpg" width="120">


# How to modify the arduino firmware

In short:

 * unplug all 4 cables from the yellow box.
 * Open the box
 * remove the "two-side".
 * attach the TTL2USB adaptor
 * connect your laptop via a normal USB cable
 * flash the firmware.

What you'll need:

 * [Hardware requirements](#hardware-requirements)
 * [Install Platformio](#platformio) or
 * [Install Avrdude](#install-avrdude)
 * [Find the path to your arduino](#find-the-path-to-your-arduino)

If you want to:

 * [Change the IP address](#how-to-change-the-ip-address-of-the-yellow-box)
 * [Just upload](#just-upload-the-firmware-without-modifications)

## Hardware requirements

In order to flash an (ArduinoEthernet)[https://www.arduino.cc/en/Main/ArduinoBoardEthernet]
you need an TTL to USB adaptor (like this one)[https://www.arduino.cc/en/Main/USBSerial].
Most modern Arduino boards have the USB connector mounted, but on the fairly old ArduinoEthernet, they saved the space ...

In order to mount the adaptor you'll need to open the yellow box and remove the "two-side" (just pull it a bit up), to make some space for the adaptor.

On this image:
<img src="https://cloud.githubusercontent.com/assets/8200858/24101308/1b31a180-0d78-11e7-9fc2-43d13bd86607.jpg" width="400">

One can see the box before we decided to add a connector for "RG11_2" as well. So the "two-side" was empty. One can easily pull it out and access the ArduinoEthernets SPI connector.

This image should help to understand what way around the adaptor needs to be
<img src="https://cloud.githubusercontent.com/assets/8200858/24102478/68231696-0d7c-11e7-970a-ef21587c6d36.jpg" width="400">

**Note: Danger!** Please take care not to power the device from two different power supplies. As soon as the arduino is connected via the TTL2USB adaptor to your laptop, your laptop powers it. Do not power the yellow box at the same time with the 24V power supply via its barrel connector. In the best case nothing bad happens, but it might well destroy something.

## Find the path to your arduino

Then you should find a new "device file" for this arduino, e.g. like: `ls /dev/tty{USB,ACM}*`. Let's say the arduino shows up as `/dev/ttyACM0` in your case.

## Platformio

http://docs.platformio.org/en/stable/what-is-platformio.html

The normal arduino IDE is just crap for any serious attempt of writing software and no fun at all.

 * Install Anaconda (shame, if you haven't yet)
 * Create a python 2.7 enviroment: `conda create --name py27 python=2.7`
 * Activate the python 2.7 environmen: `source activate py27`
 * Install platformio: `pip install platformio`
 * cd to your yellow_box directory: `cd path/to/weather_station/yellow_box`
 * build and upload: `platformio run --target upload --upload-port /dev/ttyACM0`

## Install Avrdude

The minimum required tool to flash the firmware file into the arduinos memory is
called `avrdude`. In case you happen to have either platformio or the ArduinoIDE
installed, you will already have a copy of `avrdude` on your machine.

Otherwise you can install it on Ubuntu via:

    sudo apt-get install avrdude

---


## How to change the IP address of the yellow Box?

Just edit this line:
https://github.com/fact-project/weather_station/blob/master/yellow_box/src/RG11.cpp#L11

and build and flash the firmware.


## Just upload the firmware without modifications

For your convenience a copy of the current firmware was checked into this repo as well. This is unusual since the firmware binaries are artifacts of the build process. However, it can be a hassle to install the tool chain for building atmega firmware.

You'll find the firmware in `.pioenvs/ethernet/firmware.hex`.

To flash it into the arduino you'll need to find out which device the arduino
is mounted as, c.f [Hardware requirements](#hardware-requirements).

To flash the arduino do:

    avrdude -patmega328p -P/dev/<tty_something> -b115200 -D -Uflash:w:/full/path/to/yellow_box/.pioenvs/ethernet/firmware.hex:i
