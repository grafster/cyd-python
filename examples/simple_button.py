from time import sleep
from machine import Pin

print ('listening for keypress')

key = Pin(0, Pin.IN)

count = 0
while True:
    if (key.value() == 0):
        count += 1
        print('key pressed ' + str(count) + ' times')
        sleep(1)
