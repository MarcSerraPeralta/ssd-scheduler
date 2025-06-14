import pathlib
import networkx as nx
from surface_sim.layouts import ssd_code

from algorithm import find_schedule, check_schedule
from metrics import get_circuit_distance_from_schedule_for_ssd


# build tanner graph for small stellated dodecahedron code
layout = ssd_code()
max_depth = 60000
assert_ft = True

tanner_graph = nx.Graph()
tanner_graph.add_nodes_from(layout.qubits)
for anc_qubit in layout.anc_qubits:
    support = layout.get_neighbors([anc_qubit])
    for data_qubit in support:
        tanner_graph.add_edge(data_qubit, anc_qubit)

assert set(tanner_graph.nodes) == set(layout.graph.nodes)
assert tanner_graph.edges == layout.graph.to_undirected().edges

# find schedules and store the ones that are FT and have 6 or less CNOT layers
dir = pathlib.Path("unrot_surface_code_schedules")
if not dir.exists():
    dir.mkdir(parents=True, exist_ok=True)

schedules = []
iteration = 0
while True:
    schedule = find_schedule(tanner_graph)
    check_schedule(schedule, tanner_graph)

    iteration += 1
    print(f"\riteration = {iteration}... ", end="")

    depth = len(schedule[layout.anc_qubits[0]])
    if depth > max_depth:
        print(f"Discarding schedule dute to long depth ({depth} >= {max_depth}).")
        continue

    d_circ = get_circuit_distance_from_schedule_for_ssd(schedule)
    if assert_ft and (d_circ != 3):
        print("Discarding schedule because it is not fault tolerant.")
        continue

    if schedule not in schedules:
        print(f"Found FT schedule of depth {depth} (total of {len(schedules)} found)")
        with open(
            dir / f"depth{depth}_id{len(schedules)}_fault-tolerant.txt", "w"
        ) as file:
            file.write(str(schedule))
        schedules.append(schedule)
