"""
Conway's Game of Life — Cheap Yellow Display (CYD)
480 x 320 pixels, 10 x 10 pixel cells → 48 x 32 grid
MicroPython
"""

import random
import time
from setup_display import getDisplay

tft = getDisplay()


# ── Display dimensions & cell size ───────────────────────────────────────────
W = 480
H = 320
CELL      = 20
COLS      = W // CELL   # 48
ROWS      = H // CELL   # 32

BLACK     = tft.color(  0,   0,   0)
ALIVE     = tft.color( 80, 220, 120)   # bright green cells
DEAD      = BLACK
GRID_LINE = tft.color( 20,  20,  20)   # very subtle grid (set to DEAD to hide)

# ── Grid helpers ──────────────────────────────────────────────────────────────
def make_grid():
    """Return a flat list of 0/1 values, length COLS*ROWS."""
    return [0] * (COLS * ROWS)

def idx(col, row):
    return row * COLS + col

def randomise(grid, density=0.35):
    """Fill grid randomly; ~density fraction of cells start alive."""
    for i in range(len(grid)):
        grid[i] = 1 if random.random() < density else 0

def count_neighbours(grid, col, row):
    """Toroidal (wrap-around) neighbour count."""
    total = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            r = (row + dr) % ROWS
            c = (col + dc) % COLS
            total += grid[idx(c, r)]
    return total

def step(grid, next_grid):
    """Advance one generation. Writes into next_grid in-place."""
    for row in range(ROWS):
        for col in range(COLS):
            n = count_neighbours(grid, col, row)
            alive = grid[idx(col, row)]
            if alive:
                next_grid[idx(col, row)] = 1 if n in (2, 3) else 0
            else:
                next_grid[idx(col, row)] = 1 if n == 3 else 0

def grids_equal(a, b):
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True

# ── Drawing ───────────────────────────────────────────────────────────────────
def draw_full(tft, grid):
    """Redraw every cell (used on first frame)."""
    for row in range(ROWS):
        for col in range(COLS):
            color = ALIVE if grid[idx(col, row)] else DEAD
            tft.rect(col * CELL, row * CELL, CELL, CELL, color)

def draw_diff(tft, old_grid, new_grid):
    """Only redraw cells that changed (much faster)."""
    for row in range(ROWS):
        for col in range(COLS):
            i = idx(col, row)
            if old_grid[i] != new_grid[i]:
                color = ALIVE if new_grid[i] else DEAD
                tft.rect(col * CELL, row * CELL, CELL, CELL, color)

def count_alive(grid):
    return sum(grid)

# ── Main loop ─────────────────────────────────────────────────────────────────
def run(tft, max_generations=None, stagnation_limit=10, pause_ms=60):
    """
    Run Game of Life indefinitely (or up to max_generations).

    Restarts automatically when:
      - Population dies out
      - Grid stops changing for `stagnation_limit` generations

    tft          : your display object
    max_gens     : stop after this many generations (None = forever)
    stagnation_limit : restart after this many identical generations
    pause_ms     : milliseconds between frames (lower = faster)
    """
    grid      = make_grid()
    next_grid = make_grid()
    prev_grid = make_grid()

    generation   = 0
    stagnant     = 0
    run_number   = 1

    while True:
        # ── (Re)start ─────────────────────────────────────────────────────
        print("Run {}: randomising grid...".format(run_number))
        randomise(grid)
        draw_full(tft, grid)
        generation = 0
        stagnant   = 0

        while True:
            # Advance one generation
            step(grid, next_grid)
            generation += 1

            # Draw only changed cells
            draw_diff(tft, grid, next_grid)

            # Swap buffers (copy next → grid without allocation)
            for i in range(len(grid)):
                prev_grid[i] = grid[i]
                grid[i]      = next_grid[i]

            alive = count_alive(grid)
            print("Gen {:4d}  alive: {:4d}  run: {}".format(
                generation, alive, run_number))

            # ── Restart conditions ─────────────────────────────────────
            if alive == 0:
                print("Population extinct — restarting.")
                break

            if grids_equal(grid, prev_grid):
                stagnant += 1
                if stagnant >= stagnation_limit:
                    print("Stagnated for {} gens — restarting.".format(
                        stagnation_limit))
                    break
            else:
                stagnant = 0

            if max_generations and generation >= max_generations:
                print("Max generations reached — restarting.")
                break

            time.sleep_ms(pause_ms)

        run_number += 1

  

run (tft)
# ── Entry point ───────────────────────────────────────────────────────────────
# Initialise your display driver here, then call run(tft).
#
# Example (ili9341):
#   from machine import Pin, SPI
#   import ili9341
#   spi = SPI(1, baudrate=40_000_000, sck=Pin(14), mosi=Pin(13))
#   tft = ili9341.ILI9341(spi, cs=Pin(15), dc=Pin(2), rst=Pin(4),
#                          width=480, height=320)
#   tft.fill(0)
#   run(tft)