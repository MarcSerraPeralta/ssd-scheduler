# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 14:55:53 2024

@author: joche
"""
from collections import defaultdict

def is_valid_coloring(edge_colors, adjacency_list, u, v, color):
  
    for neighbor in adjacency_list[u]:
        if (u, neighbor) in edge_colors and edge_colors[(u, neighbor)] == color:
            return False
    for neighbor in adjacency_list[v]:
        if (v, neighbor) in edge_colors and edge_colors[(v, neighbor)] == color:
            return False
    return True

def backtrack_edge_coloring(edges, adjacency_list, max_colors, edge_colors, index):
    if index == len(edges):
        return True
    
    u, v = edges[index]
    for color in range(1, max_colors + 1):
        if is_valid_coloring(edge_colors, adjacency_list, u, v, color):
            edge_colors[(u, v)] = color
            edge_colors[(v, u)] = color
            if backtrack_edge_coloring(edges, adjacency_list, max_colors, edge_colors, index + 1):
                return True
            del edge_colors[(u, v)]
            del edge_colors[(v, u)]
    
    return False

def find_minimum_edge_coloring(edges):

    adjacency_list = defaultdict(set)
    for u, v in edges:
        adjacency_list[u].add(v)
        adjacency_list[v].add(u)

    max_possible_colors = len(edges)
    for num_colors in range(1, max_possible_colors + 1):
        edge_colors = {}
        if backtrack_edge_coloring(edges, adjacency_list, num_colors, edge_colors, 0):
            return edge_colors, num_colors
    return None, None


edges = [
    ('Z1','q_0'), ('Z1','q_1'), ('Z1','q_2'), ('Z1','q_3'), ('Z1','q_4'),
    ('Z2','q_4'), ('Z2','q_5'), ('Z2','q_6'), ('Z2','q_7'), ('Z2','q_8'),
    ('Z3','q_7'), ('Z3','q_9'), ('Z3','q_10'), ('Z3','q_11'), ('Z3','q_12'),
    ('Z4','q_11'), ('Z4','q_13'), ('Z4','q_14'), ('Z4','q_15'), ('Z4','q_16'),
    ('Z5','q_15'), ('Z5','q_17'), ('Z5','q_18'), ('Z5','q_19'), ('Z5','q_1'),
    ('Z6','q_18'), ('Z6','q_2'), ('Z6','q_20'), ('Z6','q_24'), ('Z6','q_25'),
    ('Z7','q_20'), ('Z7','q_3'), ('Z7','q_5'), ('Z7','q_21'), ('Z7','q_26'),
    ('Z8','q_21'), ('Z8','q_6'), ('Z8','q_9'), ('Z8','q_27'), ('Z8','q_22'),
    ('Z9','q_22'), ('Z9','q_10'), ('Z9','q_13'), ('Z9','q_23'), ('Z9','q_28'),
    ('Z10','q_23'), ('Z10','q_14'), ('Z10','q_29'), ('Z10','q_24'), ('Z10','q_17'),
    ('Z11','q_29'), ('Z11','q_28'), ('Z11','q_27'), ('Z11','q_26'), ('Z11','q_25'),
    ('Z12','q_0'), ('Z12','q_8'), ('Z12','q_12'), ('Z12','q_16'), ('Z12','q_19'),
    ('X1','q_5'), ('X1','q_8'), ('X1','q_18'), ('X1','q_19'), ('X1','q_20'),
    ('X2','q_3'), ('X2','q_9'), ('X2','q_12'), ('X2','q_0'), ('X2','q_21'),
    ('X3','q_6'), ('X3','q_8'), ('X3','q_13'), ('X3','q_16'), ('X3','q_22'),
    ('X4','q_10'), ('X4','q_12'), ('X4','q_17'), ('X4','q_19'), ('X4','q_23'),
    ('X5','q_0'), ('X5','q_2'), ('X5','q_14'), ('X5','q_16'), ('X5','q_24'),
    ('X6','q_1'), ('X6','q_3'), ('X6','q_17'), ('X6','q_26'), ('X6','q_29'),
    ('X7','q_2'), ('X7','q_4'), ('X7','q_6'), ('X7','q_25'), ('X7','q_27'),
    ('X8','q_5'), ('X8','q_7'), ('X8','q_10'), ('X8','q_26'), ('X8','q_28'),
    ('X9','q_9'), ('X9','q_11'), ('X9','q_14'), ('X9','q_27'), ('X9','q_29'),
    ('X10','q_13'), ('X10','q_15'), ('X10','q_18'), ('X10','q_25'), ('X10','q_28'),
    ('X11','q_20'), ('X11','q_21'), ('X11','q_22'), ('X11','q_23'), ('X11','q_24'),
    ('X12','q_1'), ('X12','q_4'), ('X12','q_7'), ('X12','q_11'), ('X12','q_15')
]


edge_colors, num_colors = find_minimum_edge_coloring(edges)


if edge_colors:
    colored_edges = []
    for edge in edges:
        colored_edges.append((edge, edge_colors[(edge[0], edge[1])]))
    for edge, color in colored_edges:
        print(f"Edge {edge} has color {color}")
    print(f"Minimum number of colors used: {num_colors}")
else:
    print("No valid coloring found.")