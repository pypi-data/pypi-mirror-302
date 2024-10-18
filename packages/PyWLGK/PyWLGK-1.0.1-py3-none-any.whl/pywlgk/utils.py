from typing import List, Optional, Tuple

import numpy as np


class L:
    def __init__(self, value: Optional[List[int]] = None):
        self.value: List[int] = value or []

    def __mul__(self, other):
        if other == 0:
            return L()
        return L(self.value)

    def __add__(self, other):
        return L(self.value + other.value)

    def __radd__(self, other):
        if isinstance(other, int):
            return L(self.value + [other])
        return L(other.value + self.value)

    def __lt__(self, other):
        for a, b in zip(self.value, other.value):
            if type(a) != type(b):
                return str(type(a)) < str(type(b))
            if a < b:
                return True
            elif a > b:
                return False
        return len(self.value) < len(other.value)

    def __lshift__(self, other):
        return L(other.value + sorted(self.value))

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return f"L({self.value})"

    def __hash__(self):
        return hash(str(self.value))


def prep_labels(labels: List) -> Tuple[List[List[L]], int]:
    output = []
    mapping = {}
    current_id = -1
    for i, graph_labels in enumerate(labels):
        output.append([])
        for l in graph_labels:
            if l not in mapping:
                current_id += 1
                mapping[l] = current_id
            output[-1].append(L([mapping[l]]))
    return output, current_id


def adj_mat2list(adj):
    return [set(np.where(neighbors == 1)[0]) for neighbors in adj]
