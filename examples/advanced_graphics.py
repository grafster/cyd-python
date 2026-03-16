"""
Attractive patterns for the Cheap Yellow Display (CYD)
480x320 pixels - MicroPython

Assumes you have a display object `tft` with these methods:
    tft.circle(x, y, r, color, filled=True)
    tft.line(x1, y1, x2, y2, color)
    tft.text(font, text, x, y, color)
    tft.pixel(x, y, color)
    tft.triangle(x1,y1, x2,y2, x3,y3, color, filled=True)
    tft.rect(x, y, w, h, color)   # or tft.rect(...)

Adjust the driver calls to match your specific library (ili9341, st7789, etc.)
"""

import math
import time
import st7789_base, st7789_ext as st7789
from machine import freq, Pin, SPI
from setup_display import getDisplay

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

class TestTFT:
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
        return 42
    def pixel(self,x,y,color):
        print(f'pixek {x} {y} {color}')
    
        
# ── Dimensions ────────────────────────────────────────────────────────────────
W = 480
H = 320
CX = W // 2
CY = H // 2          # centre of the screen




#tft = TestTFT()

# ── Colour helpers (RGB565) ────────────────────────────────────────────────────
def rgb(r, g, b):
    """Pack (r,g,b) 0-255 values into RGB565."""
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 2) | (b >> 3)

def debugOut(tft, text):
    tft.text(10,295,text, tft.color(255,255,255), tft.color(0,0,0))
    tft.text(10,305,text, tft.color(0,0,0), tft.color(255,255,255))


def hue_to_rgb565(display, h):
    """h in 0..359 → RGB565 colour."""
    h = h % 360
    s, v = 1.0, 1.0
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c
    if   h < 60:  r,g,b = c,x,0
    elif h < 120: r,g,b = x,c,0
    elif h < 180: r,g,b = 0,c,x
    elif h < 240: r,g,b = 0,x,c
    elif h < 300: r,g,b = x,0,c
    else:         r,g,b = c,0,x
    return display.color(int((r+m)*255), int((g+m)*255), int((b+m)*255))

def getPalette(tft):
    # Palette
    BLACK   = tft.color(0,   0,   0)
    WHITE   = tft.color(255, 255, 255)
    RED     = tft.color(220,  30,  30)
    GREEN   = tft.color(  0, 200,  80)
    BLUE    = tft.color( 20,  80, 220)
    CYAN    = tft.color(  0, 220, 220)
    MAGENTA = tft.color(220,   0, 220)
    YELLOW  = tft.color(255, 220,   0)
    ORANGE  = tft.color(255, 130,   0)
    PURPLE  = tft.color(130,   0, 200)
    PINK    = tft.color(255,  80, 160)
    TEAL    = tft.color(  0, 180, 160)

    PALETTE = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, MAGENTA, PINK, TEAL]
    return PALETTE


# ══════════════════════════════════════════════════════════════════════════════
# Pattern 1 – Rainbow Bullseye
# ══════════════════════════════════════════════════════════════════════════════
def pattern_bullseye(tft):
    tft.rect(0, 0, W, H, tft.color(0,0,0))
    max_r = min(CX, CY)

    rings = 30
    for i in range(rings, 0, -1):
        r = int(max_r * i / rings)
        color = hue_to_rgb565(tft, int(360 * i / rings))
        tft.circle(CX, CY, r, color, True)


# ══════════════════════════════════════════════════════════════════════════════
# Pattern 2 – Starfield / Web of Lines
# ══════════════════════════════════════════════════════════════════════════════
def pattern_starburst(tft):
    tft.rect(0, 0, W, H, tft.color(0,0,0))
    spokes = 72
    rings  = 8
    max_r  = min(CX, CY) - 4
    for ring in range(1, rings + 1):
        r = int(max_r * ring / rings)
        color = hue_to_rgb565(tft, int(360 * ring / rings))
        for s in range(spokes):
            ang = 2 * math.pi * s / spokes
            x1 = int(CX + r * math.cos(ang))
            y1 = int(CY + r * math.sin(ang))
            ang2 = 2 * math.pi * (s + 1) / spokes
            x2 = int(CX + r * math.cos(ang2))
            y2 = int(CY + r * math.sin(ang2))
            tft.line(x1, y1, x2, y2, color)
    # Spokes from centre
    for s in range(spokes):
        ang = 2 * math.pi * s / spokes
        x = int(CX + max_r * math.cos(ang))
        y = int(CY + max_r * math.sin(ang))
        tft.line(CX, CY, x, y, hue_to_rgb565(tft, int(360 * s / spokes)))


# ══════════════════════════════════════════════════════════════════════════════
# Pattern 3 – Plasma / Moiré Dots
# ══════════════════════════════════════════════════════════════════════════════
def pattern_plasma(tft):
    """Colourful plasma effect drawn with pixels (slow but gorgeous)."""
    tft.rect(0, 0, W, H, tft.color(0,0,0))
    step = 4          # increase for speed, decrease for detail
    t = 0.0
    for y in range(0, H, step):
        for x in range(0, W, step):
            v = (math.sin(x / 20.0 + t) +
                 math.sin(y / 20.0 + t) +
                 math.sin((x + y) / 30.0 + t) +
                 math.sin(math.sqrt(x*x + y*y) / 20.0 + t))
            hue = int((v + 4) / 8 * 360)
            color = hue_to_rgb565(tft, hue)
            # Fill a small block so it's visible at the step size
            tft.rect(x, y, step, step, color)


# ══════════════════════════════════════════════════════════════════════════════
# Pattern 4 – Geometric Tile (triangles)
# ══════════════════════════════════════════════════════════════════════════════
def pattern_triangle_tiles(tft):
    BLACK = tft.color(0,0,0)
    tft.rect(0, 0, W, H, BLACK)
    size = 40          # triangle cell size
    col_idx = 0
    row = 0
    y = 0
    PALETTE = getPalette(tft)
    while y < H:
        x = 0
        col = 0
        while x < W + size:
            color1 = PALETTE[col_idx % len(PALETTE)]
            color2 = PALETTE[(col_idx + 3) % len(PALETTE)]
            # Two triangles make a parallelogram tile
            tft.triangle(x, y,
                         x + size, y,
                         x + size // 2, y + size,
                         color1, True)
            tft.triangle(x + size, y,
                         x + size + size // 2, y + size,
                         x + size // 2, y + size,
                         color2, True)
            col_idx += 1
            x += size
            col += 1
        y += size
        row += 1
        col_idx += 1  # shift hue each row


# ══════════════════════════════════════════════════════════════════════════════
# Pattern 5 – Nested Squares (spiral illusion)
# ══════════════════════════════════════════════════════════════════════════════
def pattern_nested_squares(tft):
    BLACK = tft.color(0,0,0)
    tft.rect(0, 0, W, H, BLACK)
    steps = 30
    for i in range(steps, 0, -1):
        margin = int(i * min(CX, CY) / steps)
        x0 = CX - margin
        y0 = CY - margin
        w  = margin * 2
        h  = margin * 2
        color = hue_to_rgb565(tft, int(360 * i / steps))
        tft.rect(x0, y0, w, h, color)
        # Thin black border to separate rings
        tft.rect(x0, y0, w, 2, BLACK)
        tft.rect(x0, y0 + h - 2, w, 2, BLACK)
        tft.rect(x0, y0, 2, h, BLACK)
        tft.rect(x0 + w - 2, y0, 2, h, BLACK)


# ══════════════════════════════════════════════════════════════════════════════
# Pattern 6 – Lissajous Curve
# ══════════════════════════════════════════════════════════════════════════════
def pattern_lissajous(tft, a=3, b=4, delta=0):
    """Classic XY-oscilloscope figure."""
    BLACK = tft.color(0,0,0)
    tft.rect(0, 0, W, H, BLACK)
    margin = 20
    rx = CX - margin
    ry = CY - margin
    steps = 800
    prev_x, prev_y = None, None
    for i in range(steps + 1):
        t = 2 * math.pi * i / steps
        px = int(CX + rx * math.sin(a * t + delta))
        py = int(CY + ry * math.sin(b * t))
        color = hue_to_rgb565(tft, int(360 * i / steps))
        if prev_x is not None:
            tft.line(prev_x, prev_y, px, py, color)
        prev_x, prev_y = px, py


# ══════════════════════════════════════════════════════════════════════════════
# Pattern 7 – Spirograph
# ══════════════════════════════════════════════════════════════════════════════
def pattern_spirograph(tft, R=120, r=35, d=90):
    """Hypotrochoid (inner gear rolling inside outer)."""
    BLCK = tft.color(0,0,0)
    tft.rect(0, 0, W, H, BLCK)
    steps = 1500
    prev_x, prev_y = None, None
    for i in range(steps + 1):
        t = 2 * math.pi * i / steps * (r / gcd(R, r))
        px = int(CX + (R - r) * math.cos(t) + d * math.cos((R - r) / r * t))
        py = int(CY + (R - r) * math.sin(t) - d * math.sin((R - r) / r * t))
        color = hue_to_rgb565(tft, int(360 * i / steps))
        if prev_x is not None:
            tft.line(prev_x, prev_y, px, py, color)
        prev_x, prev_y = px, py


# ══════════════════════════════════════════════════════════════════════════════
# Pattern 8 – Sunburst / Flag Segments
# ══════════════════════════════════════════════════════════════════════════════
def pattern_sunburst(tft):
    BLACK = tft.color(0,0,0)
    tft.rect(0, 0, W, H, BLACK)
    segments = 24
    max_r = int(math.sqrt(CX**2 + CY**2)) + 10   # reach corners
    for s in range(segments):
        ang1 = 2 * math.pi * s / segments
        ang2 = 2 * math.pi * (s + 1) / segments
        ang_mid = (ang1 + ang2) / 2
        # Tip of the wedge (past screen edge)
        tx = int(CX + max_r * math.cos(ang_mid))
        ty = int(CY + max_r * math.sin(ang_mid))
        # Two base corners near centre
        bx1 = int(CX + 5 * math.cos(ang1))
        by1 = int(CY + 5 * math.sin(ang1))
        bx2 = int(CX + 5 * math.cos(ang2))
        by2 = int(CY + 5 * math.sin(ang2))
        # Fill with far corners
        ex1 = int(CX + max_r * math.cos(ang1))
        ey1 = int(CY + max_r * math.sin(ang1))
        color = hue_to_rgb565(tft, int(360 * s / segments))
        tft.triangle(CX, CY, ex1, ey1, tx, ty, color, True)
        tft.triangle(CX, CY, tx, ty,
                     int(CX + max_r * math.cos(ang2)),
                     int(CY + max_r * math.sin(ang2)),
                     color, True)


# ══════════════════════════════════════════════════════════════════════════════
# Pattern 9 – Checker with circles
# ══════════════════════════════════════════════════════════════════════════════
def pattern_checker_dots(tft):
    BLACK = tft.color(0,0,0)
    WHITE = tft.color(255,255,255)
    PALETTE = getPalette(tft)
    cell = 40
    cols = W // cell + 1
    rows = H // cell + 1
    for row in range(rows):
        for col in range(cols):
            x = col * cell
            y = row * cell
            bg = BLACK if (row + col) % 2 == 0 else WHITE
            tft.rect(x, y, cell, cell, bg)
            # Contrasting dot in each cell
            dot_color = PALETTE[(row * cols + col) % len(PALETTE)]
            tft.circle(x + cell // 2, y + cell // 2, cell // 2 - 6, dot_color, True)


# ══════════════════════════════════════════════════════════════════════════════
# Pattern 10 – Animated Bouncing Rainbow Wave (runs in a loop)
# ══════════════════════════════════════════════════════════════════════════════
def pattern_wave_animate(tft, frames = 120):
    """Draws an animated sine wave banner. Runs for `frames` iterations."""
    amplitude = 80
    wavelength = 80
    speed = 8
    thickness = 6
    BLACK = tft.color(0,0,0)

    for frame in range(frames):
        tft.rect(0, 0, W, H, BLACK)
        offset = frame * speed
        for x in range(W):
            y = int(CY + amplitude * math.sin(2 * math.pi * (x + offset) / wavelength))
            color = hue_to_rgb565(tft, (x + offset * 2) % 360)
            for dy in range(-thickness, thickness + 1):
                yy = y + dy
                if 0 <= yy < H:
                    tft.pixel(x, yy, color)


# ══════════════════════════════════════════════════════════════════════════════
# Main demo – cycle through every pattern
# ══════════════════════════════════════════════════════════════════════════════
def run_demo(tft):
    patterns = [
        ("Bullseye",        lambda: pattern_bullseye(tft)),
        ("Starburst",       lambda: pattern_starburst(tft)),
        ("Plasma",          lambda: pattern_plasma(tft)),
        ("Triangle Tiles",  lambda: pattern_triangle_tiles(tft)),
        ("Nested Squares",  lambda: pattern_nested_squares(tft)),
        ("Lissajous 3:4",   lambda: pattern_lissajous(tft, 3, 4, math.pi/4)),
        ("Spirograph",      lambda: pattern_spirograph(tft)),
        ("Sunburst",        lambda: pattern_sunburst(tft)),
        ("Checker Dots",    lambda: pattern_checker_dots(tft)),
        ("Wave",            lambda: pattern_wave_animate(tft, frames=60)),
    ]
    while True:
        for name, draw in patterns:
            debugOut(tft, name)
            #print("Drawing:", name)
            draw()
            time.sleep(3)          # pause 3 seconds between patterns
            tft.fill(tft.color(0,0,0))
            
    
def creteDisply():
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
    #debugOut(display, 'bull')
    return display

#pattern_checker_dots(display)


#tft = TestTFT()

tft = getDisplay()
run_demo(tft)

while True:
    pattern_bullseye(tft)
    tft.fill(tft.color(0,0,0))
    pattern_starburst(tft)
    tft.fill(tft.color(0,0,0))
    pattern_triangle_tiles(tft)
    pattern_plasma(tft)
    tft.fill(tft.color(0,0,0))
    pattern_spirograph(tft)
    pattern_nested_squares(tft)
    pattern_lissajous(tft)
    tft.fill(tft.color(0,0,0))
    debugOut(tft, 'loop')
    sleep(2)
# ── Entry point ───────────────────────────────────────────────────────────────
# Replace this block with your own display initialisation.
# Example using ili9341 driver:
#
#   from machine import Pin, SPI
#   import ili9341
#   spi = SPI(1, baudrate=40_000_000, sck=Pin(14), mosi=Pin(13))
#   tft = ili9341.ILI9341(spi, cs=Pin(15), dc=Pin(2), rst=Pin(4),
#                          width=480, height=320, rotation=0)
#   tft.fill(BLACK)
#   run_demo(tft)
#
# Or for st7789:
#   import st7789
#   tft = st7789.ST7789(spi, 320, 480, ...)
#
# Uncomment and adapt the two lines below when running on hardware:
# import your_display_driver as driver
# run_demo(driver.tft)