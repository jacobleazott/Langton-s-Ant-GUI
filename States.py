import numpy as np
import logging as log
import re
from collections import defaultdict

log.basicConfig(filename='Ant.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')

"""
COLORS
Colors follow the following array pattern


"""

UP_LEFT = 0
UP_RIGHT = 1
RIGHT = 2
DOWN_RIGHT = 3
DOWN_LEFT = 4
LEFT = 5


class HexGrid:
    def __init__(self, height, width):
        # Height and width 'must' both be odd, this just makes the grid look nice
        self.height = (height + 1) if (height % 2 == 0) else height
        self.width = (width + 1) if (width % 2 == 0) else width
        # self.grid = np.zeros((height, width), dtype=np.uint)
        self.starting_position = [int(height / 2), int(width / 2)]


class Ant:
    def __init__(self, init_x, init_y, direction, states=None, state=0):
        if states is None:
            states = StateMachine(default=True)
        self.x = init_x
        self.y = init_y
        self.state_diagram = states
        self.state = state
        self.direction = direction

    def move_ant(self):
        transition = self.state_diagram.getTransition(self.state, )



class StateTransition:
    def __init__(self, turn, next_color, next_state):
        self.turn = turn
        self.next_color = next_color
        self.next_state = next_state


class StateMachine:
    def __init__(self, default=False):
        if default:
            self.add_state_chunk(0, 0x000000, LEFT, 0xFFFFFF, 1)
            self.add_state_chunk(0, 0xFFFFFF, RIGHT, 0x000000, 1)
        self.chunks = defaultdict(dict)

    def add_state_chunk(self, state, color, turn, next_color, next_state):
        if type(state) != int:
            log.error(f'State variable input into class State is not of type int it is {type(state)}')
        if type(color) != int:
            log.error(f'Color variable input into class State is not of type int it is {type(color)}')
        if type(turn) != int:
            log.error(f'Turn variable input into class State is not of type int it is {type(turn)}')
        if type(next_color) != int:
            log.error(f'Next_color variable input into class State is not of type int it is {type(next_color)}')
        if type(next_state) != int:
            log.error(f'Next_state variable input into class State is not of type int it is {type(next_state)}')
        self.chunks[state][color] = StateTransition(turn, next_color, next_state)

    def get_transition(self, state, color):
        return self.chunks[color][state]


machine = State()
machine.add_state_chunk(0, 0x000000, LEFT, 0xFFFFFF, 1)
machine.add_state_chunk(0, 0xFFFFFF, RIGHT, 0x000000, 1)
machine.add_state_chunk(1, 0x000000, LEFT, 0xFFFFFF, 2)
machine.add_state_chunk(1, 0xFFFFFF, RIGHT, 0x000000, 2)
machine.add_state_chunk(2, 0x000000, LEFT, 0xFFFFFF, 0)
machine.add_state_chunk(2, 0xFFFFFF, RIGHT, 0x000000, 0)






