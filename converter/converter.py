from typing import List

from value import Value, Pair, NULL_PAIR_VALUE

class CannotConvertToList(Exception):

    def __init__(self, message):
        super(CannotConvertToList, self).__init__(message)


def slice_to_pair_values(slices: List[Value]) -> Value:
    front: Value = NULL_PAIR_VALUE
    for x in reversed(slices):
        front = Pair(x, front)
    return front


def pairs_to_slice(pairs: Value) -> List[Value]:
    slice: List[Value] = []
    while pairs is not NULL_PAIR_VALUE and pairs is not None:
        if isinstance(pairs, Pair):
            slice.append(pairs.first)
            pairs = pairs.second
        else:
            raise CannotConvertToList('{} cannot convert to list'.format(type(pairs)))
    return slice