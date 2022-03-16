import numpy as np
import States
import window_setup

import PIL
from PIL import Image, ImageTk, ImageColor
import imageio
import numpy as np
import webbrowser
import math
from math import exp


class HexGrid:
    def __init__(self, height, width):
        # Height and width 'must' both be odd, this just makes the grid look nice
        self.height = (height + 1) if (height % 2 == 0) else height
        self.width = (width + 1) if (width % 2 == 0) else width
        # self.grid = np.zeros((height, width), dtype=np.uint)
        self.starting_position = [int(height / 2), int(width / 2)]


class SquareGrid:
    def __init__(self, size_x, size_y):
        self.grid = np.zeros((size_x, size_y), dtype=np.uint)
        self.ants = []
        self.size_x = size_x
        self.size_y = size_y

    def add_ant(self, pos_x, pos_y, direction):
        self.ants.append(States.Ant(pos_x, pos_y, direction))

    def fill_color(self, color):
        for x in range(0, self.size_x-1):
            for y in range(0, self.size_y-1):
                self.grid[x, y] = color

    def run_simulation(self, steps):
        for step in range(0, steps):
            for ant in self.ants:
                self.grid[ant.x, ant.y] = ant.move_ant(self.grid[ant.x, ant.y])
                if ant.direction == 0:  # Up
                    ant.y -= 1
                elif ant.direction == 1:  # Right
                    ant.x += 1
                elif ant.direction == 2:  # Down
                    ant.y += 1
                else:  # Left
                    ant.x -= 1

    def make_image(self, save=False):
        image_grid = np.full((self.size_x, self.size_x, 3), 255, dtype=np.uint8)

        for ant in self.ants:
            image_grid[ant.x, ant.y] = 0xFF0000

        for x in range(0, self.size_x-1):
            for y in range(0, self.size_y-1):
                if self.grid[x, y] == 1:
                    image_grid[x, y] = (0, 0, 0)
                else:
                    image_grid[x, y] = (255, 255, 255)

        img = Image.fromarray(image_grid, 'RGB')
        img.save("test.png")


WIDTH = 500
game = SquareGrid(500, 500)
game.add_ant(250, 250, 2)
game.fill_color(0)
game.run_simulation(160000)
game.make_image()

