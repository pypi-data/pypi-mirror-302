from typing import Callable, Optional, List

import numpy as np

from pywlgk.utils import L, prep_labels, adj_mat2list


def wlk(
        adjs: List[np.ndarray],
        labels: List[np.ndarray],
        k: int = 4,
        normalize: bool = False,
        kernel_fn: Optional[Callable] = None,
):
    """
    Main function implementing the logic for the WLK algorithm.

    :param adjs: List of adjacency matrices
    :param labels: List of labels which can have any type
    :param k: number of iterations of the WLK algorithm, must be non-negative
    :param normalize: whether to normalize the kernel matrix or not
    :param kernel_fn: Kernel function to use. Default is dot product (if kernel_fn=None) as used in the original paper. Alternative functions can be used to compute the kernel matrix. These have to be provided as callables.
    :return: A symmetric matrix storing the pairwise metric values between graphs. Depending on the kernel function it can be distances or similarities.
    """
    sizes = [len(graph_labels) for graph_labels in labels]
    edges = [adj_mat2list(adj) for adj in adjs]
    labels, current_id = prep_labels(labels)
    classes = []

    for _ in range(k):
        tmp_labels = [[
            L([graph_labels[i].value[0]] + list(sorted(graph_labels[-sizes[j] + n].value[0] for n in neighbors)))
            for i, neighbors in enumerate(edges[j])
        ] for j, graph_labels in enumerate(labels)]
        mapping = {}
        for graph_labels in tmp_labels:
            for l in graph_labels:
                if l not in mapping:
                    current_id += 1
                    x = L([current_id])
                    mapping[l] = x
        for i, tmp_graph_labels in enumerate(tmp_labels):
            labels[i] += [mapping[label] for label in tmp_graph_labels]

    classes += [L([c]) for c in range(current_id + 1)]
    tmp = np.eye(len(classes), dtype=int)
    mapping = {val: tmp[i] for i, val in enumerate(classes)}
    subtree_k = np.array([np.array([mapping[label] for label in graph_labels]).sum(axis=0) for graph_labels in labels])
    matrix = np.dot(subtree_k, subtree_k.T) if not kernel_fn else kernel_fn(subtree_k)
    if not normalize:
        return matrix
    return np.nan_to_num(np.divide(matrix, np.sqrt(np.outer(np.diagonal(matrix), np.diagonal(matrix)))))
