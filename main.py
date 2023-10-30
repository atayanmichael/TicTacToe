from state import BoardState
from policy import Policy
from constants import *
from state_management import apply_action


# the commented code is for training to play as X and O respectively

# x_policy = Policy(X)
# x_policy.train()
# x_policy.save()

# for playing second, tie is more prioritized
# o_policy = Policy(O, tie_reward=0.5)
# o_policy.train()
# o_policy.save()

def play(policy):
    state = BoardState([BLANK] * policy.board_size * policy.board_size)
    print(repr(state))
    while not state.is_terminal:
        # AI turn
        if state.get_action_item() == policy.action_item:
            state = policy.play(state)
            print(repr(state))
        else:
            user_input = int(input(f'your_turn, input number from 1 to {policy.board_size * policy.board_size}:\n')) - 1
            state = apply_action(state, (-policy.action_item, user_input))
    print(f'winner: {CELLS[state.winner]}')


policy = Policy(O)
policy.load()
play(policy)
while input(f'play more?\n') == 'yes':
    play(policy)
