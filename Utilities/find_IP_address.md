Finding IP Addresses of Raspberry PIs
===============

In our course, we have had the issue that the IP addresses of the Raspberry Pis change after being powered down and up again. To avoid this problem from happening, ensure that the hostname of the Raspberry Pi is changed before the Pi connects to the network. 

If the IP address has changed and it is not possible to connect the Raspberry Pi to a monitor and check its IP address manually, it can be found using the Raspberry Pi hostname from another computer on the network. Assuming the hostname is "raspberry01":

From Linux: `ping raspberry01`

From Windows: `ping raspberry01`

From macOS: `ping raspberry01.local`

This will ping the Pi and return the IP address. Once the systems have been pinged, all IP addresses on the network can be listed using `arp -a`.
