import networkx as nx
from surface_sim.layouts import rot_surface_code

from algorithm import find_schedule, check_schedule


# build tanner graph for small stellated dodecahedron code
layout = rot_surface_code(distance=5)
max_depth = 4
assert_ft = True
seed = None
verbose = False

tanner_graph = nx.Graph()
tanner_graph.add_nodes_from(layout.qubits)
for anc_qubit in layout.anc_qubits:
    support = layout.get_neighbors([anc_qubit])
    for data_qubit in support:
        tanner_graph.add_edge(data_qubit, anc_qubit)

assert set(tanner_graph.nodes) == set(layout.graph.nodes)
assert tanner_graph.edges == layout.graph.to_undirected().edges

iteration = 0
while True:
    try:
        schedule = find_schedule(tanner_graph, seed=seed, verbose=verbose)
    except ValueError:
        continue

    check_schedule(schedule, tanner_graph)

    iteration += 1
    print(f"\riteration = {iteration}... ", end="")

    depth = len(schedule[layout.anc_qubits[0]])
    if depth > max_depth:
        continue

    print(f"\nFound schedule of depth {depth}.\n")
