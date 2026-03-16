# Drawing function cheat sheet

## Display X & Y Co-ordinates

The display is 480 pixels wide and 320 high

x = 0, y = 0 is the top left of the screen
x = 480, y = 320 is the bottom right of the screen

## Create a colour to use with other functions

display.colour(r, g, b)

| Parameter | Description |
| --- | --- |
|r | Red 0-255 |
|g | Green 0-255 |
|b | Blue 0-255 |

### Example

red = display.colour(255,0,0)

## Set a single pixel

display.pixel(x, y, colour)

| Parameter | Description |
| --- | --- |
| x | screen x |
| y | screen y |
| colour | colour for pixel |

### Example

#Set central pixel white

display.pixel(240,160, display.colour(255,255,255))

# Fill screen with a single colour 

display.fill(color)

| Parameter | Description |
| --- | --- |
| colour | colour for screen |

### Example

#Set whole screen white

display.fill(display.colour(255,255,255))

# Draw an image from the disk

display.image(x, y, filename)

| Parameter | Description |
| --- | --- |
| x | screen x position to display image|
| y | screen y position to display image |
| filename | image file (currently only logo.565 |

### Example

#Draw scout logo at top left of screen

display.image(0, 0, 'logo.565')

# Text

display.text(x,y,txt,fgcolor,bgcolor)

| Parameter | Description |
| --- | --- |
| x | screen x position to display text |
| y | screen y position to display text |
| txt | the text to display |
| fgcolour | the foreground colour for the text |
| bgcolour | the background colour for the text |

### Example

#draw 'hello' with white text on black background

display.text(10,295, 'hello', display.color(255,255,255), display.color(0,0,0))

# Large text

 display.upscaled_text(x,y,txt,fgcolor,bgcolor=None,upscaling=2)
 
| Parameter | Description |
| --- | --- |
| x | screen x position to display text |
| y | screen y position to display text |
| txt | the text to display |
| fgcolour | the foreground colour for the text |
| bgcolour | the background colour for the text (optional) |
| upscaling | factor to scale up by, defaults to 2x size - Named parameter |


### Example

display.upscaled_text(20, 20, 'Hello', display.color(255,255,255),upscaling=3)

# Circles 

display.circle(x, y, radius, color, fill=False)

| Parameter | Description |
| --- | --- |
| x | screen x position to display circle |
| y | screen y position to display circle |
| radius | radius of circle in pixels |
| colour | the colour for the circle |
| fill | whether the circle should be filled with colour |

### Example

#Draw a blue circle at 150, 50 with a radius of 30, in blue and filled in

display.circle(150, 50, 30, display.color(0,0,255), True)

# Rectangles

display.rect(x,y,w,h,color,fill=False)

| Parameter | Description |
| --- | --- |
| x | screen x position to display rectangle |
| y | screen y position to display rectangle |
| w | width of the rectangle in pixels |
| h | height of rectangle in pixels |
| colour | the colour for the rectangle |
| fill | whether the rectangle should be filled with colour |

### Example

#draw a red rectangle, starting at 20, 20 - 100 wide and 50 tall

display.rect(20,20, 100, 50, display.color(255,0,0), True)

# Draw a single Line

display.line(x0, y0, x1, y1, color)


| Parameter | Description |
| --- | --- |
| x0 | screen x position to start the line |
| y0 | screen y position to start the line |
| x1 | screen x position to end the line |
| y1 | screen y position to end the line |
| colour | the colour for the line |

### Example

display.line(20, 100, 400, 120, display.color(0,255,0))

# Triangle

display.triangle(x0, y0, x1, y1, x2, y2, color, fill=False):

| Parameter | Description |
| --- | --- |
| x0 | screen x position of 1st corner of the triangle |
| y0 | screen y position of 1st corner of the triangle |
| x1 | screen x position of 2nd corner of the triangle |
| y1 | screen y position of 2nd corner of the triangle |
| x1 | screen x position of 3rd corner of the triangle |
| y1 | screen y position of 3rd corner of the triangle |
| colour | the colour for the triangle |
| fill | whether the triangle should be filled with colour |

### Example

#draw a cyan triangle

display.triangle(200, 150, 80, 280, 320, 280, display.color(0,255,255), True)
