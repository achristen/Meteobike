# Meteobike

## Installing the DHT 22 Sensor

Enter the following commands into the command line on the Raspberry Pi Zero to install the communication with the Adafruit DHT 22 library:

    $ sudo apt-get update
    $ sudo apt-get install build-essential python-dev python-openssl git
    $ git clone https://github.com/adafruit/Adafruit_Python_DHT.git
    $ cd Adafruit_Python_DHT
    $ sudo python setup.py install

Turn off the Raspberry Pi Zero. Disconnect Power and all cables. Connect the DHT 22 Sensor physically with the following PINs of the Raspberry Pi Zero:

* DHT 22 T/RH Sensor PIN 1 <--> <span style="color: red">Red Cable</span> <--> Raspberry PIN 1 (3V+)
* DHT 22 T/RH Sensor PIN 2 <--> <span style="color: orange">Orange Cable</span> <--> Raspberry PIN 7 (GPIO4)
* DHT 22 T/RH Sensor PIN 3 (no cable attached)
* DHT 22 T/RH Sensor PIN 4 <--> <span style="color: brown">Brown Cable</span> <--> Raspberry PIN 9 (Ground)

Reconnect all cables. Restart the Raspberry Pi Zero.

Test the DHT 22 Sensor with the following commands. First start Python in interactive mode:

    $ sudo python 
    
Then enter

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
