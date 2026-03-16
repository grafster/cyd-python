import st7789_base, st7789_ext as st7789
from machine import freq, Pin, SPI


class TestDisplay:
    def rect(self,x,y,w,h,color,fill=False):
        print ('rect {x},{y},{w},{h},{color}')
    def circle(self, x, y, radius, color, fill=False):
        print('circle')
    def line(self, x0, y0, x1, y1, color):
        print(f'line {x0} {y0} {x1} {y1}')
    def triangle(self, x0, y0, x1, y1, x2, y2, color, fill=False):
        print('triangle')
    def color(self, x,y,z):
        print(f'color {x} {y} {z}')
        return 1
    def colour(self, x,y,z):
        print(f'color {x} {y} {z}')
        return 1
    def pixel(self,x,y,color):
        print(f'pixel {x} {y} {color}')
    def fill(self, color):
        print('fill')
    def text(self,x,y,txt,fgcolor,bgcolor):
        print ('text ' + txt)
    def upscaled_text(self,x,y,txt,fgcolor,*,bgcolor=None,upscaling=2):
        print('upscaled text ' + txt)
    def image(self,x,y,filename):
        print('image')



def getTestDisplay():
    return TestDisplay()

def getDisplay():
    display = st7789.ST7789(
        SPI(1, baudrate=40000000, phase=0, polarity=0),
        480, 320,
        reset=Pin(1, Pin.OUT),
        dc=Pin(2, Pin.OUT),
        cs=Pin(15, Pin.OUT),
    )

    display.init(landscape=True,mirror_y=False,inversion=False)
    backlight = Pin(27,Pin.OUT)
    backlight.on()

   # display.fill(display.color(255,0,0))
    #display.fill(display.color(0,255,0))
    #display.fill(display.color(0,0,255))
    return display