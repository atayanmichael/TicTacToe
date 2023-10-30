from policy import Policy
from constants import X
from constants import O
from game import Game


# the commented code is for training to play as X and O respectively

# x_policy = Policy(X)
# x_policy.train()
# x_policy.save()

# for playing second, tie is more prioritized
# o_policy = Policy(O, tie_reward=0.5)
# o_policy.train()
# o_policy.save()


def user_turn(board_size):
    return input(f'your_turn, input number from 1 to {board_size * board_size}:\n')


def play_more():
    return input(f'play more?\n')


policy = Policy(X, board_size=3, saved=True)
game = Game(policy, user_turn)
game.start_playing(play_more)
