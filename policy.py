import json
from state_management import StateHolder
from constants import CELLS
from state_management import possible_states
from state_management import apply_action
from state import BoardState


def find_action_values(state, all_states):
    for action_state, action in possible_states(state):
        if action_state.is_terminal:
            yield all_states.get_or(action_state, 0), action
            continue
        actions_count = len(action_state.get_free_indices())
        value = 0
        for result, _ in possible_states(action_state):
            value += all_states.get_or(result, 0) / actions_count
        yield value, action


class Policy:
    def __init__(self, action_item, board_size=3, discount_factor=0.9, **kwargs):
        self.discount_factor = discount_factor
        self.transition_reward = kwargs.get('transition_reward', .05)
        self.win_reward = kwargs.get('win_reward', 1)
        self.lose_reward = kwargs.get('lose_reward', -1)
        self.tie_reward = kwargs.get('tie_reward', 0)
        self.action_item = action_item
        self.state_holder = StateHolder(board_size=board_size)
        self.board_size = board_size

    @property
    def states(self):
        return self.state_holder.states

    @states.setter
    def states(self, states):
        self.state_holder.states.update(states)

    def calculate_values(self, iteration):
        for state in self.states.keys():
            if state.steps_from_filled != iteration:
                continue
            if state.is_terminal or state.get_action_item() == self.action_item:
                yield state, self.calculate_value(state)

    def calculate_value(self, state):
        if state.is_terminal:
            return self.calculate_terminal_value(state)
        return self.transition_reward + self.discount_factor * max(find_action_values(state, self.states))[0]

    def calculate_terminal_value(self, state):
        if (value := self.states[state]) is not None:
            return value
        if self.action_item == state.winner:
            return self.win_reward
        if self.action_item == -state.winner:
            return self.lose_reward
        else:
            return self.tie_reward

    def train(self):
        for iteration in range(self.board_size * self.board_size + 1):
            updated_states = {}
            for key, value in self.calculate_values(iteration):
                updated_states[key] = value
            self.states = updated_states

    def save(self):
        with open(f'policy_{CELLS[self.action_item]}_{self.board_size}.txt', 'w') as f:
            f.write(json.dumps({str(key): value for key, value in self.states.items()}))

    def load(self):
        with open(f'policy_{CELLS[self.action_item]}_{self.board_size}.txt', 'r') as f:
            self.states = {BoardState.from_string(key): value for key, value in json.load(f).items()}

    def play(self, state):
        action = max(find_action_values(state, self.states))[1]
        return apply_action(state, action)
