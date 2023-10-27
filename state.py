import numpy as np
from utility import all_rotations
from utility import main_state
from utility import get_winner
from constants import *


class BoardState:

    def __init__(self, state_array):
        assert len(state_array) == BOARD_SIZE * BOARD_SIZE
        for item in state_array:
            assert item in [X, O, BLANK]
        self.states = all_rotations(state_array)
        self.state = main_state(self.states)
        self.winner = get_winner(self.state)

    @classmethod
    def from_string(cls, row):
        return BoardState([CELLS_REVERSED[item] for item in [*row]])

    @property
    def is_terminal(self):
        return self.winner is not None

    def __repr__(self):
        values = [*str(self)]
        groups = []
        for group_size in range(0, len(self.state), BOARD_SIZE):
            groups.append('| ' + ' '.join(values[group_size:(group_size + BOARD_SIZE)]) + ' |')
        return '\n' + '\n'.join(groups)

    def __str__(self):
        state_string = ''.join(CELLS[item] for item in self.state)
        return state_string

    def __eq__(self, other):
        return str(self) == str(other)

    def get_free_indices(self):
        free_indices = []
        for index, item in enumerate(self.state):
            if item == BLANK:
                free_indices.append(index)
        return free_indices

    def get_action_item(self):
        if self.is_terminal:
            return None
        if sum(self.state) == 0:
            return X
        else:
            return O

    def is_same(self, state_array):
        return state_array in self.states

    def __hash__(self):
        return str(self).__hash__()
