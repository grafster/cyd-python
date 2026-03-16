
The micropython firmware can be downloaded from 

https://micropython.org/download/ESP32_GENERIC/

The setup.sh script can be used to reflash the Micropython firmware on the devices and copy the example code across.

Display code depends on

https://github.com/antirez/ST77xx-pure-MP.git

The editor used was Thonny

This command may be needed to give a user access to the USB Serial device

sudo usermod -a -G dialout [username]
