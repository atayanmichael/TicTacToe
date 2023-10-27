import numpy as np
from itertools import permutations
import itertools
from state import BoardState
from policy import Policy
from constants import X
from constants import O
from constants import CELLS
from state_management import apply_action


# the commented code is for training to play as X and O respectively

# x_policy = Policy(X)
# x_policy.iterate_value_algorithm(300)
# x_policy.save()

# for playing second, tie is more prioritized
# o_policy = Policy(O, tie_reward=0.5)
# o_policy.iterate_value_algorithm(300)
# o_policy.save()

def play(policy):
    state = BoardState.from_string('---------')
    print(repr(state))
    while not state.is_terminal:
        # AI turn
        if state.get_action_item() == policy.action_item:
            state = policy.play(state)
            print(repr(state))
        else:
            user_input = int(input('your_turn, input number from 1 to 9:\n')) - 1
            state = apply_action(state, (-policy.action_item, user_input))
    print(f'winner: {CELLS[state.winner]}')


x_policy = Policy(X)
x_policy.load()
o_policy = Policy(O)
o_policy.load()
play(o_policy)
