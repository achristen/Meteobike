# Meteobike

"Meteobike" is a educational Raspberry Pi Zero Project at the University of Freiburg, Chair of Environmental Meteorology. In our course as part of the minor in meteorology and climatology we develop a system to measure, analyze and visualize the urban heat island of Freiburg. We measure temperature and humidity transcects and tag measurement locations with GPS. The system is battery operated and light, so it can be mounted on bikes. Communication with the Raspberry Pi Zero is enabled via wireless network.

![IMG_meteobike](IMG_meteobike.jpg)

## Overview

The mobile system is assembled using the following components:

![IMG_components](IMG_components.jpg)

## Preparing the Raspberry Pi Zero

Your Raspberry Pi Zero comes with a micro SD cards with the operating sysetm ([Raspbian](https://en.wikipedia.org/wiki/Raspbian Raspbian)) preinstalled. The micro SD is inside the larger SD card adapter. Pull it out and insert it carefully into the card slot.

## Installing the Sensors

### Installing the DHT 22 Sensor

Enter the following commands into the command line on the Raspberry Pi Zero to install the communication with the Adafruit DHT 22 library:

    $ sudo apt-get update
    $ sudo apt-get install build-essential python-dev python-openssl git
    $ git clone https://github.com/adafruit/Adafruit_Python_DHT.git
    $ cd Adafruit_Python_DHT
    $ sudo python setup.py install

Turn off the Raspberry Pi Zero. Disconnect the power cable, the USB cable, and the HDMI cables from the Raspberry Pi Zero. Connect the DHT22 sensor physically using the pre-soldered wires, with the following color coding on the pins of the Raspberry Pi Zero:

| DHT22 T/RH Sensor | Cable Color | Raspberry Pi Zero |
| ------------------ | ----------- | ----------------- |
| PIN 1  | <span style="color: red">Red Cable</span>  | PIN 1 (3V+)
| PIN 2 | <span style="color: orange">Orange Cable</span>  | PIN 7 (GPIO4)
| PIN 3 | (no cable)  |
| PIN 4 | <span style="color: brown">Brown Cable</span>  | PIN 9 (Ground)

Double check if the connection is correct. Then reconnect the USB cable, the HDMI cables, and finally the power cable to the Raspberry Pi Zero. The Raspberry Pi Zero restarts, and the green light flashes.

Once started, test the DHT 22 Sensor with the following commands in Python. First start the Phython environment for Python 2.7 in interactive mode. In Python, enter

    >>> import Adafruit_DHT
    >>> humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22,4)
    >>> print temperature, humidity
  
This will display the currently measured values.

Next, as an exercise you can calculate the vapour pressure using the Clausius-Clapeyron equation. First calculate the saturation vapour pressure in kPa, then convert RH to vapour pressure. Note that temperature needs to be entered in Kelvins.

    >>> import numpy 
    >>> saturation_vappress = 0.6113 * numpy.exp((2501000.0/461.5)*((1.0/273.15)-(1.0/(temperature+273.15))))
    >>> vappress=(humidity/100.0)*saturation_vappress
    >>> print vappress

## Installing the GPS Module

    $ sudo apt-get install gpsd gpsd-clients python-gps
    
    $ sudo systemctl stop serial-getty@ttyS0.service 
    $ sudo systemctl disable serial-getty@ttyS0.service

For the Raspberry Pi Zero we need to enable the serial port on the GPIO pins. Open the "nano" text editor and change the file `config.txt`
    
    $ sudo nano /boot/config.txt
    
Scroll to the the very bottom of the file with the arrow keys an add this on a new line:
    
    enable_uart=1
    
Save and Exit with Strng-O and Strng-X and reboot the Raspberry Pi Zero

Run these commands to use the serial port:
    
    $ sudo killall gpsd 
    $ sudo gpsd /dev/ttyS0 -F /var/run/gpsd.sock

An insert at the very end, but above the line `exit 0` the following command:

    gpsd /dev/ttyS0 -F /var/run/gpsd.sock

This enables that every time the Raspberry Pi Zero is bootet, the command will be executed. You can test the GPS using:

    $ cgps -s
