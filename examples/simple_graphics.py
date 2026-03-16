# Simple graphics example

from setup_display import getDisplay

display = getDisplay()

# fill the screen with light blue
display.fill(display.colour(20,128,128))

text = 'test writing some text'
display.text(10,295,text, display.color(255,255,255), display.color(0,0,0))
display.text(10,305,text, display.color(0,0,0), display.color(255,255,255))

# draw a red rectangle, starting at 20, 100 wide and 50 tall

display.rect(20,20, 100, 50, display.color(255,0,0), True)

# draw a blue circle
display.circle(150, 50, 30, display.color(0,0,255), True)

# draw a line
display.line(20, 100, 400, 120, display.color(0,255,0))

# save the colour red in a variable
red = display.color(255,0,0)

#set 4 pixels to be red
display.pixel(470,100, red)
display.pixel(471,100, red)
display.pixel(470,101, red)
display.pixel(471,101, red)

#draw a cyan triangle
display.triangle(200, 150, 80, 280, 320, 280, display.color(0,255,255), True)

#draw big text
text = ["Thats","all","folks..."]
for i in range(3):
    display.upscaled_text(20 + (30*i), 20 + (30*i), text[i], display.color(255,255,255),upscaling=3)

#draw scouts logo image
display.image (300, 20, "logo.565")
