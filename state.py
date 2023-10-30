import numpy as np
from utility import all_rotations
from utility import main_state
from utility import get_winner
from utility import calculate_board_size
from utility import to_string
from utility import to_visual_board
from constants import *


class BoardState:

    def __init__(self, state_array):
        board_size = calculate_board_size(state_array)
        assert board_size in SUPPORTED_BOARD_SIZES
        for item in state_array:
            assert item in [X, O, BLANK]
        self.rotations = all_rotations(state_array, board_size)
        self.state = main_state(self.rotations)
        self.winner = get_winner(self.state, board_size)
        self.board_size = board_size
        self.steps_from_filled = state_array.count(BLANK)

    @classmethod
    def from_string(cls, row):
        return BoardState([CELLS_REVERSED[item] for item in [*row]])

    @property
    def is_terminal(self):
        return self.winner is not None

    def __repr__(self):
        return to_visual_board(self.state)

    def __str__(self):
        return to_string(self.state)

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

    def __hash__(self):
        return str(self).__hash__()
