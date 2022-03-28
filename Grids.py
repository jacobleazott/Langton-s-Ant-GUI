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
import pprint
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import logging
from hexalattice.hexalattice import *

logging.basicConfig(filename='beasts.log', level=logging.INFO, filemode='w',
                    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
                    datefmt='%H:%M:%S')


def plot_hex(ax, i1, i2, c='#888888'):
    """Draw the hexagon indexed at (i2, i1) in colour c on Axes ax."""

    # Scaling factor: separate the centre of the hexagons by this amount.
    s = 1
    # Hexagon side-length.
    a = s / np.sqrt(3)
    # Hexagon centre (cx, cy), and vertex coordinates.
    cx, cy = s * i1 + s / 4 * (-1) ** (i2 % 2), 3 * a / 2 * i2
    x1, y1 = cx, cy + a
    x2, y2 = cx + s / 2, cy + a / 2
    x3, y3 = cx + s / 2, cy - a / 2
    x4, y4 = cx, cy - a
    x5, y5 = cx - s / 2, cy - a / 2
    x6, y6 = cx - s / 2, cy + a / 2
    hexagon = plt.Polygon(((x1, y1), (x2, y2), (x3, y3), (x4, y4),
                           (x5, y5), (x6, y6)), fc=c)
    ax.add_patch(hexagon)


class Grid:
    def __init__(self, size_x, size_y):
        self.ants = []
        self.states = None
        self.size_x = size_x
        self.size_y = size_y
        self.grid = np.zeros((size_x, size_y), dtype=np.uint8)

    def add_ant(self, pos_x, pos_y, direction):
        self.ants.append(States.Ant(pos_x, pos_y, direction, states=self.states))

    def run_simulation(self, steps):
        return

    def make_image(self, save=False):
        return


class SquareGrid(Grid):
    def __init__(self, size_x, size_y):
        Grid.__init__(self, size_x, size_y)
        self.states = States.StateMachine()
        self.states.add_state_chunk(state=0, color=0, next_color=1, turn=3, next_state=1, sides=4)
        self.states.add_state_chunk(state=0, color=1, next_color=1, turn=3, next_state=1, sides=4)
        self.states.add_state_chunk(state=1, color=0, next_color=1, turn=1, next_state=1, sides=4)
        self.states.add_state_chunk(state=1, color=1, next_color=0, turn=0, next_state=0, sides=4)

    def run_simulation(self, steps):
        logging.info("Beginning Simulation")
        for step in range(0, steps):
            for ant in self.ants:
                self.grid[ant.y, ant.x] = ant.move_ant(self.grid[ant.y, ant.x])
                if ant.direction == 0:  # Up
                    ant.y -= 1
                elif ant.direction == 1:  # Right
                    ant.x += 1
                elif ant.direction == 2:  # Down
                    ant.y += 1
                else:  # Left
                    ant.x -= 1
        logging.info("Finished Simulation")

    def make_image(self, save=False):
        logging.info("Begin Image Processing")
        image_grid = np.full((self.size_y, self.size_x, 3), 0, dtype=np.uint8)

        image_grid[self.grid == 0] = (255, 255, 255)
        image_grid[self.grid == 1] = (0, 0, 0)

        for ant in self.ants:
            image_grid[ant.y, ant.x] = (255, 0, 0)

        img = Image.fromarray(image_grid, 'RGB')
        img.save("test.png")
        logging.info("Finished Image Processing")


class HexGrid(Grid):
    def __init__(self, size_x, size_y, states=None):
        Grid.__init__(self, size_x, size_y)
        # Height and width 'must' both be odd, this just makes the grid look nice
        # Grid.__init__(self, (size_x + 1) if (size_x % 2 == 0) else size_x,
        #               (size_y + 1) if (size_y % 2 == 0) else size_y)
        if states is None:
            self.states = States.StateMachine()
            self.states.add_state_chunk(state=0, color=0, next_color=1, turn=1, next_state=0, sides=6)
            self.states.add_state_chunk(state=0, color=1, next_color=0, turn=5, next_state=0, sides=6)
        else:
            self.states = states

    def run_simulation(self, steps):
        logging.info("Beginning Simulation")
        for step in range(0, steps):
            for ant in self.ants:
                #print(ant.x, ant.y, ant.direction)
                self.grid[ant.x, ant.y] = ant.move_ant(self.grid[ant.x, ant.y])
                # print(ant.x, ant.y, ant.direction)
                if ant.direction == 0:  # Right
                    # print("right")
                    ant.x += 1
                    # ant.y += 0
                elif ant.direction == 1:  # Down Right
                    ant.x += (ant.y + 1) % 2
                    ant.y += -1
                elif ant.direction == 2:  # Down Left
                    ant.x += -(ant.y % 2)
                    ant.y += -1
                elif ant.direction == 3:  # Left
                    ant.x += -1
                    # ant.y += 0
                elif ant.direction == 4:  # Up Left
                    ant.x += -(ant.y % 2)
                    ant.y += 1
                else:  # Up Right
                    ant.x += (ant.y + 1) % 2
                    ant.y += 1
                print(ant.x, ant.y, (ant.direction+3)%6)
                # print(ant.x, ant.y, ant.direction)

        logging.info("Finished Simulation")

    def make_image(self, save=False):
        """
        image_grid = np.full((self.size_x*self.size_y, 3), 0, dtype=np.uint8)

        self.grid = np.swapaxes(self.grid, 0, 0)

        self.grid = self.grid.flatten()

        image_grid[self.grid == 0] = (0, 0, 0)
        image_grid[self.grid == 1] = (1, 1, 1)
        image_grid[self.grid == 2] = (1, 0, 1)
        image_grid[self.grid == 3] = (0, 1, 0)
        image_grid[self.grid == 4] = (0, 0, 1)
        image_grid[self.grid == 5] = (0, 1, 1)
        image_grid[self.grid == 6] = (1, 1, 0)


        # for ant in self.ants:
        #     image_grid[ant.x * ant.y] = (1, 0, 0)


        logging.info("Begin Image Processing")

        hex_centers, _ = create_hex_grid(nx=self.size_x,
                                         ny=self.size_y,
                                         do_plot=False)
        x_hex_coords = hex_centers[:, 0]
        y_hex_coords = hex_centers[:, 1]

        plot_single_lattice_custom_colors(x_hex_coords, y_hex_coords,
                                          face_color=image_grid,
                                          edge_color=image_grid,
                                          min_diam=1.,
                                          plotting_gap=0.05,
                                          rotate_deg=0)
        """

        # image_grid = np.full((self.size_x, self.size_y), '#888888', dtype=str)
        image_grid = np.full((self.size_x, self.size_y, 3), 0, dtype=np.uint8)

        # self.grid = np.flip(self.grid, 1)

        # self.grid = np.swapaxes(self.grid, 0, 0)
        """
        image_grid[self.grid == 0] = 'FFFFFF'
        image_grid[self.grid == 1] = '000000'
        image_grid[self.grid == 2] = '00FF00'
        image_grid[self.grid == 3] = '0000FF'
        image_grid[self.grid == 4] = 'FFFF00'
        image_grid[self.grid == 5] = '00FFFF'
        image_grid[self.grid == 6] = 'FF00FF'
        """
        image_grid[self.grid == 0] = (1, 1, 1)
        image_grid[self.grid == 1] = (0, 0, 0)
        image_grid[self.grid == 2] = (1, 0, 1)
        image_grid[self.grid == 3] = (0, 1, 0)
        image_grid[self.grid == 4] = (0, 0, 1)
        image_grid[self.grid == 5] = (0, 1, 1)
        image_grid[self.grid == 6] = (1, 1, 0)

        #for ant in self.ants:
        #    image_grid[ant.x, ant.y] = (1, 0, 0)

        # image_grid = image_grid.swapaxes(0, 1)
        # self.grid = self.grid.swapaxes(0, 1)



        DPI = 100
        width, height = 1000, 1000
        fig = plt.figure(figsize=(width / DPI, height / DPI), dpi=DPI, facecolor='k')
        ax = fig.add_subplot()

        plt.axis('equal')
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)

        for y in range(self.size_x):
            for x in range(self.size_y):
                if self.grid[x, y] != 0:
                    # Only plot a hexagon if its state is not zero.
                    plot_hex(ax, x, y, image_grid[x, y])

        ax.set_xlim(0, self.size_x)
        ax.set_ylim(0, self.size_y)

        plt.show()

        logging.info("Finished Image Processing")


def run_square():
    width = 500
    game = SquareGrid(width, width)
    game.add_ant(width/2, width/2, 2)
    game.run_simulation(50000)
    game.make_image()


def run_hex():
    states = States.StateMachine()
    # R1 R2 N U R2 R1 L2
    states.add_state_chunk(state=0, color=0, next_color=1, turn=1, next_state=0, sides=6)
    states.add_state_chunk(state=0, color=1, next_color=2, turn=2, next_state=0, sides=6)
    states.add_state_chunk(state=0, color=2, next_color=3, turn=0, next_state=0, sides=6)
    states.add_state_chunk(state=0, color=3, next_color=4, turn=3, next_state=0, sides=6)
    states.add_state_chunk(state=0, color=4, next_color=5, turn=2, next_state=0, sides=6)
    states.add_state_chunk(state=0, color=5, next_color=6, turn=1, next_state=0, sides=6)
    states.add_state_chunk(state=0, color=6, next_color=0, turn=4, next_state=0, sides=6)

    # TODO figure out why values like 10 or 30 fuck with our hex placement
    width = 250
    game = HexGrid(width, width, states=states)
    game.add_ant(int(width/2), int(width/2), 3)
    # game.add_ant(10, 11, 2)
    game.run_simulation(64000)
    game.make_image()
    return

run_hex()
