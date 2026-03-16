from setup_display import getDisplay
import time, random 

def displayImage(display):
    # If the file logo.565 was lodaded in the device, show
    # it on the screen.
    for i in range(20):
        x = random.getrandbits(6)
        y = random.getrandbits(6)
        display.image(x,y,"logo.565")

start = time.ticks_ms()
print ("strt time is " + str(start))
print (random.randint(0, 22))

# Test colors
COLORS = (
    ('Red', 0xFF, 0, 0),
    ('Green', 0, 0xFF, 0),
    ('Blue', 0, 0, 0xFF),
    ('Yellow', 0xFF, 0xFF, 0),
    ('Magenta', 0xFF, 0, 0xFF),
    ('Cyan', 0, 0xFF, 0xFF)
)

width = 480
height = 320

display = getDisplay()

white = display.color(255,255,255)
blck = display.color(0,0,0)



#  upscaled_text(x,y,txt,fgcolor,*,bgcolor=None,upscaling=2):

def textExample():
    upscaled = ["", "START","TEST","NOW..."]
    for i in range(4):
        display.upscaled_text(30*i,30*i,upscaled[i],display.color(15+80*i,15+80*i,15+80*i),upscaling=3)


def textExample2(text):
    # Write some text.
    x = 0
    y = 0
    for i in range(20):
        x += 2
        y += 10
        display.text(x,y, text ,white , blck)

def testRectangles():
    # Random rectangles, empty and full.
    # rect(x,y,w,h,color,fill=False):
    full = True
    for i in range(500):
        fill_color = display.color(random.getrandbits(8),
                                   random.getrandbits(8),
                                   random.getrandbits(8))
        display.rect(
            random.randint(0, width),
            random.randint(0, height),
            random.getrandbits(6),
            random.getrandbits(6),
            fill_color,
            full)
        full = not full # Switch between full and empty circles.

def testCircles():    
    # Random circles, empty and full.
    full = True
    for i in range(50):
        fill_color = display.color(random.getrandbits(8),
                                   random.getrandbits(8),
                                   random.getrandbits(8))
        display.circle(
            random.randint(0, width),
            random.randint(0, height),
            random.getrandbits(6),
            fill_color,
            full)
        full = not full # Switch between full and empty circles.

def testLines():
    full = True

    for i in range(100):
        fill_color = display.color(random.getrandbits(8),
                                   random.getrandbits(8),
                                   random.getrandbits(8))
        display.line(
            random.randint(0, width),
            random.randint(0, height),
            random.randint(0, width),
            random.randint(0, height),
            fill_color)

def testTriangles(count):
    full = True
    for i in range(count):
        fill_color = display.color(random.getrandbits(8),
                                   random.getrandbits(8),
                                   random.getrandbits(8))
        display.triangle(
            random.randint(0, width),
            random.randint(0,height),
            random.getrandbits(7),
            random.getrandbits(7),
            random.getrandbits(7),
            random.getrandbits(7),
            fill_color, full)
        full = not full # Switch between full and empty triangles.


# START OF PROGRAM


while True:
    textExample()

    time.sleep (5)

    textExample2('Hello Scouts')

    time.sleep(5)
    display.fill(blck)

    # Random points using raw pixels.
    for i in range(2000):
        x = random.randint(0, width)
        y = random.randint(0, height)
        display.pixel(x,y,white)

    time.sleep(3)
    
    displayImage(display)
    
    testRectangles()

    time.sleep(3)

    display.fill(blck)
    
    testCircles()

    time.sleep(3)
    display.fill(blck)
    
    testLines()

    # Random lines
    display.fill(blck)
    time.sleep(3)
    
    testTriangles(20)
    time.sleep(3)
