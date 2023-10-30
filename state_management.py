import constants
from state import BoardState
from constants import BLANK
from constants import X
from utility import DefaultDict


def apply_action(state, action):
    item, index = action
    new_state = list(state.state)
    new_state[index] = item
    return BoardState(new_state)


def possible_states(state):
    if state.is_terminal:
        return
    item = state.get_action_item()
    for index in state.get_free_indices():
        yield apply_action(state, (item, index)), (item, index)


class StateHolder:
    def __init__(self, board_size=3, saved=False):
        self.states = DefaultDict()
        self.board_size = board_size
        if not saved:
            self.store_states()

    def store_states(self):
        new_states = set()
        new_states.add(BoardState([BLANK] * self.board_size * self.board_size))
        while len(new_states):
            result = set()
            for state in new_states:
                for child_state, _ in possible_states(state):
                    result.add(child_state)
            for state in new_states:
                self.states[state] = None
            new_states.clear()
            for new_state in result:
                new_states.add(new_state)
