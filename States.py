import numpy as np
import logging as log
import re
from collections import defaultdict

log.basicConfig(filename='Ant.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%H:%M:%S')


# direction - current direction the ant is facing
# states - the given state diagram for our ants behavior
# state - the current state our ant is in
class Ant:
    def __init__(self, pos_x, pos_y, direction, states=None, state=0):
        if states is None:
            states = StateMachine(default=True)
        self.state_diagram = states
        self.state = state
        self.direction = direction
        self.x = pos_x
        self.y = pos_y

    def move_ant(self, color):
        transition = self.state_diagram.get_transition(self.state, color)
        # TODO - This will break when we go from like an 8 sided to a 4 sides polygon. Direction will need some
        #  lookup table to translate these values
        self.direction = (self.direction + transition.turn) % transition.sides
        self.state = transition.next_state
        return transition.next_color


# turn - relative direction we should turn
# next_color - color the space we are standing on should turn
# next_state - the next state the ant will be in
# sides - gives the number of available paths out of the current spot
class StateTransition:
    def __init__(self, turn, next_color, next_state, sides=4):
        self.turn = turn
        self.next_color = next_color
        self.next_state = next_state
        self.sides = sides


class StateMachine:
    def __init__(self, default=False):
        self.chunks = defaultdict(dict)
        if default:
            self.add_state_chunk(0, 0, 1, 3, 0)
            self.add_state_chunk(0, 1, 1, 3, 1)
            self.add_state_chunk(1, 0, 1, 1, 1)
            self.add_state_chunk(1, 1, 0, 0, 0)

    def add_state_chunk(self, state, color, next_color, turn, next_state):
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
        return self.chunks[state][color]

