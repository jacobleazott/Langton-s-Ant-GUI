import image_processor
import window_setup

# import numpy as np

# Constants
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


def run_simulation(ants, color_action, grid, max_steps):

    # Returns true if an ant is about to leave the allotted grid size
    def check_edge_collision():
        # global ants, grid
        # Iterates through all of the ants
        for k in range(0, len(ants)):
            # Check to make sure it is not on any of the 4 sides
            if (ants[k][0] == 0 or ants[k][1] == 0) or \
                    (ants[k][0] == int(grid.shape[0]) or ants[k][1] == int(grid.shape[1])):
                return True
        return False

    # Perform 1 step of simulation
    def step(step_num):
        # global ants, color_action, grid
        for i in range(0, len(ants)):
            # Gets what color the ant is on
            color_index = grid[ants[i][0], ants[i][1]]
            # Changes it's direction based off of the associated colors action
            ants[i][2] = (ants[i][2] + color_action[color_index]) % 4
            # Iterates the color value accordingly
            color_value = (color_index + 1) % len(color_action)
            # Update the grid with the new color value
            grid[ants[i][0], ants[i][1]] = color_value
            # Send the changed locations new color and location to the image_processor

            image_processor.update_image(ants[i][1], ants[i][0], color_value, step_num)

            if ants[i][2] == 0:     # Up
                ants[i][0] -= 1
            elif ants[i][2] == 1:   # Right
                ants[i][1] += 1
            elif ants[i][2] == 2:   # Down
                ants[i][0] += 1
            else:                       # Left
                ants[i][1] -= 1

    # Run the simulation stopping if the ant hits the edge
    for j in range(0, max_steps):
        step(j)
        if check_edge_collision():
            break
    window_setup.progress_update(max_steps)
    image_processor.make_image()
    image_processor.make_gif()
