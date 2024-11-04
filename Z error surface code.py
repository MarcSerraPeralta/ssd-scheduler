# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 17:24:44 2024

@author: joche
"""
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 18:01:17 2024

@author: joche
"""
import stim
import numpy as np
import random 
from pymatching import Matching

#matching = [{'0': [('Z1', 'q_0'), ('X2', 'q_1'), ('Z2', 'q_2'), ('Z3', 'q_4'), ('X3', 'q_5'), ('X4', 'q_7')]},
# {'1': [('Z4', 'q_5'), ('X2', 'q_0'), ('Z2', 'q_1'), ('Z3', 'q_3'), ('X3', 'q_4'), ('X4', 'q_6')]}, 
#{'2': [('X2', 'q_4'), ('Z2', 'q_5'), ('X1', 'q_2'), ('Z3', 'q_7'), ('X3', 'q_8'), ('Z1', 'q_3')]}, 
#{'3': [('X2', 'q_3'), ('Z2', 'q_4'), ('Z3', 'q_6'), ('X3', 'q_7'), ('Z4', 'q_8'), ('X1','q_1')]}]


matching = [{'0': [('Z1', 'q_0'), ('Z2', 'q_2'), ('X2', 'q_1'), ('X3', 'q_5'), ('Z3', 'q_4'), ('X4', 'q_7')]},
 {'1': [('X2', 'q_0'), ('X3', 'q_4'), ('X4', 'q_6'), ('Z1', 'q_3'), ('Z2', 'q_5'), ('Z3', 'q_7')]}, 
{'2': [('X1', 'q_2'), ('X2', 'q_4'), ('X3', 'q_8'), ('Z2', 'q_1'), ('Z3', 'q_3'), ('Z4', 'q_5')]}, 
{'3': [('X1', 'q_1'), ('X2', 'q_3'), ('X3', 'q_7'), ('Z2', 'q_4'), ('Z3', 'q_6'), ('Z4','q_8')]}]

def check_all_elements_presence(group):
    elements = [f'X{i}' for i in range(1, 5)] + [f'Z{i}' for i in range(1, 5)]
    presence_dict = {}
    

    for element in elements:
       
        presence_dict[element] = any(pair[0] == element for pair in group)
    
    return presence_dict

def check_all_elements_data(group):

    elements = [f'q_{i}' for i in range(0,9)]


    presence_dict = {}
    

    for element in elements:
       
        presence_dict[element] = any(pair[1] == element for pair in group)
    
    return presence_dict
def starts_with(x):
    return x[0].upper()

def find_qi_for_xi(matching, xi):
    qi_list = []
    for item in matching:
        for key, operations in item.items():
            for op, qi in operations:
                if op == xi:
                    qi_list.append(qi)
    return qi_list

p = 2*10**(-5)

def measurement_circuit(rounds):
    circuit = stim.Circuit()
    circuit_noise_2 = stim.Circuit()
    hadamard = stim.Circuit()
    for i in range(0,4):
        hadamard.append('H',[int(i)])
    
   
    
    for i in range(len(matching)):
        k=0
        for j in range(len(matching[i][str(i)])):
            measurement = (matching[i][str(i)][j])
            if starts_with(measurement[0])=='X':
                sliced_X = int(measurement[0][1:])-1
                sliced_qubit = int(measurement[1][2:])+4
                print(sliced_qubit)
                circuit.append("CNOT", [sliced_X, sliced_qubit])
                k+=1
            if starts_with(measurement[0])=='Z':
                sliced_Z = int(measurement[0][1:])+4+8
                sliced_qubit = int(measurement[1][2:])+4
                circuit.append("CNOT", [sliced_qubit,sliced_Z])
                k+=1
    
        
    for i in range(len(matching)):
        k=0
        for j in range(len(matching[i][str(i)])):
            measurement = (matching[i][str(i)][j])
            if starts_with(measurement[0])=='X':
                sliced_X = int(measurement[0][1:])-1
                sliced_qubit = int(measurement[1][2:])+4
                circuit_noise_2.append("CNOT", [sliced_X, sliced_qubit])
                k+=1
            if starts_with(measurement[0])=='Z':
                sliced_Z = int(measurement[0][1:])+4+8
                sliced_qubit = int(measurement[1][2:])+4
                circuit_noise_2.append("CNOT", [sliced_qubit,sliced_Z])
                k+=1

    for i in range(0,4):
        circuit.append('MRX',[int(i)])
    for j in range(13,17): 
        circuit.append('MR',[int(j)])
        
    
    
        
    for i in range(0,4):
        circuit_noise_2.append('MRX',[int(i)])
    for j in range(13,17): 
        circuit_noise_2.append('MR',[int(j)])
  
    for j in range(0,8):
        circuit_noise_2.append("DETECTOR", [stim.target_rec(-j-9), stim.target_rec(-j-1)]) 
        
    stable_circuit = stim.Circuit()

    stable_circuit += circuit_noise_2
    
    noisy_stable_circuit = stim.Circuit()
     
    for i in range(0,4):
        noisy_stable_circuit.append('Z_ERROR',[int(i)],2/3*p)
        
        noisy_stable_circuit.append('X_ERROR',[int(i)+13],2/3*p)
    for i in range(len(matching)):
        k=0
        for j in range(len(matching[i][str(i)])):
            measurement = (matching[i][str(i)][j])
            if starts_with(measurement[0])=='X':
                sliced_X = int(measurement[0][1:])-1
                sliced_qubit = int(measurement[1][2:])+4
                noisy_stable_circuit.append("CNOT", [sliced_X, sliced_qubit])
                noisy_stable_circuit.append('DEPOLARIZE2',[sliced_X, sliced_qubit],p)
                k+=1
            if starts_with(measurement[0])=='Z':
                sliced_Z = int(measurement[0][1:])+4+8
                sliced_qubit = int(measurement[1][2:])+4
                noisy_stable_circuit.append("CNOT", [sliced_qubit,sliced_Z])
                noisy_stable_circuit.append('DEPOLARIZE2',[sliced_Z, sliced_qubit],p)
                k+=1
        for X,j in check_all_elements_presence(matching[i][str(i)]).items():
            print(X[0], 'hier hier')
            if X[0] =='X':
                sliced_X = int(X[1:])-1
                print(sliced_X)
            else:
                sliced_X = int(X[1:])+4+8
            if j == False:
                noisy_stable_circuit.append("DEPOLARIZE1",[sliced_X],p)
                
        for X,j in check_all_elements_data(matching[i][str(i)]).items():
        
            sliced_X = int(X[2:])+4
            print(X,sliced_X,j, 'HIERRRR')
            
            if j == False:
                noisy_stable_circuit.append("DEPOLARIZE1",[sliced_X],p)
     

    for i in range(0,4):
        #noisy_stable_circuit.append('Z_error',[int(i)],2/3*p)
        noisy_stable_circuit.append('MRX',[int(i)])
        noisy_stable_circuit.append('Z_error',[int(i)],2/3*p)
    for j in range(13,17): 
        #noisy_stable_circuit.append('X_ERROR', [int(j)],2/3*p)
        noisy_stable_circuit.append('MR',[int(j)])
        noisy_stable_circuit.append('X_ERROR', [int(j)],2/3*p)
    for j in range(0,8):
       noisy_stable_circuit.append("DETECTOR", [stim.target_rec(-j-9), stim.target_rec(-j-1)])   
 
    
    full_circuit = stim.Circuit()

    full_circuit = hadamard+circuit+noisy_stable_circuit*6
    
    
    
  
    #for h in range(0,9):
    #    full_circuit.append('X_ERROR',[int(h)+4],0.1)
    for h in range(0,9):
        #full_circuit.append('X_ERROR', [h+4],p)
        full_circuit.append('MR',[h+4] )
        full_circuit.append('X_ERROR', [h+4],p)
        
    #full_circuit.append('OBSERVABLE_INCLUDE', [stim.target_rec(-1),stim.target_rec(-2),stim.target_rec(-3),stim.target_rec(-4),stim.target_rec(-5),stim.target_rec(-6),stim.target_rec(-7),stim.target_rec(-8),stim.target_rec(-9)],0)    
    
    full_circuit.append('OBSERVABLE_INCLUDE', [stim.target_rec(-9),stim.target_rec(-8),stim.target_rec(-7)],0)
    full_circuit.append('OBSERVABLE_INCLUDE', [stim.target_rec(-6),stim.target_rec(-5),stim.target_rec(-4)],1)
    full_circuit.append('OBSERVABLE_INCLUDE', [stim.target_rec(-3),stim.target_rec(-2),stim.target_rec(-1)],2)
    
    #full_circuit.append('OBSERVABLE_INCLUDE', [stim.target_rec(-9),stim.target_rec(-5),stim.target_rec(-1)],0)
    
    full_circuit.append('DETECTOR',[stim.target_rec(-9),stim.target_rec(-6),stim.target_rec(-13)])
    full_circuit.append('DETECTOR',[stim.target_rec(-8),stim.target_rec(-7),stim.target_rec(-5),stim.target_rec(-4),stim.target_rec(-12)])
    full_circuit.append('DETECTOR',[stim.target_rec(-6),stim.target_rec(-5),stim.target_rec(-3),stim.target_rec(-2),stim.target_rec(-11)])
    full_circuit.append('DETECTOR',[stim.target_rec(-1),stim.target_rec(-4),stim.target_rec(-10)])
    
    
   
    
    stable_circuit_2 = stim.Circuit()
    
    for i in range(len(matching)):
       k=0
       for j in range(len(matching[i][str(i)])):
           measurement = (matching[i][str(i)][j])
           if starts_with(measurement[0])=='X':
               sliced_X = int(measurement[0][1:])-1
               sliced_qubit = int(measurement[1][2:])+4
               stable_circuit_2.append("CNOT", [sliced_X, sliced_qubit])
               k+=1
           if starts_with(measurement[0])=='Z':
               sliced_Z = int(measurement[0][1:])+4+8
               sliced_qubit = int(measurement[1][2:])+4
               stable_circuit_2.append("CNOT", [sliced_qubit,sliced_Z])
               k+=1
    
   
    
    for i in range(0,4):
        
        stable_circuit_2.append('MRX',[int(i)])
    for j in range(13,17): 
        stable_circuit_2.append('M',[int(j)])
  
    for j in range(0,8):
        stable_circuit_2.append("DETECTOR", [stim.target_rec(-j-18), stim.target_rec(-j-1)]) 
    
    return full_circuit

gebouwd_circuit = measurement_circuit(2)
sampler = gebouwd_circuit.compile_detector_sampler()

def shot(result):
    k=0
    int_array = result.astype(int)
    str_array = np.where(int_array == 0, '_', int_array)

 
    flattened_array = str_array.flatten()


    for i in range(0, len(flattened_array), 8):
        row = flattened_array[i:i+8]
        print(''.join(map(str, row)))


shot(sampler.sample(shots=1))
detectors, flips = sampler.sample(shots=10000000,separate_observables=True)
#shot(sampler.sample(shots=1))
dem = gebouwd_circuit.detector_error_model(allow_gauge_detectors=True,decompose_errors=True)




mwpm = Matching(dem)
predictions = mwpm.decode_batch(detectors)



diagram_object = gebouwd_circuit.diagram("timeline-svg")
  
svg_content = str(diagram_object)
with open("circuit_diagram_test.svg", "w") as f:
    f.write(svg_content)

print("SVG diagram saved to 'circuit_diagram.svg'.")

print(len(gebouwd_circuit.shortest_graphlike_error()))  

p_values = 10**np.linspace(np.log10(1e-5), np.log10(1e-3), 21)


all_average_results = []
all_deviations = []


def run_experiment_for_p(p_value, rounds=2, bootstrap_samples=1000):
    # Set the global p value
    global p
    p = p_value
    

    gebouwd_circuit = measurement_circuit(rounds)
    
    sampler = gebouwd_circuit.compile_detector_sampler()

    average_results = []


    for i in range(20):
        shots = 10**6
        detectors, flips = sampler.sample(shots, separate_observables=True)
        dem = gebouwd_circuit.detector_error_model(allow_gauge_detectors=True, decompose_errors=True)
        mwpm = Matching(dem)
        predictions = mwpm.decode_batch(detectors)


        comparison_result = predictions != flips
        rows_with_differences = np.any(comparison_result, axis=1)

        different_rows_array1 = predictions[rows_with_differences]
        average_result = len(different_rows_array1) / shots

        average_results.append(average_result)
        print(f"Average of rows with differences for p={p_value}, iteration {i+1}: {average_result}")


    bootstrap_means = []
    for _ in range(bootstrap_samples):
        resample = np.random.choice(average_results, size=len(average_results), replace=True)
        bootstrap_mean = np.mean(resample)
        bootstrap_means.append(bootstrap_mean)


    bootstrap_std = np.std(bootstrap_means)
    print(f"Bootstrap standard deviation for p={p_value}: {bootstrap_std}")

    return average_results, bootstrap_std

for p_value in p_values:
    average_results, bootstrap_std = run_experiment_for_p(p_value)
    all_average_results.append(average_results)
    all_deviations.append(bootstrap_std)
    
for i in range(20):
    print(np.mean(all_average_results[i]))
for i in range(20):
    print(all_deviations[i])
