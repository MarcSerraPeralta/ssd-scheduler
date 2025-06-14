import os
import pathlib
import pickle

import networkx as nx
from surface_sim.layouts import ssd_code

from algorithm import find_schedule, check_schedule
from metrics import get_circuit_distance_from_schedule_for_ssd


# build tanner graph for small stellated dodecahedron code
layout = ssd_code()
max_depth = 7
assert_ft = True
seed = None
dir_name = "ssd_schedules"

tanner_graph = nx.Graph()
tanner_graph.add_nodes_from(layout.qubits)
for anc_qubit in layout.anc_qubits:
    support = layout.get_neighbors([anc_qubit])
    for data_qubit in support:
        tanner_graph.add_edge(data_qubit, anc_qubit)

assert set(tanner_graph.nodes) == set(layout.graph.nodes)
assert tanner_graph.edges == layout.graph.to_undirected().edges

# find schedules and store the ones that are FT and have 6 or less CNOT layers
dir = pathlib.Path(dir_name)
if not dir.exists():
    dir.mkdir(parents=True, exist_ok=True)

# load previous schedules
schedules = []
for file_name in os.listdir(dir):
    with open(dir / file_name, "rb") as file:
        schedules.append(pickle.load(file))

iteration = 0
all_schedules = [s for s in schedules]
while True:
    try:
        schedule = find_schedule(tanner_graph, seed=seed)
    except:
        continue

    check_schedule(schedule, tanner_graph)

    iteration += 1
    print(f"\riteration = {iteration}... ", end="")

    depth = len(schedule[layout.anc_qubits[0]])
    if depth > max_depth:
        print(f"Discarding schedule dute to long depth ({depth} >= {max_depth}).")
        continue

    if schedule in all_schedules:
        print("Discarding schedule because it is already present.")
    all_schedules.append(schedule)

    d_circ = get_circuit_distance_from_schedule_for_ssd(schedule)
    ft = d_circ == 3
    if assert_ft and (not ft):
        print("Discarding schedule because it is not fault tolerant.")
        continue
    schedules.append(schedule)

    print(f"Found FT schedule of depth {depth} (total of {len(schedules)} found)")
    with open(dir / f"depth{depth}_id{len(schedules)}_ft-{ft}.pickle", "wb") as file:
        pickle.dump(schedule, file, pickle.HIGHEST_PROTOCOL)
