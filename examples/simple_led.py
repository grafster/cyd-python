from machine import Pin
from time import sleep

led1 = Pin(4, Pin.OUT) # RED
led2 = Pin(16, Pin.OUT) #BLUE 
led3 = Pin(17, Pin.OUT) # GREEN

while True:
    led1.value(0)
    sleep(0.5)
    led1.value(1)
    sleep(0.5)
    led2.value(0)
    sleep(0.5)
    #led2.value(1)
    #sleep(0.5)
    led3.value(0)
    sleep(0.5)
    led3.value(1)
    led2.value(1)
    sleep(0.5)
    
