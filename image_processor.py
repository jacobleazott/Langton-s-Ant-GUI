import window_setup

import PIL
from PIL import Image, ImageTk
import imageio
import numpy as np
import webbrowser
import math
from math import exp

global log_state
log_state = False

global images
images = []
global height
height = 100
global width
width = 100
global filename
filename = ''
global gif_frames
gif_frames = 100
global max_steps
max_steps = 100
global frame_count
frame_count = 0
global color_values
color_values = []
global image_grid


global count
count = 0


# Sets what hex values we should be using
def set_color_hex(colors):
    global color_values
    color_values = colors


# Sets how many steps will be done for the program
def set_max_steps(val):
    global max_steps
    max_steps = val


# Sets true or false for log scale in gif format
def set_log(val):
    global log_state
    log_state = val


# Sets height of the grid size
def set_height(y):
    global height
    height = y


# Sets width of the grid size
def set_width(x):
    global width
    width = x


# Sets where the gif should be saved to
def set_gif_filename(name):
    global filename
    filename = name


# Sets how long (seconds) the output gif should be
def set_gif_length(val):
    global gif_frames
    gif_frames = val


# Converts Hex Data To RGB Equivalent
def hex_to_rgb(val):
    color = val.lstrip('#')
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))


# Loads an image into an array for creepy results
def load_image(pic_file):
    img = Image.open(pic_file)
    img.load()
    data = np.asarray(img, dtype="int32")
    return data


# Takes grid data, translates it into an image, and appends to list
def make_image():
    global images, image_grid, count
    img = Image.fromarray(image_grid, 'RGB')
    # img.save('my.gif')
    images.append(img)
    count += 1


# Makes and displays the gif from all of the images
def make_gif():
    global filename, images
    # Makes sure that whatever file you name saves as a .gif
    if not filename.endswith(".gif"):
        filename = filename + ".gif"
    imageio.mimsave(filename, images)
    webbrowser.open(filename)


# Setup for image_grid which and sets up background color correctly
def setup():
    global image_grid, height, width, color_values, frame_count, images, max_steps
    window_setup.progress_setup(max_steps)
    frame_count = 0
    if images is not None:
        images = []
    image_grid = np.full((height, width, 3), 255, dtype=np.uint8)
    for i in range(0, width):
        for j in range(0, height):
            image_grid[j, i] = hex_to_rgb(color_values[0])


# Updates the image grid with the new ant placements as well as spaces out when pictures should be made
def update_image(x, y, color_index, step):
    global max_steps, frame_count, image_grid, color_values, gif_frames
    image_grid[y, x] = hex_to_rgb(color_values[color_index])

    # Make a user defined length image gif either logarithmically or lineally
    if log_state:
        # New fancy logarithmic gif creation
        log_val = gif_frames * (1 - exp(((-13) * step) / (2.71 * max_steps)))
        if log_val > frame_count:
            make_image()
            frame_count += 1
            window_setup.progress_update(step)
    elif not log_state:
        lin_val = (gif_frames / max_steps) * step
        if lin_val > frame_count:
            make_image()
            frame_count += 1
            window_setup.progress_update(step)