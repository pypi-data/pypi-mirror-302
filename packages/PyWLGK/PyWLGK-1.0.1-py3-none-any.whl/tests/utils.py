import numpy as np
from grakel import Graph

tto = {
    'ALA': 'A',
    'ARG': 'R',
    'ASN': 'N',
    'ASP': 'D',
    'CYS': 'C',
    'GLN': 'Q',
    'GLU': 'E',
    'GLY': 'G',
    'HIS': 'H',
    'ILE': 'I',
    'LEU': 'L',
    'LYS': 'K',
    'MET': 'M',
    'PHE': 'F',
    'PRO': 'P',
    'SER': 'S',
    'THR': 'T',
    'TRP': 'W',
    'TYR': 'Y',
    'VAL': 'V',
}

g1 = np.array([
    [0, 1, 0, 0, 0],
    [1, 0, 1, 0, 0],
    [0, 1, 0, 1, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0]
]), np.array([1, 1, 1, 1, 1])
g2 = np.array([
    [0, 1, 0, 0, 0],
    [1, 0, 1, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 0, 0, 1],
    [0, 0, 0, 1, 0]
]), np.array([1, 1, 1, 1, 1])
g3 = np.array([
    [0, 1, 0, 0],
    [1, 0, 1, 1],
    [0, 1, 0, 0],
    [0, 1, 0, 0],
]), np.array([1, 1, 1, 1])


class Residue:
    def __init__(self, line: str) -> None:
        self.name = tto.get(line[17:20].strip(), "X")
        self.num = int(line[22:26].strip())
        self.chainID = line[21].strip()
        self.x = float(line[30:38].strip())
        self.y = float(line[38:46].strip())
        self.z = float(line[46:54].strip())


class Structure:
    def __init__(self, filename: str) -> None:
        self.residues = [Residue(line) for line in open(filename, "r")
                         if line.startswith("ATOM") and line[12:16].strip() == "CA"]

    def get_coords(self):
        return np.array([[res.x, res.y, res.z] for res in self.residues])

    def get_nodes(self):
        return [res.name for res in self.residues]

    def get_adj(self, threshold: float):
        coords = self.get_coords()
        dist = np.sqrt(np.sum(np.square(coords[:, None, :] - coords[None, :, :]), axis=2))
        edges = np.where(dist < threshold, 1, 0)
        return edges


def to_grakel(adj, labels):
    edges = {}
    for start, end in zip(*np.where(adj == 1)):
        if start not in edges:
            edges[start] = []
        edges[start].append(end)
    return Graph(edges, node_labels={i: label for i, label in enumerate(labels)})


def read(filename):
    pdb = Structure(filename)

    adj = pdb.get_adj(7)
    edges = {}
    for start, end in zip(*np.where(adj == 1)):
        if start not in edges:
            edges[start] = []
        edges[start].append(end)

    return Graph(edges, node_labels={i: label for i, label in enumerate(pdb.get_nodes())}), (adj, pdb.get_nodes())


def get_dummy_equal():
    return g1, g2


def get_dummy_unequal():
    return g1, g3
