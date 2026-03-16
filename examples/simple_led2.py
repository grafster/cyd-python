from machine import Pin
from time import sleep

class Led:
    def __init__(self):
        self.led1 = Pin(4, Pin.OUT) # RED
        self.led2 = Pin(16, Pin.OUT) #BLUE 
        self.led3 = Pin(17, Pin.OUT) # GREEN
    
    def setColor(self, r, g, b):
        #self.led1.value(1 - (r / 256))
        #self.led2.value(1 - (b / 256))
        #self.led3.value(1 - (g / 255))
        self.led1.value(0)
        self.led2.value(1)
        self.led3.value(1)
        

led = Led()

while True:
    print('red')
    led.setColor(255,0,0)
    sleep(1)

print('green')
led.setColor(0,255,0)
sleep(1)
print('blue')
led.setColor(0,0,255)
sleep(1)
print('ornge')
led.setColor(255, 165, 0) #orange
sleep(1)
print('purple')
led.setColor(128, 0, 128) #purple
sleep(1)


