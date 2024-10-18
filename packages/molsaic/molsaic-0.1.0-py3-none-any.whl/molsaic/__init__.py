import typing as t

import networkx as nx
import numpy as np
from ase.neighborlist import natural_cutoffs


def atoms_to_graph(atoms):
    distance_matrix = atoms.get_all_distances(mic=True)
    cutoffs = np.array(natural_cutoffs(atoms, mult=1.2))  # TODO: better cutoffs!
    cutoffs = cutoffs[:, None] + cutoffs[None, :]
    connectivity_matrix = np.zeros((len(atoms), len(atoms)), dtype=int)
    np.fill_diagonal(distance_matrix, np.inf)
    connectivity_matrix[distance_matrix <= cutoffs] += 1
    np.fill_diagonal(distance_matrix, 0)
    G = nx.from_numpy_array(connectivity_matrix)
    # add positions as node data
    for i, atom in enumerate(atoms):
        G.nodes[i]["position"] = atom.position
        G.nodes[i]["number"] = atom.number
        G.nodes[i]["index"] = i
    return G, distance_matrix