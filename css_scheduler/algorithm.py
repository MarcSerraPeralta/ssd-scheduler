from collections.abc import Sequence
from itertools import product
from copy import deepcopy

import networkx as nx


def find_schedule(
    tanner_graph: nx.Graph,
    seed: int | None = None,
    verbose: bool = False,
) -> dict[str, list[str | None]]:
    """Returns a proper schedule for a CSS code in which the overlap of any
    pair of Z-type and X-type stabilizers is either 0 or 2 data qubits.

    Parameters
    ----------
    tanner_graph
        Tanner graph of the CSS code. The data qubits labels must start with ``"D"``,
        the X-type stabilizers with ``"X"``, and the Z-type stabilizers with ``"Z"``.
        The overlap of any pair of Z-type and X-type stabilizer must be either
        0 or 2 data qubits.
    seed
        Random seed for ``nx.maximal_independent_set``. By default ``None``.
    verbose
        If ``True`` prints the status of the colored edges while the algorithm
        is running.

    Returns
    -------
    schedule
        Proper schedule for the given code. The layer of CNOTs are specified as
        a (ordered) list, whose elements correspond to the sets of
        (data-qubit)-stabilizer pairs that undergo a CNOT at the layer.

    Raises
    ------
    ValueError
        If a schedule could not be found in this call of the function.
    """
    if not isinstance(tanner_graph, nx.Graph):
        raise TypeError(
            f"'tanner_graph' must be a nx.Graph, but {type(tanner_graph)} as given."
        )
    if not nx.algorithms.is_bipartite(tanner_graph):
        raise TypeError("'tanner_graph' must be a bipartite graph.")
    if any(
        (not isinstance(node, str)) or (node[0] not in {"D", "X", "Z"})
        for node in tanner_graph
    ):
        raise TypeError(
            "Node labels in 'tanner_graph' must start with 'D', 'X', or 'Z'."
        )

    stab_overlap = get_overlap_stabilizers(tanner_graph)
    for overlap in stab_overlap.values():
        if len(overlap) != 2:
            raise ValueError(
                "Any pair of X-type and Z-type stabilizers must have overlap "
                "with 0 or 2 data qubits."
            )

    # ensure that the labelling of the nodes follow (data_qubit, stab) in the line graphs
    parallel_conds = nx.line_graph(tanner_graph)
    for n1, n2 in parallel_conds:
        if n1[0] != "D":
            parallel_conds = nx.relabel_nodes(parallel_conds, {(n1, n2): (n2, n1)})

    proper_conds = nx.Graph()
    proper_conds.add_nodes_from(parallel_conds.nodes)
    for (z_stab, x_stab), (q1, q2) in stab_overlap.items():
        proper_conds.add_edge((q1, z_stab), (q2, x_stab))
        proper_conds.add_edge((q2, z_stab), (q1, x_stab))

    # edge/arrows start from release node and point to blocked node
    # the edge will have a the attribute 'blocking_edge' that points
    # to the edge in the 'proper_conds' graph that blocks the blocked node.
    blocking_graph = nx.DiGraph()
    blocking_graph.add_nodes_from(parallel_conds.nodes)

    empty_sets = set()
    node_to_sets = {n: [] for n in parallel_conds.nodes}
    set_to_nodes = {}
    for ind, ((z_stab, x_stab), (q1, q2)) in enumerate(stab_overlap.items()):
        node_to_sets[(q1, z_stab)].append(ind)
        node_to_sets[(q2, z_stab)].append(ind)
        node_to_sets[(q1, x_stab)].append(ind)
        node_to_sets[(q2, x_stab)].append(ind)
        set_to_nodes[ind] = {(q1, z_stab), (q2, z_stab), (q1, x_stab), (q2, x_stab)}
        empty_sets.add(ind)

    list_coloring = []
    colored_nodes = set()
    while len(colored_nodes) != len(parallel_conds.nodes):
        if verbose:
            print(
                f"{len(colored_nodes)} nodes colored out of {len(parallel_conds.nodes)}"
            )

        blocked_nodes = set(e[1] for e in blocking_graph.edges)
        release_nodes = set(e[0] for e in blocking_graph.edges)

        conds = deepcopy(proper_conds)
        conds.add_edges_from(parallel_conds.edges)

        # loop-blockage
        loop_blocked_nodes = set()
        for empty_set in empty_sets:
            nodes = set_to_nodes[empty_set]
            bs = nodes.intersection(blocked_nodes)
            rs = nodes.intersection(release_nodes)
            for r, b in product(rs, bs):
                if nx.has_path(blocking_graph, r, b) and r[0] == b[0]:
                    other_node = [n for n in proper_conds.neighbors(r) if n in nodes]
                    if len(other_node) != 1:
                        raise ValueError("Something wrong happened in a loop blockage.")
                    loop_blocked_nodes.add(other_node[0])

        conds.remove_nodes_from(blocked_nodes)
        conds.remove_nodes_from(loop_blocked_nodes)
        conds.remove_nodes_from(colored_nodes)

        # find maximum set of edges to color
        if len(conds) == 0:
            raise ValueError(
                "Previous coloring was such that it does not allow for any more edges. "
                "Algorithm has not converged."
            )
        new_nodes = set(nx.maximal_independent_set(conds, seed=seed))
        if len(new_nodes) == 0:
            raise ValueError(
                "Cannot add more edges without breaking any restriction. "
                "Algorithm has not converged."
            )

        # the choice of 'new_nodes' is provisional, as it may contain a full
        # loop-blocking cycle. First check that there are no full blocking
        # cycles and then commit to the 'new_nodes'.
        prov_proper_conds = deepcopy(proper_conds)
        prov_blocking_graph = deepcopy(blocking_graph)
        prov_empty_sets = deepcopy(empty_sets)

        _process_new_nodes(
            new_nodes,
            prov_proper_conds,
            prov_blocking_graph,
            prov_empty_sets,
            node_to_sets,
        )

        # if there are no cycles, then commit to choice of 'new_nodes';
        # else remove one of the 'new_nodes' that create the cycle
        cycles = list(nx.simple_cycles(prov_blocking_graph))
        if len(cycles) == 0:
            list_coloring.append(new_nodes)
            colored_nodes = colored_nodes.union(new_nodes)

            proper_conds = deepcopy(prov_proper_conds)
            blocking_graph = deepcopy(prov_blocking_graph)
            empty_sets = deepcopy(prov_empty_sets)
        else:
            # remove one node of each cycle
            nodes_to_remove = set()
            for cycle in cycles:
                for n1, n2 in zip(cycle[:-1], cycle[1:]):
                    node = prov_blocking_graph.get_edge_data(n1, n2)["colored_node"]
                    if node in new_nodes:
                        nodes_to_remove.add(node)
                        break
            new_nodes.difference_update(nodes_to_remove)
            _process_new_nodes(
                new_nodes,
                proper_conds,
                blocking_graph,
                empty_sets,
                node_to_sets,
            )
            list_coloring.append(new_nodes)
            colored_nodes = colored_nodes.union(new_nodes)

    schedule = list_coloring_to_schedule(list_coloring)

    return schedule


def _process_new_nodes(
    new_nodes, proper_conds, blocking_graph, empty_sets, node_to_sets
) -> None:
    # release blocking edges if necessary
    for release, blocked in deepcopy(blocking_graph.edges):
        if release in new_nodes:
            blocking_edge = blocking_graph.get_edge_data(release, blocked)
            blocking_edge = blocking_edge["blocking_edge"]
            blocking_graph.remove_edge(release, blocked)
            proper_conds.remove_edge(*blocking_edge)

    # block nodes if needed (only done if the set is empty)
    for new_node in new_nodes:
        parallel_edges = [(new_node, n) for n in proper_conds.neighbors(new_node)]
        perpendicular_edges = [_perpendicular(e) for e in parallel_edges]
        for paral_edge, perp_edge in zip(parallel_edges, perpendicular_edges):
            if perp_edge in proper_conds.edges:
                proper_conds.remove_edge(*perp_edge)

                blocked_node = paral_edge[1]
                release_node = _release_node(new_node, perp_edge)
                blocking_graph.add_edge(
                    release_node,
                    blocked_node,
                    blocking_edge=paral_edge,
                    colored_node=new_node,
                )

    # track empty sets
    for new_node in new_nodes:
        for set_ in node_to_sets[new_node]:
            empty_sets.discard(set_)

    return


def _perpendicular(
    edge: tuple[tuple[str, str], tuple[str, str]]
) -> tuple[tuple[str, str], tuple[str, str]]:
    (q1, stab1), (q2, stab2) = edge
    return (q1, stab2), (q2, stab1)


def _release_node(
    node: tuple[str, str], perp_edge: tuple[tuple[str, str], tuple[str, str]]
) -> tuple[str, str]:
    n1, n2 = perp_edge
    if node[1] == n1[1]:
        return n1
    elif node[1] == n2[1]:
        return n2
    else:
        raise ValueError(
            f"'perp_edge={perp_edge}' is not perpendicular of 'node={node}'."
        )


def list_coloring_to_schedule(
    list_coloring: Sequence[set[str]],
) -> dict[str, list[str | None]]:
    """
    Formats a list of colored edges into a schedule for ``surface_sim``.

    Parameters
    ----------
    list_coloring
        Sequence of sets of qubit pairs corresponding to the CNOT layers
        in the schedule. The data qubits labels must start with ``"D"``,
        the X-type stabilizers with ``"X"``, and the Z-type stabilizers with ``"Z"``.
        The first element in the pair must correspond to the data qubit and
        the second element to the ancilla qubit.

    Returns
    -------
    schedule
        Dictionary with keys corresponding to ancilla qubits and values
        corresponding to the sequence of of CNOT layers with data qubits,
        with ``None`` if the ancilla qubit is not performing a CNOT.
    """
    anc_qubits = []
    for coloring in list_coloring:
        anc_qubits += [stab for q, stab in coloring]

    schedule = {anc: [None for _ in list_coloring] for anc in anc_qubits}
    for k, coloring in enumerate(list_coloring):
        for edge in coloring:
            anc, q = edge if edge[0] in anc_qubits else edge[1], edge[0]
            schedule[anc][k] = q

    return schedule


def get_overlap_stabilizers(tanner_graph: nx.Graph) -> dict[tuple[str, str], set[str]]:
    """
    Returns the overlap between X-type and Z-type stabilizers from the given
    tanner graph.

    Parameters
    ----------
    tanner_graph
        Tanner graph of the code. The data qubits labels must start with ``"D"``,
        the X-type stabilizers with ``"X"``, and the Z-type stabilizers with ``"Z"``.

    Returns
    -------
    stab_overlap
        Dictionary with keys corresponding to ``(z_stab, x_stab)`` and values
        corresponding to the data qubit that have support both in ``z_stab``
        and ``x_stab``.
    """
    if not isinstance(tanner_graph, nx.Graph):
        raise TypeError(
            f"'tanner_graph' must be a nx.Graph, but {type(tanner_graph)} as given."
        )
    if not nx.algorithms.is_bipartite(tanner_graph):
        raise TypeError("'tanner_graph' must be a bipartite graph.")
    if any(
        (not isinstance(node, str)) or (node[0] not in {"D", "X", "Z"})
        for node in tanner_graph
    ):
        raise TypeError(
            "Node labels in 'tanner_graph' must start with 'D', 'X', or 'Z'."
        )

    data_qubits = {n for n in tanner_graph if n[0] == "D"}
    x_stabs = {n for n in tanner_graph if n[0] == "X"}
    z_stabs = {n for n in tanner_graph if n[0] == "Z"}

    stab_overlap = {}
    for data_qubit in data_qubits:
        neighbors = list(tanner_graph.neighbors(data_qubit))
        x_neighbors = {n for n in neighbors if n in x_stabs}
        z_neighbors = {n for n in neighbors if n in z_stabs}
        for z_stab, x_stab in product(z_neighbors, x_neighbors):
            data_from_z = set(tanner_graph.neighbors(z_stab))
            data_from_x = set(tanner_graph.neighbors(x_stab))
            overlap = data_from_z.intersection(data_from_x)
            stab_overlap[(z_stab, x_stab)] = overlap

    return stab_overlap


def check_schedule(
    schedule: dict[str, list[str | None]], tanner_graph: nx.Graph
) -> None:
    """
    Checks that the provided schedule (1) measures the correct stabilizers specified
    by the Tanner graph, (2) qubits do not perform more than one interaction
    in each layer, (3) is proper.

    Parameters
    ----------
    schedule
        Dictionary with keys corresponding to ancilla qubits and values
        corresponding to the sequence of of CNOT layers with data qubits,
        with ``None`` if the ancilla qubit is not performing a CNOT.
    tanner_graph
        Tanner graph of the code. The data qubits labels must start with ``"D"``,
        the X-type stabilizers with ``"X"``, and the Z-type stabilizers with ``"Z"``.
    """
    anc_qubits = [n for n in tanner_graph.nodes if n[0] in ("X", "Z")]
    for anc in anc_qubits:
        support = list(tanner_graph.neighbors(anc))
        interactions = [q for q in schedule[anc] if q is not None]
        if set(support) != set(interactions):
            raise ValueError(
                f"Ancilla qubit {anc} does not measure the correct data qubits."
            )
        if any(q[0] != "D" for q in interactions):
            raise ValueError(
                f"Ancilla qubit {anc} interacts with a qubit that is not a data qubit."
            )

    for k, interacted_qubits in enumerate(zip(*schedule.values(), strict=True)):
        interacted_qubits = [q for q in interacted_qubits if q is not None]
        if len(interacted_qubits) != len(set(interacted_qubits)):
            raise ValueError(
                f"Data qubits perform more than one operation in layer index {k}."
            )

    stabs_overlap = get_overlap_stabilizers(tanner_graph)
    for (z_stab, x_stab), overlap in stabs_overlap.items():
        z_order = [q if q in overlap else None for q in schedule[z_stab]]
        x_order = [q if q in overlap else None for q in schedule[x_stab]]
        num_x_before_z = 0
        for qubit in overlap:
            if x_order.index(qubit) < z_order.index(qubit):
                num_x_before_z += 1
        if num_x_before_z % 2 == 1:
            raise ValueError(f"Schedule is not proper for {z_stab} and {x_stab}.")

    return
