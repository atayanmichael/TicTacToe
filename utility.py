import numpy
import numpy as np
from constants import *


def all_rotations(array):
    array = to_2d(array)
    rotations = []
    add_rotations(array, rotations)
    array = np.fliplr(array)
    add_rotations(array, rotations)
    return rotations


def to_2d(array):
    return np.array(array).reshape((BOARD_SIZE, BOARD_SIZE))


def get_winner(array):
    def has_winner(sum_of):
        if BOARD_SIZE in sum_of:
            return X
        if -BOARD_SIZE in sum_of:
            return O
        return None

    array_2d = to_2d(array)
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


class DefaultDict(dict):
    def get_or(self, key, value):
        if self[key] is None:
            return value
        return self[key]