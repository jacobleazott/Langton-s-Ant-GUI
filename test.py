import numpy as np
import logging as log
import re
import json
from collections import defaultdict


UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


class StateTransition:
    def __init__(self, turn, next_color, next_state):
        self.turn = turn
        self.next_color = next_color
        self.next_state = next_state


class State:
    def __init__(self,):
        self.chunks = defaultdict(dict)

    def add_state_chunk(self, state, color, turn, next_color, next_state):
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


# print(json.dumps(machine.chunks, indent=2))
print(machine.chunks)
