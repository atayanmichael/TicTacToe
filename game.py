from state import BoardState
from constants import BLANK
from constants import CELLS
from utility import find_differences
from utility import to_visual_board
from utility import is_blank
from state_management import apply_action


class Game:
    def __init__(self, policy, user_turn):
        self.policy = policy
        self.user_turn = user_turn

    @staticmethod
    def get_state_visual_rotation(state, previous_array):
        for array in state.rotations:
            if len(list(find_differences(previous_array, array))) == 1:
                return array

    def play(self):
        previous_array = [BLANK] * self.policy.board_size * self.policy.board_size
        print(to_visual_board(previous_array))
        current_state = BoardState(previous_array)
        while not current_state.is_terminal:
            if current_state.get_action_item() == self.policy.action_item:  # AI turn
                current_state = self.policy.play(current_state)
                previous_array = self.get_state_visual_rotation(current_state, previous_array)
            else:  # user turn
                if (user_input := self.handle_user_input(previous_array)) < 0:
                    print("wrong input, please enter correct number")
                    continue
                current_state = self.handle_user_turn(user_input, previous_array)
                previous_array[user_input] = -self.policy.action_item
            print(to_visual_board(previous_array))
        print(f'winner: {CELLS[current_state.winner]}')

    def start_playing(self, play_more):
        self.play()
        while play_more().lower() == 'yes':
            self.play()

    def handle_user_input(self, array):
        try:
            user_input = int(self.user_turn(self.policy.board_size)) - 1
        except ValueError:
            return -1
        if user_input not in range(len(array)):
            return -1
        if array[user_input] != BLANK:
            return -1
        return user_input

    def handle_user_turn(self, user_input, previous_array):
        current_array = previous_array.copy()
        current_array[user_input] = -self.policy.action_item
        return BoardState(current_array)
