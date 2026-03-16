esptool --port /dev/ttyUSB0 erase_flash
esptool --port /dev/ttyUSB0 --baud 460800 write_flash 0x1000 ~/Downloads/ESP32_GENERIC-20251209-v1.27.0.bin 
sleep 5
mpremote cp ~/dev/examples/* :

