from itertools import permutations
from collections import defaultdict


subgroups = {
    'Z1': [['q_1', 'q_2'], ['q_1', 'q_0'], ['q_2', 'q_3'], ['q_4', 'q_0'], ['q_4', 'q_3']],
    'Z2': [['q_8', 'q_4'], ['q_8', 'q_7'], ['q_6', 'q_5'], ['q_6', 'q_7'], ['q_4', 'q_5']],
    'Z3': [['q_12', 'q_11'], ['q_12', 'q_7'], ['q_9', 'q_10'], ['q_9', 'q_7'], ['q_11', 'q_10']],
    'Z4': [['q_16', 'q_15'], ['q_16', 'q_11'], ['q_15', 'q_14'], ['q_13', 'q_14'], ['q_13', 'q_11']],
    'Z5': [['q_1', 'q_18'], ['q_1', 'q_19'], ['q_18', 'q_17'], ['q_15', 'q_17'], ['q_15', 'q_19']],
    'Z6': [['q_20', 'q_2'], ['q_20', 'q_25'], ['q_2', 'q_18'], ['q_18', 'q_24'], ['q_24', 'q_25']],
    'Z7': [['q_20', 'q_26'], ['q_20', 'q_3'], ['q_5', 'q_3'], ['q_5', 'q_21'], ['q_26', 'q_21']],
    'Z8': [['q_6', 'q_9'], ['q_6', 'q_21'], ['q_22', 'q_9'], ['q_22', 'q_27'], ['q_27', 'q_21']],
    'Z9': [['q_22', 'q_28'], ['q_22', 'q_10'], ['q_13', 'q_23'], ['q_13', 'q_10'], ['q_23', 'q_28']],
    'Z10': [['q_17', 'q_14'], ['q_17', 'q_24'], ['q_14', 'q_23'], ['q_24', 'q_29'], ['q_23', 'q_29']],
    'Z11': [['q_26', 'q_27'], ['q_26', 'q_25'], ['q_27', 'q_28'], ['q_28', 'q_29'], ['q_25', 'q_29']],
    'Z12': [['q_8', 'q_0'], ['q_8', 'q_12'], ['q_0', 'q_19'], ['q_16', 'q_12'], ['q_16', 'q_19']],
    'X1': [['q_20', 'q_8'], ['q_20', 'q_19'], ['q_8', 'q_18'], ['q_18', 'q_5'], ['q_5', 'q_19']],
    'X2': [['q_0', 'q_9'], ['q_0', 'q_21'], ['q_12', 'q_3'], ['q_12', 'q_21'], ['q_9', 'q_3']],
    'X3': [['q_8', 'q_22'], ['q_8', 'q_13'], ['q_6', 'q_16'], ['q_6', 'q_13'], ['q_22', 'q_16']],
    'X4': [['q_12', 'q_17'], ['q_12', 'q_23'], ['q_17', 'q_10'], ['q_23', 'q_19'], ['q_10', 'q_19']],
    'X5': [['q_2', 'q_16'], ['q_2', 'q_14'], ['q_0', 'q_14'], ['q_0', 'q_24'], ['q_16', 'q_24']],
    'X6': [['q_1', 'q_26'], ['q_1', 'q_29'], ['q_17', 'q_26'], ['q_17', 'q_3'], ['q_3', 'q_29']],
    'X7': [['q_2', 'q_6'], ['q_2', 'q_27'], ['q_6', 'q_25'], ['q_4', 'q_27'], ['q_4', 'q_25']],
    'X8': [['q_5', 'q_28'], ['q_5', 'q_10'], ['q_26', 'q_10'], ['q_26', 'q_7'], ['q_28', 'q_7']],
    'X9': [['q_14', 'q_9'], ['q_14', 'q_27'], ['q_9', 'q_29'], ['q_11', 'q_27'], ['q_11', 'q_29']],
    'X10': [['q_18', 'q_13'], ['q_18', 'q_28'], ['q_15', 'q_28'], ['q_15', 'q_25'], ['q_13', 'q_25']],
    'X11': [['q_20', 'q_22'], ['q_20', 'q_23'], ['q_22', 'q_24'], ['q_24', 'q_21'], ['q_23', 'q_21']],
    'X12': [['q_1', 'q_11'], ['q_1', 'q_7'], ['q_4', 'q_15'], ['q_4', 'q_11'], ['q_15', 'q_7']],
}

edges = [
    ('Z1', 'q_0'), ('Z1', 'q_1'), ('Z1', 'q_2'), ('Z1', 'q_3'), ('Z1', 'q_4'),
    ('Z2', 'q_4'), ('Z2', 'q_5'), ('Z2', 'q_6'), ('Z2', 'q_7'), ('Z2', 'q_8'),
    ('Z3', 'q_7'), ('Z3', 'q_9'), ('Z3', 'q_10'), ('Z3', 'q_11'), ('Z3', 'q_12'),
    ('Z4', 'q_11'), ('Z4', 'q_13'), ('Z4', 'q_14'), ('Z4', 'q_15'), ('Z4', 'q_16'),
    ('Z5', 'q_15'), ('Z5', 'q_17'), ('Z5', 'q_18'), ('Z5', 'q_19'), ('Z5', 'q_1'),
    ('Z6', 'q_18'), ('Z6', 'q_2'), ('Z6', 'q_20'), ('Z6', 'q_24'), ('Z6', 'q_25'),
    ('Z7', 'q_20'), ('Z7', 'q_3'), ('Z7', 'q_5'), ('Z7', 'q_21'), ('Z7', 'q_26'),
    ('Z8', 'q_21'), ('Z8', 'q_6'), ('Z8', 'q_9'), ('Z8', 'q_27'), ('Z8', 'q_22'),
    ('Z9', 'q_22'), ('Z9', 'q_10'), ('Z9', 'q_13'), ('Z9', 'q_23'), ('Z9', 'q_28'),
    ('Z10', 'q_23'), ('Z10', 'q_14'), ('Z10', 'q_29'), ('Z10', 'q_24'), ('Z10', 'q_17'),
    ('Z11', 'q_29'), ('Z11', 'q_28'), ('Z11', 'q_27'), ('Z11', 'q_26'), ('Z11', 'q_25'),
    ('Z12', 'q_12'), ('Z12', 'q_0'), ('Z12', 'q_19'), ('Z12', 'q_4'), ('Z12', 'q_16'),
    ('X1', 'q_20'), ('X1', 'q_8'), ('X1', 'q_5'), ('X1', 'q_19'), ('X1', 'q_18'),
    ('X2', 'q_0'), ('X2', 'q_9'), ('X2', 'q_12'), ('X2', 'q_21'), ('X2', 'q_6'),
    ('X3', 'q_8'), ('X3', 'q_6'), ('X3', 'q_13'), ('X3', 'q_16'), ('X3', 'q_22'),
    ('X4', 'q_12'), ('X4', 'q_17'), ('X4', 'q_10'), ('X4', 'q_19'), ('X4', 'q_23'),
    ('X5', 'q_2'), ('X5', 'q_0'), ('X5', 'q_14'), ('X5', 'q_24'), ('X5', 'q_16'),
    ('X6', 'q_1'), ('X6', 'q_26'), ('X6', 'q_29'), ('X6', 'q_17'), ('X6', 'q_3'),
    ('X7', 'q_2'), ('X7', 'q_6'), ('X7', 'q_25'), ('X7', 'q_27'), ('X7', 'q_4'),
    ('X8', 'q_5'), ('X8', 'q_7'), ('X8', 'q_26'), ('X8', 'q_10'), ('X8', 'q_28'),
    ('X9', 'q_9'), ('X9', 'q_27'), ('X9', 'q_29'), ('X9', 'q_14'), ('X9', 'q_11'),
    ('X10', 'q_13'), ('X10', 'q_18'), ('X10', 'q_25'), ('X10', 'q_15'), ('X10', 'q_28'),
    ('X11', 'q_23'), ('X11', 'q_24'), ('X11', 'q_20'), ('X11', 'q_21'), ('X11', 'q_22'),
    ('X12', 'q_1'), ('X12', 'q_7'), ('X12', 'q_11'), ('X12', 'q_15'), ('X12', 'q_4'),
]


def is_edge_valid(edge, color, edge_color_map):
    node1, node2 = edge
    for other_edge, other_color in edge_color_map.items():
        if other_color == color:
            other_node1, other_node2 = other_edge
            if node1 in (other_node1, other_node2) or node2 in (other_node1, other_node2):
                return False
    return True


def count_permutations(edge_groups, num_colors):
    count = 1
    for group in edge_groups:
        count *= len(list(permutations(range(1, num_colors + 1), len(group))))
    return count


def backtrack_color_edges(edge_groups, num_colors, edge_color_map, current_group_index, total_permutations,
                          permutation_counter):
    if current_group_index == len(edge_groups):
        return True  # All groups have been successfully colored

    group = edge_groups[current_group_index]
    group_permutations = list(permutations(range(1, num_colors + 1), len(group)))
    total_permutations[current_group_index] = len(group_permutations)

    for coloring in group_permutations:
        permutation_counter[current_group_index] += 1
        valid = True
        temp_color_map = edge_color_map.copy()
        for edge, color in zip(group, coloring):
            if not is_edge_valid(edge, color, temp_color_map):
                valid = False
                break
            temp_color_map[edge] = color


        total_attempted = sum(permutation_counter)
        total_possible = count_permutations(edge_groups, num_colors)
        progress = (total_attempted / total_possible) * 100
        print(f"Progress: {progress:.2f}%")

        if valid and backtrack_color_edges(edge_groups, num_colors, temp_color_map, current_group_index + 1,
                                           total_permutations, permutation_counter):
            edge_color_map.update(temp_color_map)
            return True

    return False


def edge_coloring(edges, num_colors):

    edge_groups = [edges[i:i + 5] for i in range(0, len(edges), 5)]


    edge_color_map = {}

    total_permutations = [0] * len(edge_groups)
    permutation_counter = [0] * len(edge_groups)

    if backtrack_color_edges(edge_groups, num_colors, edge_color_map, 0, total_permutations, permutation_counter):
        return edge_color_map
    else:
        return None


num_colors = 5
colored_edges = edge_coloring(edges, num_colors)

if colored_edges:
    print("Found valid coloring:")
    print(colored_edges)
else:
    print("No valid coloring found.")
