# Meteobike

## Installing the DHT 22 Sensor



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

An insert at the very end, but above the line `exit` the following command:

    gpsd /dev/ttyS0 -F /var/run/gpsd.sock

This enables that every time the Raspberry Pi Zero is bootet, the command will be executed. You can test the GPS using:

    $ cgps -s
