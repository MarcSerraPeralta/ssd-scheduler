# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 12:11:27 2024

@author: joche
"""
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 15:32:22 2024

@author: joche
"""

import time
import networkx as nx
from networkx import bipartite
import matplotlib.pyplot as plt
import re
from itertools import product
import numpy as np
import winsound
start_time = time.time()

B= nx.Graph()
B.add_nodes_from(['X1','X2','X3','X4','X5','X6','X7','X8','X9','X10','X11','X12'], bipartite=0)  
B.add_nodes_from(['Z1','Z2','Z3','Z4','Z5','Z6','Z7','Z8','Z9','Z10','Z11','Z12'], bipartite=1)
B.add_nodes_from(['q_0','q_1','q_2','q_3','q_4','q_5','q_6','q_7','q_8','q_9','q_10','q_11','q_12',
                  'q_13','q_14','q_15','q_16','q_17','q_18','q_19','q_20','q_21','q_22','q_23',
                  'q_24','q_25','q_26','q_27','q_28','q_29'], bipartite=2)                 


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
B.add_edges_from(edges)



bottom_nodes = {n for n, d in B.nodes(data=True) if d['bipartite'] == 0}
middle_nodes = {n for n, d in B.nodes(data=True) if d['bipartite'] == 1}
top_nodes = set(B) - bottom_nodes - middle_nodes


bottom_nodes_sorted = sorted(bottom_nodes)
middle_nodes_sorted = sorted(middle_nodes)
top_nodes_sorted = sorted(top_nodes)



pos = {}
pos.update((n, (1, i)) for i, n in enumerate(bottom_nodes_sorted))
pos.update((n, (1, i + 14)) for i, n in enumerate(middle_nodes_sorted))
pos.update((n, (3, i)) for i, n in enumerate(top_nodes_sorted))

nx.draw(B, pos=pos, with_labels=True, font_size=10, node_size=50)
plt.show()

def find_neighbohrs(graph):
    neighbohrs = {}
    for n, d in graph.nodes(data=True):
         if d.get('bipartite') in [0,1]:
             neighbohrs[n]= list(graph.neighbors(n))
    return neighbohrs


def find_overlapping_neighbohrs(graph):
    overlaps = {}
    nodes = list(find_neighbohrs(graph).keys())
    for i in range(len(nodes)):
        for j in range(i, len(nodes)):
            if (i != j):
                node1 = nodes[i]
                node2 = nodes[j]
                overlap = set(find_neighbohrs(graph)[node1]).intersection(set(find_neighbohrs(graph)[node2]))
                if len(overlap) ==2:
                    overlaps[(node1, node2)] = list(overlap)
    return overlaps


overlapping_neighbohrs=[]
for (key1, key2), (value1, value2) in find_overlapping_neighbohrs(B).items():
    group_list = [
        {key1: value1},
        {key1: value2},
        {key2: value1},
        {key2: value2}
    ]
    overlapping_neighbohrs.append(group_list)

def starts_with(x):
    return x[0].upper()

def check_if_done(graph, edge_dicts):
    edges = [(list(edge.keys())[0], list(edge.values())[0]) for edge in edge_dicts]
    matching_dicts = [edge_dict for edge_dict, edge in zip(edge_dicts, edges) if graph.has_edge(*edge)]
    return matching_dicts
 
def dict_to_tuple(d):
    if isinstance(d, dict) and len(d) == 1:
        key, value = next(iter(d.items()))
        return (key, value)
    else:
        raise ValueError("The input must be a dictionary with a single key-value pair.")
        
def find_non_adjacent_edge(value, dictionary_list):
    key_value_pair = list(value[0].items())[0]
    key1, val1 = key_value_pair
    letter1, number1 = key1[0], val1.split('_')[1]
    for dictionary in dictionary_list:
        key2, val2 = list(dictionary.items())[0]
        letter2, number2 = key2[0], val2.split('_')[1]
        if letter1 != letter2 and number1 != number2:
            return dictionary
    return None

def groups_to_check(pair_groups, value_1, value_2):
    value_1_dict = {value_1[0]: value_1[1]}
    value_2_dict = {value_2[0]: value_2[1]}
    
    matching_groups = []
    for group in pair_groups:
        contains_value_1 = any(pair == value_1_dict for pair in group)
        contains_value_2 = any(pair == value_2_dict for pair in group)
        
        if contains_value_1 and not contains_value_2:
            matching_groups.append(group)
    return matching_groups

def check_end_number(tuple1, tuple2):
   
    num1 = int(tuple1[1].split('_')[1])
    num2 = int(tuple2[1].split('_')[1])

    if num1 == num2:
        return True
    else:
        return False
    

def finding_non_adjacent_in_subgraph(edges, target):
    target_start, target_end = target
    target_end_number = target_end.split('_')[-1]
    

    for edge in edges:
        edge_start, edge_end = edge
        edge_end_number = edge_end.split('_')[-1]
        if (edge_start[0] != target_start[0]) and (edge_end_number != target_end_number):
            return edge
    return None



def find_matching_number(dict_list, target_tuple):
 
    for dictionary in dict_list:
        for key, value in dictionary.items():
            if target_tuple in value:
                return key
    return None


def find_other_2(list1, list2):
    missing_dictionaries = []
    
    for dictionary in list2:
        if dictionary not in list1:
            missing_dictionaries.append(dictionary)
    
    return missing_dictionaries


    
def contains_duplicates(lst):
    seen = set()
    duplicates = set()
    for item in lst:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return duplicates
def all_lists_contain_elements(data):
    return all(len(sublist) > 0 for sublist in data)


def get_dict_with_lowest_number(data):

    min_number = float('inf')
    min_dict = {}


    for pair in data:
        dictionary, number = pair
        number = int(number)  
        if number < min_number:
            min_number = number
            min_dict = dictionary

    return min_dict
restarts = 0

def fourth_edge(list_1, list_2):

    list_1_tuples = [tuple(d.items()) for d in list_1]
    list_2_tuples = [tuple(d.items()) for d in list_2]


    difference = [dict(t) for t in list_2_tuples if t not in list_1_tuples]
    
    return difference

j=0
def edge_coloring(graph):
    edges_done = nx.Graph()
    matching = nx.Graph()
    g = graph.copy()
    matching_list = []
    removed_edges= nx.Graph()
    edge_colors = {}
    restart = 0
    k=0
    for i in range(0,100):
        
        if len(g.edges()) ==0 and len(removed_edges.edges())==0:
            if len(matching_list) != 6:
                edge_coloring(B)  
                return matching_list
            else:
                print(matching_list, 'len of coloring =', len(matching_list))
                restart+=1
                if restart==1:

                    return matching_list
                    
                
                
        for pair in overlapping_neighbohrs:
         
            k=0
            edges_done_from_pair = check_if_done(edges_done,pair)
            k = len(edges_done_from_pair)  
       
            if k==1:
                 
                 non_adjacent = find_non_adjacent_edge(edges_done_from_pair,pair)
                 if dict_to_tuple(non_adjacent) in g.edges():
                     g.remove_edge(*dict_to_tuple(non_adjacent))
                     removed_edges.add_edge(*dict_to_tuple(non_adjacent))
####################################################################################################  
            if k==2:
            
                if starts_with(dict_to_tuple(edges_done_from_pair[0])) == starts_with(dict_to_tuple(edges_done_from_pair[1])):
                    to_add_2 = find_other_2(edges_done_from_pair,pair)
                    for last_edge_to_add in to_add_2:
                        pair_to_check = groups_to_check(overlapping_neighbohrs, dict_to_tuple(last_edge_to_add), dict_to_tuple(edges_done_from_pair[0]))
                        if len(pair_to_check) == 0:
                            if dict_to_tuple(last_edge_to_add) not in g.edges():
                                g.add_edge(*dict_to_tuple(last_edge_to_add))
                                removed_edges.remove_edge(*dict_to_tuple(last_edge_to_add))
                            continue
                        pair_to_check = groups_to_check(overlapping_neighbohrs, dict_to_tuple(last_edge_to_add), dict_to_tuple(edges_done_from_pair[0]))[0]
                        edges_done_from_pair_to_check = check_if_done(edges_done,pair_to_check)
                        if len(edges_done_from_pair_to_check)==1:
                            if starts_with(dict_to_tuple(edges_done_from_pair_to_check[0])) == starts_with(dict_to_tuple(last_edge_to_add)):
                                if dict_to_tuple(last_edge_to_add) not in g.edges():
                                    g.add_edge(*dict_to_tuple(last_edge_to_add))
                                    removed_edges.remove_edge(*dict_to_tuple(last_edge_to_add))
                            if check_end_number(dict_to_tuple(edges_done_from_pair_to_check[0]),dict_to_tuple(last_edge_to_add)):
                                if dict_to_tuple(last_edge_to_add) not in g.edges():
                                    g.add_edge(*dict_to_tuple(last_edge_to_add))
                                    removed_edges.remove_edge(*dict_to_tuple(last_edge_to_add))
                        if len(edges_done_from_pair_to_check) ==2:

                               
                               if starts_with(dict_to_tuple(edges_done_from_pair_to_check[0])) == starts_with(dict_to_tuple(edges_done_from_pair_to_check[1])):
                                   if dict_to_tuple(last_edge_to_add) not in g.edges():
                                       g.add_edge(*dict_to_tuple(last_edge_to_add))
                                       removed_edges.remove_edge(*dict_to_tuple(last_edge_to_add))
                               if find_matching_number(matching_list,dict_to_tuple(edges_done_from_pair_to_check[0]))<find_matching_number(matching_list,dict_to_tuple(edges_done_from_pair_to_check[1])):
                                   non_adjacent = find_non_adjacent_edge([edges_done_from_pair_to_check[0]], pair_to_check)
                               if find_matching_number(matching_list,dict_to_tuple(edges_done_from_pair_to_check[1])) < find_matching_number(matching_list,dict_to_tuple(edges_done_from_pair_to_check[0])):
                                   non_adjacent = find_non_adjacent_edge([edges_done_from_pair_to_check[1]], pair_to_check)
                              
                               if last_edge_to_add != non_adjacent:
                                   if dict_to_tuple(last_edge_to_add) not in g.edges():
                                       g.add_edge(*dict_to_tuple(last_edge_to_add))
                                       removed_edges.remove_edge(*dict_to_tuple(last_edge_to_add))
                        if len(edges_done_from_pair_to_check) ==3 or len(edges_done_from_pair_to_check) ==4:
                            
                            if dict_to_tuple(last_edge_to_add) not in g.edges():
                                
                                g.add_edge(*dict_to_tuple(last_edge_to_add))
                                removed_edges.remove_edge(*dict_to_tuple(last_edge_to_add))
###############################################################################################                        
                if find_matching_number(matching_list,dict_to_tuple(edges_done_from_pair[0]))<find_matching_number(matching_list,dict_to_tuple(edges_done_from_pair[1])):
                   non_adjacent = find_non_adjacent_edge([edges_done_from_pair[0]], pair)
                if find_matching_number(matching_list,dict_to_tuple(edges_done_from_pair[1])) < find_matching_number(matching_list,dict_to_tuple(edges_done_from_pair[0])):
                   non_adjacent = find_non_adjacent_edge([edges_done_from_pair[1]], pair)
                edges_done_from_pair.append(non_adjacent)
                last_edge_to_add = fourth_edge(edges_done_from_pair,pair)
                pair_to_check = groups_to_check(overlapping_neighbohrs, dict_to_tuple(last_edge_to_add[0]), dict_to_tuple(edges_done_from_pair[0]))
               
                pair_to_check = groups_to_check(overlapping_neighbohrs, dict_to_tuple(last_edge_to_add[0]), dict_to_tuple(edges_done_from_pair[0]))[0]
                edges_done_from_pair_to_check = check_if_done(edges_done,pair_to_check)
               
####################################################################################################
            if k==3:
                
            
                last_edge_to_add = fourth_edge(edges_done_from_pair,pair)
                pair_to_check = groups_to_check(overlapping_neighbohrs, dict_to_tuple(last_edge_to_add[0]), dict_to_tuple(edges_done_from_pair[0]))
                if len(pair_to_check) == 0:
                    if dict_to_tuple(last_edge_to_add[0]) not in g.edges():
                        g.add_edge(*dict_to_tuple(last_edge_to_add[0]))
                        removed_edges.remove_edge(*dict_to_tuple(last_edge_to_add[0]))
                    continue
                pair_to_check = groups_to_check(overlapping_neighbohrs, dict_to_tuple(last_edge_to_add[0]), dict_to_tuple(edges_done_from_pair[0]))[0]
                edges_done_from_pair_to_check = check_if_done(edges_done,pair_to_check)
                if len(edges_done_from_pair_to_check)==1:
                    if starts_with(dict_to_tuple(edges_done_from_pair_to_check[0])) == starts_with(dict_to_tuple(last_edge_to_add[0])):
                        if dict_to_tuple(last_edge_to_add[0]) not in g.edges():
                            g.add_edge(*dict_to_tuple(last_edge_to_add[0]))
                            removed_edges.remove_edge(*dict_to_tuple(last_edge_to_add[0]))
                        
                    if check_end_number(dict_to_tuple(edges_done_from_pair_to_check[0]),dict_to_tuple(last_edge_to_add[0])):
                        if dict_to_tuple(last_edge_to_add[0]) not in g.edges():
                            g.add_edge(*dict_to_tuple(last_edge_to_add[0]))
                            removed_edges.remove_edge(*dict_to_tuple(last_edge_to_add[0]))
                if len(edges_done_from_pair_to_check)==2:
                    
                    if starts_with(dict_to_tuple(edges_done_from_pair_to_check[0])) == starts_with(dict_to_tuple(edges_done_from_pair_to_check[1])):
                        if dict_to_tuple(last_edge_to_add[0]) not in g.edges():
                            g.add_edge(*dict_to_tuple(last_edge_to_add[0]))
                            removed_edges.remove_edge(*dict_to_tuple(last_edge_to_add[0]))
                    if find_matching_number(matching_list,dict_to_tuple(edges_done_from_pair_to_check[0]))<find_matching_number(matching_list,dict_to_tuple(edges_done_from_pair_to_check[1])):
                        non_adjacent = find_non_adjacent_edge([edges_done_from_pair_to_check[0]], pair_to_check)
                    if find_matching_number(matching_list,dict_to_tuple(edges_done_from_pair_to_check[1])) < find_matching_number(matching_list,dict_to_tuple(edges_done_from_pair_to_check[0])):
                        non_adjacent = find_non_adjacent_edge([edges_done_from_pair_to_check[1]], pair_to_check)
                    if last_edge_to_add[0] != non_adjacent:
                        if dict_to_tuple(last_edge_to_add[0]) not in g.edges():
                            g.add_edge(*dict_to_tuple(last_edge_to_add[0]))
                            removed_edges.remove_edge(*dict_to_tuple(last_edge_to_add[0]))
                if len(edges_done_from_pair_to_check) ==3:
                    if dict_to_tuple(last_edge_to_add[0]) not in g.edges():
                        g.add_edge(*dict_to_tuple(last_edge_to_add[0]))
                        removed_edges.remove_edge(*dict_to_tuple(last_edge_to_add[0]))
                        continue
            if k==4:
                continue
                
                
        if restart==0:
            G = nx.line_graph(g) 
        else:
            break
        for pair in overlapping_neighbohrs:
            
            k=0
            edges_done_for_pair = check_if_done(edges_done,pair)
            k = len(edges_done_for_pair)  
            if k==0:
               
                edges = [(list(edge.keys())[0], list(edge.values())[0]) for edge in pair]
                if edges[0] in g.edges() and finding_non_adjacent_in_subgraph(edges,edges[0]) in g.edges():
                    G.add_edge(edges[0],finding_non_adjacent_in_subgraph(edges,edges[0]))
                if edges[1] in g.edges() and finding_non_adjacent_in_subgraph(edges,edges[1]) in g.edges():
                    G.add_edge(edges[1],finding_non_adjacent_in_subgraph(edges,edges[1]))
            
                adjusted_nodes = {}
                for node in G.nodes():
                    u, v = node
                    if not (u.startswith('X') or u.startswith('Z')):
                        u, v = v, u
                    adjusted_nodes[node] = (u, v)
        
                G= nx.relabel_nodes(G, adjusted_nodes)
            

        
     
            
        matching_choice = nx.maximal_independent_set(G)    
        
     
      
        graph_dict = {str(i):matching_choice}
     
        matching_list.append(graph_dict)
        g.remove_edges_from(matching_choice)
        edges_done.add_edges_from(matching_choice)
        

      
        if len(matching_list)>6:
            print("REMATCH DUE TO LENGTH")
            edge_coloring(B)
            return matching_list
        for edge in top_nodes:
            filtered_lists = [sublist for sublist in overlapping_neighbohrs if any(edge in d.values() for d in sublist)]
            
            if len(filtered_lists) ==4:
              
                list_done = []
                for pair in filtered_lists:
              
                    edges_done_for_pair = check_if_done(edges_done,pair)
                    find_matching_number(matching_list,edges_done_for_pair)
                    list_done.append(edges_done_for_pair)
   
                if all_lists_contain_elements(list_done):
                  
                    working_on_qubits = []
                    measurement_done =[]
                    
                    for j in range(0,4):
                        matching_number = []
                        for h in range(len(list_done[j])):
                        
                            matching_number.append([list_done[j][h], find_matching_number(matching_list,dict_to_tuple(list_done[j][h]))])
                     
                        for value in get_dict_with_lowest_number(matching_number).values():
                            working_on_qubits.append(value)
                        for key in get_dict_with_lowest_number(matching_number).keys():
                            measurement_done.append(key)
                        
                   
                    if edge not in working_on_qubits and len(contains_duplicates(measurement_done))==0:
                        print("FORCED RESTART DUE TO CYCLE")
                        edge_coloring(B)
                        return matching_list
        
def run_function_until_success():
    while True:
        try:
            edge_coloring(B)
            return  
        except IndexError as e:
            print(f"IndexError: {e}. Restarting the function...")
          
        except Exception as e:
            print(f"Unexpected Error: {e}. Restarting the function...")
          
            
run_function_until_success()


end_time = time.time()


elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")

6
duration = 1000  # milliseconds
freq = 440  # Hz
winsound.Beep(freq, duration)