import numpy as np
from constants import *
import math


def all_rotations(array, board_size):
    array = to_2d(array, board_size)
    rotations = []
    add_rotations(array, rotations)
    array = np.fliplr(array)
    add_rotations(array, rotations)
    return rotations


def to_2d(array, board_size):
    return np.array(array).reshape((board_size, board_size))


def get_winner(array, board_size):
    def has_winner(sum_of):
        if board_size in sum_of:
            return X
        if -board_size in sum_of:
            return O
        return None

    array_2d = to_2d(array, board_size)
    if winner := has_winner(np.sum(array_2d, axis=0)):
        return winner
    if winner := has_winner(np.sum(array_2d, axis=1)):
        return winner
    if winner := has_winner([np.sum(np.diag(array_2d))]):
        return winner
    if winner := has_winner([np.sum(np.diag(np.rot90(array_2d)))]):
        return winner
    if BLANK not in array:
        return TIE
    return None


def main_state(rotations):
    return max(rotations)


def add_rotations(array_2d, into):
    for _ in range(4):
        array_2d = np.rot90(array_2d)
        into.append(array_2d.flatten().tolist())


def calculate_board_size(array):
    return int(math.sqrt(len(array)))


def to_string(array):
    return ''.join(CELLS[item] for item in array)


def to_visual_board(array):
    values = to_string(array)
    board_size = calculate_board_size(array)
    groups = []
    for group_size in range(0, len(values), board_size):
        groups.append('| ' + ' '.join(values[group_size:(group_size + board_size)]) + ' |')
    return '\n' + '\n'.join(groups)


def find_differences(first_array, second_array):
    for first, second in zip(first_array, second_array):
        if first != second:
            yield first, second


def is_blank(array):
    return X not in array and O not in array


class DefaultDict(dict):
    def get_or(self, key, value):
        if self[key] is None:
            return value
        return self[key]
