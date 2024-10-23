# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 18:01:17 2024

@author: joche
"""
import stim
import numpy as np
import random 
from pymatching import Matching

matching =[{'0': [('Z11', 'q_26'), ('X3', 'q_8'), ('X7', 'q_2'), ('X5', 'q_16'), ('X1', 'q_19'), ('Z7', 'q_5'), ('X12', 'q_15'), ('Z1', 'q_0'), ('X4', 'q_12'), ('Z9', 'q_10'), ('X6', 'q_3'), ('X10', 'q_25'), ('X11', 'q_23'), ('X2', 'q_9'), ('Z2', 'q_4'), ('X9', 'q_29'), ('Z3', 'q_11'), ('Z8', 'q_22'), ('Z4', 'q_13'), ('Z6', 'q_20'), ('X8', 'q_7'), ('Z5', 'q_17')]},
 {'1': [('Z4', 'q_16'), ('Z6', 'q_2'), ('Z3', 'q_7'), ('Z10', 'q_23'), ('X5', 'q_0'), ('Z8', 'q_27'), ('X3', 'q_13'), ('X4', 'q_10'), ('X1', 'q_8'), ('X2', 'q_21'), ('X12', 'q_11'), ('Z9', 'q_28'), ('Z11', 'q_29'), ('X10', 'q_18'), ('X7', 'q_25'), ('X11', 'q_22'), ('Z7', 'q_20'), ('Z5', 'q_19'), ('X9', 'q_14'), ('X6', 'q_17'), ('Z12', 'q_12'), ('X8', 'q_5'), ('Z1', 'q_3')]}, 
{'2': [('Z6', 'q_24'), ('Z2', 'q_8'), ('X10', 'q_28'), ('X1', 'q_5'), ('X3', 'q_22'), ('X2', 'q_3'), ('Z11', 'q_25'), ('Z7', 'q_21'), ('Z9', 'q_23'), ('X7', 'q_4'), ('X12', 'q_1'), ('Z1', 'q_2'), ('X9', 'q_11'), ('Z8', 'q_6'), ('Z3', 'q_9'), ('Z4', 'q_15'), ('X5', 'q_14'), ('X6', 'q_26'), ('X11', 'q_20'), ('X8', 'q_10'), ('Z12', 'q_0'), ('Z10', 'q_17'), ('X4', 'q_19')]}, 
{'3': [('X3', 'q_6'), ('Z9', 'q_13'), ('Z2', 'q_7'), ('Z4', 'q_11'), ('X11', 'q_24'), ('X9', 'q_27'), ('Z7', 'q_3'), ('Z11', 'q_28'), ('X10', 'q_15'), ('Z10', 'q_14'), ('X1', 'q_20'), ('X4', 'q_17'), ('X2', 'q_0'), ('Z12', 'q_19'), ('Z3', 'q_10'), ('Z5', 'q_1'), ('Z8', 'q_9'), ('Z6', 'q_18'), ('X6', 'q_29'), ('X5', 'q_2'), ('X12', 'q_4')]}, 
{'4': [('X1', 'q_18'), ('Z2', 'q_6'), ('Z8', 'q_21'), ('X2', 'q_12'), ('X5', 'q_24'), ('X8', 'q_28'), ('X7', 'q_27'), ('X3', 'q_16'), ('Z10', 'q_29'), ('Z9', 'q_22'), ('Z4', 'q_14'), ('X4', 'q_23'), ('X9', 'q_9'), ('Z7', 'q_26'), ('X10', 'q_13'), ('Z5', 'q_15'), ('Z6', 'q_25'), ('X6', 'q_1'), ('X12', 'q_7'), ('Z12', 'q_8'), ('Z1', 'q_4')]},
 {'5': [('Z2', 'q_5'), ('Z1', 'q_1'), ('X11', 'q_21'), ('Z3', 'q_12'), ('X8', 'q_26'), ('Z10', 'q_24'), ('Z11', 'q_27'), ('Z12', 'q_16'), ('Z5', 'q_18'), ('X7', 'q_6')]}]


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
    ('Z12','q_0'), ('Z12','q_8'), ('Z12',' 2'), ('Z12','q_16'), ('Z12','q_19'),

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
def check_all_elements_presence(group):

    elements = [f'X{i}' for i in range(1, 5)] + [f'Z{i}' for i in range(1, 5)]


    presence_dict = {}
    

    for element in elements:
       
        presence_dict[element] = any(pair[0] == element for pair in group)
    
    return presence_dict

def check_all_elements_data(group):

    elements = [f'q_{i}' for i in range(0,30)]


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
    coords = stim.Circuit(
        """
        
        QUBIT_COORDS(0,-1.5632) 0
QUBIT_COORDS(1.4864,-0.4832) 1
QUBIT_COORDS(0.9186,1.2648) 2
QUBIT_COORDS(-0.9186,1.2648) 3
QUBIT_COORDS(-1.4864,-0.4832) 4
QUBIT_COORDS(-0.516,-0.71) 5
QUBIT_COORDS(0.516,-0.71) 6
QUBIT_COORDS(0.8346,0.2712) 7
QUBIT_COORDS(0,0.878) 8
QUBIT_COORDS(-0.8346,0.2712) 9
QUBIT_COORDS(0,0) 10
QUBIT_COORDS(2,-2) 11

QUBIT_COORDS(2,-2) 53
QUBIT_COORDS(0,0) 52
QUBIT_COORDS(-0.8346,0.2712) 51
QUBIT_COORDS(0,0.878) 50
QUBIT_COORDS(0.8346,0.2712) 49
QUBIT_COORDS(0.516,-0.71) 48
QUBIT_COORDS(-0.516,-0.71) 47
QUBIT_COORDS(-1.4864,-0.4832) 46
QUBIT_COORDS(-0.9186,1.2648) 45
QUBIT_COORDS(0.9186,1.2648) 44
QUBIT_COORDS(1.4864,-0.4832) 43
QUBIT_COORDS(0,-1.5632) 42

        
        
        QUBIT_COORDS(-0.0005,-1.995) 12
        QUBIT_COORDS(-1.2035,-1.656) 13
        QUBIT_COORDS(-0.4785,-1.2545) 14
        QUBIT_COORDS(0.4785,-1.2545) 15
        QUBIT_COORDS(1.203,-1.656) 16
        QUBIT_COORDS(1.045,-0.843) 17
        QUBIT_COORDS(1.3405,0.067) 18
        QUBIT_COORDS(1.9465,0.6325) 19
        QUBIT_COORDS(1.897,-0.6165) 20
        QUBIT_COORDS(1.124,0.734) 21
        QUBIT_COORDS(0.35,1.2965) 22
        QUBIT_COORDS(0,2.047) 23
        QUBIT_COORDS(1.1725,1.614) 24
        QUBIT_COORDS(-0.35,1.2965) 25
        QUBIT_COORDS(-1.124,0.734) 26
        QUBIT_COORDS(-1.9465,0.6325) 27
        QUBIT_COORDS(-1.1725,1.614) 28
        QUBIT_COORDS(-1.341,0.0675) 29
        QUBIT_COORDS(-1.0455,-0.8425) 30
        QUBIT_COORDS(-1.8975,-0.6165) 31
        QUBIT_COORDS(0,-0.853) 32
        QUBIT_COORDS(0.811,-0.264) 33
        QUBIT_COORDS(0.501,0.6905) 34
        QUBIT_COORDS(-0.501,0.6905) 35
        QUBIT_COORDS(-0.8115,-0.2635) 36
        QUBIT_COORDS(-0.2245,-0.3365) 37
        QUBIT_COORDS(0.2445,-0.3365) 38
        QUBIT_COORDS(0.3955,0.1285) 39
        QUBIT_COORDS(0,0.416) 40
        QUBIT_COORDS(-0.3955,0.1285) 41
        
        
        
       
        """)
    hadamard = stim.Circuit()
    for i in range(0,42):
        hadamard.append('H',[int(i)])
    
    for i in range(len(matching)):
        k=0
        for j in range(len(matching[i][str(i)])):
            measurement = (matching[i][str(i)][j])
            if starts_with(measurement[0])=='X':
                sliced_X = int(measurement[0][1:])-1
                sliced_qubit = int(measurement[1][2:])+12
             
                circuit.append("CNOT", [sliced_X, sliced_qubit])
                k+=1
            if starts_with(measurement[0])=='Z':
                sliced_Z = int(measurement[0][1:])+41
                sliced_qubit = int(measurement[1][2:])+12
                circuit.append("CNOT", [sliced_qubit,sliced_Z])
                k+=1
    
        
    for i in range(len(matching)):
        k=0
        for j in range(len(matching[i][str(i)])):
            measurement = (matching[i][str(i)][j])
            if starts_with(measurement[0])=='X':
                sliced_X = int(measurement[0][1:])-1
                sliced_qubit = int(measurement[1][2:])+12
                circuit_noise_2.append("CNOT", [sliced_X, sliced_qubit])
                k+=1
            if starts_with(measurement[0])=='Z':
                sliced_Z = int(measurement[0][1:])+41
                sliced_qubit = int(measurement[1][2:])+12
                circuit_noise_2.append("CNOT", [sliced_qubit,sliced_Z])
                k+=1

    for i in range(0,12):
        circuit.append('MRX',[int(i)])
    for j in range(42,54): 
        circuit.append('MR',[int(j)])
        
    
    
        
    for i in range(0,12):
        circuit_noise_2.append('MRX',[int(i)])
    for j in range(12,42): 
        circuit_noise_2.append('MR',[int(j)])
  
    for j in range(0,24):
        circuit_noise_2.append("DETECTOR", [stim.target_rec(-j-25), stim.target_rec(-j-1)]) 
        
    stable_circuit = stim.Circuit()

    stable_circuit += circuit_noise_2
    
    noisy_stable_circuit = stim.Circuit()
    for i in range(0,12):
        noisy_stable_circuit.append('Z_ERROR',[int(i)],2/3*p)
        
        noisy_stable_circuit.append('X_ERROR',[int(i)+42],2/3*p)
    
    for i in range(len(matching)):
        k=0
        for j in range(len(matching[i][str(i)])):
            measurement = (matching[i][str(i)][j])
            if starts_with(measurement[0])=='X':
                sliced_X = int(measurement[0][1:])-1
                sliced_qubit = int(measurement[1][2:])+12
                noisy_stable_circuit.append("CNOT", [sliced_X, sliced_qubit])
                noisy_stable_circuit.append('DEPOLARIZE2',[sliced_X, sliced_qubit],p)
                k+=1
            if starts_with(measurement[0])=='Z':
                sliced_Z = int(measurement[0][1:])+41
                sliced_qubit = int(measurement[1][2:])+12
                noisy_stable_circuit.append("CNOT", [sliced_qubit,sliced_Z])
                noisy_stable_circuit.append('DEPOLARIZE2',[sliced_Z, sliced_qubit],p)
                k+=1
        for X,j in check_all_elements_presence(matching[i][str(i)]).items():
    
            if X[0] =='X':
                sliced_X = int(X[1])-1
        
            else:
                sliced_X = int(X[1])+41
            if j == False:
                noisy_stable_circuit.append("DEPOLARIZE1",[sliced_X],p)
        for X,j in check_all_elements_data(matching[i][str(i)]).items():
            
            
            
            sliced_X = int(X[2:])+12
 
            
            if j == False:
                noisy_stable_circuit.append("DEPOLARIZE1",[sliced_X],p)    
     

    for i in range(0,12):
       
        noisy_stable_circuit.append('MX',[int(i)])

    for j in range(42,54): 

        noisy_stable_circuit.append('M',[int(j)])
      
    noisy_stable_circuit.append('TICK')
    for i in range(0,12):
   
        noisy_stable_circuit.append('RX',[int(i)])
        
        noisy_stable_circuit.append('Z_ERROR', [int(i)],2/3*p)
    for j in range(42,54): 

        noisy_stable_circuit.append('R',[int(j)])
        
        noisy_stable_circuit.append('X_ERROR', [int(j)],2/3*p)
    for j in range(0,24):
        noisy_stable_circuit.append("DETECTOR", [stim.target_rec(-j-25), stim.target_rec(-j-1)])   
       
    
    full_circuit = stim.Circuit()

    full_circuit = coords+hadamard+circuit+noisy_stable_circuit*6
    
    
    
  

    for h in range(0,30):
        full_circuit.append('MRX',[h+12] )    
        full_circuit.append('Z_ERROR', [h+12],2/3*p)
    
    full_circuit.append('OBSERVABLE_INCLUDE', [stim.target_rec(-4),stim.target_rec(-5),stim.target_rec(-10)],0)
    full_circuit.append('OBSERVABLE_INCLUDE', [stim.target_rec(-1),stim.target_rec(-6),stim.target_rec(-5)],1)
    full_circuit.append('OBSERVABLE_INCLUDE', [stim.target_rec(-4),stim.target_rec(-9),stim.target_rec(-3)],2)
    full_circuit.append('OBSERVABLE_INCLUDE', [stim.target_rec(-21),stim.target_rec(-24),stim.target_rec(-23)],3)
    full_circuit.append('OBSERVABLE_INCLUDE', [stim.target_rec(-29),stim.target_rec(-28),stim.target_rec(-12)],4)
    full_circuit.append('OBSERVABLE_INCLUDE', [stim.target_rec(-28),stim.target_rec(-27),stim.target_rec(-5),stim.target_rec(-4)],5)
    full_circuit.append('OBSERVABLE_INCLUDE', [stim.target_rec(-20),stim.target_rec(-19),stim.target_rec(-17)],6)
    full_circuit.append('OBSERVABLE_INCLUDE', [stim.target_rec(-1),stim.target_rec(-6),stim.target_rec(-10),stim.target_rec(-19),stim.target_rec(-4),stim.target_rec(-23),stim.target_rec(-22),stim.target_rec(-14)],7)


    full_circuit.append('DETECTOR',[stim.target_rec(-25),stim.target_rec(-22),stim.target_rec(-12),stim.target_rec(-11),stim.target_rec(-10),stim.target_rec(-54)])
    full_circuit.append('DETECTOR',[stim.target_rec(-27),stim.target_rec(-21),stim.target_rec(-18),stim.target_rec(-30),stim.target_rec(-9),stim.target_rec(-53)])
    full_circuit.append('DETECTOR',[stim.target_rec(-24),stim.target_rec(-22),stim.target_rec(-17),stim.target_rec(-14),stim.target_rec(-8),stim.target_rec(-52)])
    full_circuit.append('DETECTOR',[stim.target_rec(-20),stim.target_rec(-18),stim.target_rec(-13),stim.target_rec(-11),stim.target_rec(-7),stim.target_rec(-51)])
    full_circuit.append('DETECTOR',[stim.target_rec(-30),stim.target_rec(-28),stim.target_rec(-16),stim.target_rec(-14),stim.target_rec(-6),stim.target_rec(-50)])
    full_circuit.append('DETECTOR',[stim.target_rec(-29),stim.target_rec(-27),stim.target_rec(-13),stim.target_rec(-4),stim.target_rec(-1),stim.target_rec(-49)])
    full_circuit.append('DETECTOR',[stim.target_rec(-28),stim.target_rec(-26),stim.target_rec(-24),stim.target_rec(-5),stim.target_rec(-3),stim.target_rec(-48)])
    full_circuit.append('DETECTOR',[stim.target_rec(-25),stim.target_rec(-23),stim.target_rec(-20),stim.target_rec(-4),stim.target_rec(-2),stim.target_rec(-47)])
    full_circuit.append('DETECTOR',[stim.target_rec(-21),stim.target_rec(-19),stim.target_rec(-16),stim.target_rec(-3),stim.target_rec(-1),stim.target_rec(-46)])
    full_circuit.append('DETECTOR',[stim.target_rec(-17),stim.target_rec(-15),stim.target_rec(-12),stim.target_rec(-5),stim.target_rec(-2),stim.target_rec(-45)])
    full_circuit.append('DETECTOR',[stim.target_rec(-10),stim.target_rec(-9),stim.target_rec(-8),stim.target_rec(-7),stim.target_rec(-6),stim.target_rec(-44)])
    full_circuit.append('DETECTOR',[stim.target_rec(-29),stim.target_rec(-26),stim.target_rec(-23),stim.target_rec(-19),stim.target_rec(-15),stim.target_rec(-43)])
    
    
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

#shot(sampler.sample(shots=1))


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

