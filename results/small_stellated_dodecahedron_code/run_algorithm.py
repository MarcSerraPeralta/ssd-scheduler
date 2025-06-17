print("Preparing algorithm...")
import os
import pathlib
import pickle
from copy import deepcopy

import networkx as nx
from surface_sim.layouts import ssd_code

from css_scheduler import find_schedule_from_precompiled, precompile, check_schedule
from lib.metrics import get_circuit_distance_from_schedule_for_ssd


# input parameters
layout = ssd_code()
max_depth = 6
assert_ft = True
seed = None
verbose = False
dir_name = "schedules"

# build tanner graph for small stellated dodecahedron code
tanner_graph = nx.Graph()
tanner_graph.add_nodes_from(layout.qubits)
for anc_qubit in layout.anc_qubits:
    support = layout.get_neighbors([anc_qubit])
    for data_qubit in support:
        tanner_graph.add_edge(data_qubit, anc_qubit)

assert set(tanner_graph.nodes) == set(layout.graph.nodes)
assert tanner_graph.edges == layout.graph.to_undirected().edges


# load previous schedules to avoid duplicates
dir = pathlib.Path(dir_name)
if not dir.exists():
    dir.mkdir(parents=True, exist_ok=True)

schedules = []
for file_name in os.listdir(dir):
    if not file_name.endswith(".pickle"):
        # avoid annoying macOS files (.DS_Store)
        continue
    with open(dir / file_name, "rb") as file:
        schedules.append(pickle.load(file))

# precompile data
proper_conds, parallel_conds, blocking_graph, node_to_sets, set_to_nodes, empty_sets = (
    precompile(tanner_graph)
)

# run algorithm
print("Running algorithm...")
iteration = 0
all_schedules = [s for s in schedules]
while True:
    try:
        iteration += 1
        print(f"\riteration = {iteration}... ", end="")
        schedule = find_schedule_from_precompiled(
            deepcopy(proper_conds),
            parallel_conds,
            deepcopy(blocking_graph),
            node_to_sets,
            set_to_nodes,
            deepcopy(empty_sets),
            seed=seed,
            verbose=verbose,
            early_stop={"max_num_layers": max_depth},
        )
    except ValueError as error:
        print(error, end="")
        continue

    check_schedule(schedule, tanner_graph)

    depth = len(schedule[layout.anc_qubits[0]])
    if depth > max_depth:
        print(
            f"Discarding schedule dute to long depth ({depth} >= {max_depth}).", end=""
        )
        continue

    if schedule in all_schedules:
        print("Discarding schedule because it is already present.")
        continue
    all_schedules.append(schedule)

    if depth == 5:
        # store even if it is not FT
        with open(dir / f"depth{depth}_tmp{len(schedules)}.pickle", "wb") as file:
            pickle.dump(schedule, file, pickle.HIGHEST_PROTOCOL)

    d_circ = get_circuit_distance_from_schedule_for_ssd(schedule)
    ft = d_circ == 3
    if assert_ft and (not ft):
        print("Discarding schedule because it is not fault tolerant.")
        continue
    schedules.append(schedule)

    print(f"Found FT schedule of depth {depth} (total of {len(schedules)} found)")
    with open(dir / f"depth{depth}_id{len(schedules)}_ft-{ft}.pickle", "wb") as file:
        pickle.dump(schedule, file, pickle.HIGHEST_PROTOCOL)
