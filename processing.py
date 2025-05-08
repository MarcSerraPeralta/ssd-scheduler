from copy import deepcopy

SSD_LAYOUT_DICT = {
    "code": "smallest_stellated_dodecahedron",
    "logical_qubits": {
        "L1": {"ind": 0, "log_x": [], "log_z": []},
        "L2": {"ind": 1, "log_x": [], "log_z": []},
        "L3": {"ind": 2, "log_x": [], "log_z": []},
        "L4": {"ind": 3, "log_x": [], "log_z": []},
        "L5": {"ind": 4, "log_x": [], "log_z": []},
        "L6": {"ind": 5, "log_x": [], "log_z": []},
        "L7": {"ind": 6, "log_x": [], "log_z": []},
        "L8": {"ind": 7, "log_x": [], "log_z": []},
    },
    "distance": 3,
    "distance_x": 3,
    "distance_z": 3,
    "interaction_order": {"": []},
}

data = [
    {
        "qubit": "D1",
        "role": "data",
        "stab_type": None,
        "ind": 12,
        "neighbors": {
            "XA": "X2",
            "XB": "X5",
            "ZA": "Z1",
            "ZB": "Z12",
        },
        "coords": [-0.0005, -1.995],
    },
    {
        "qubit": "D2",
        "role": "data",
        "stab_type": None,
        "ind": 13,
        "neighbors": {
            "XA": "X6",
            "XB": "X12",
            "ZA": "Z1",
            "ZB": "Z5",
        },
        "coords": [-1.2035, -1.656],
    },
    {
        "qubit": "D3",
        "role": "data",
        "stab_type": None,
        "ind": 14,
        "neighbors": {
            "XA": "X5",
            "XB": "X7",
            "ZA": "Z1",
            "ZB": "Z6",
        },
        "coords": [-0.4785, -1.2545],
    },
    {
        "qubit": "D4",
        "role": "data",
        "stab_type": None,
        "ind": 15,
        "neighbors": {
            "XA": "X2",
            "XB": "X6",
            "ZA": "Z1",
            "ZB": "Z7",
        },
        "coords": [0.4785, -1.2545],
    },
    {
        "qubit": "D5",
        "role": "data",
        "stab_type": None,
        "ind": 16,
        "neighbors": {
            "XA": "X7",
            "XB": "X12",
            "ZA": "Z1",
            "ZB": "Z2",
        },
        "coords": [1.203, -1.656],
    },
    {
        "qubit": "D6",
        "role": "data",
        "stab_type": None,
        "ind": 17,
        "neighbors": {
            "XA": "X1",
            "XB": "X8",
            "ZA": "Z2",
            "ZB": "Z7",
        },
        "coords": [1.045, -0.843],
    },
    {
        "qubit": "D7",
        "role": "data",
        "stab_type": None,
        "ind": 18,
        "neighbors": {
            "XA": "X3",
            "XB": "X7",
            "ZA": "Z2",
            "ZB": "Z8",
        },
        "coords": [1.3405, 0.067],
    },
    {
        "qubit": "D8",
        "role": "data",
        "stab_type": None,
        "ind": 19,
        "neighbors": {
            "XA": "X8",
            "XB": "X12",
            "ZA": "Z2",
            "ZB": "Z3",
        },
        "coords": [1.9465, 0.6325],
    },
    {
        "qubit": "D9",
        "role": "data",
        "stab_type": None,
        "ind": 20,
        "neighbors": {
            "XA": "X1",
            "XB": "X3",
            "ZA": "Z2",
            "ZB": "Z12",
        },
        "coords": [1.897, -0.6165],
    },
    {
        "qubit": "D10",
        "role": "data",
        "stab_type": None,
        "ind": 21,
        "neighbors": {
            "XA": "X2",
            "XB": "X9",
            "ZA": "Z3",
            "ZB": "Z8",
        },
        "coords": [1.124, 0.734],
    },
    {
        "qubit": "D11",
        "role": "data",
        "stab_type": None,
        "ind": 22,
        "neighbors": {
            "XA": "X4",
            "XB": "X8",
            "ZA": "Z3",
            "ZB": "Z9",
        },
        "coords": [0.35, 1.2965],
    },
    {
        "qubit": "D12",
        "role": "data",
        "stab_type": None,
        "ind": 23,
        "neighbors": {
            "XA": "X9",
            "XB": "X12",
            "ZA": "Z3",
            "ZB": "Z4",
        },
        "coords": [0, 2.047],
    },
    {
        "qubit": "D13",
        "role": "data",
        "stab_type": None,
        "ind": 24,
        "neighbors": {
            "XA": "X2",
            "XB": "X4",
            "ZA": "Z3",
            "ZB": "Z12",
        },
        "coords": [1.1725, 1.614],
    },
    {
        "qubit": "D14",
        "role": "data",
        "stab_type": None,
        "ind": 25,
        "neighbors": {
            "XA": "X3",
            "XB": "X10",
            "ZA": "Z4",
            "ZB": "Z9",
        },
        "coords": [-0.35, 1.2965],
    },
    {
        "qubit": "D15",
        "role": "data",
        "stab_type": None,
        "ind": 26,
        "neighbors": {
            "XA": "X5",
            "XB": "X9",
            "ZA": "Z4",
            "ZB": "Z10",
        },
        "coords": [-1.124, 0.734],
    },
    {
        "qubit": "D16",
        "role": "data",
        "stab_type": None,
        "ind": 27,
        "neighbors": {
            "XA": "X10",
            "XB": "X12",
            "ZA": "Z4",
            "ZB": "Z5",
        },
        "coords": [-1.9465, 0.6325],
    },
    {
        "qubit": "D17",
        "role": "data",
        "stab_type": None,
        "ind": 28,
        "neighbors": {
            "XA": "X3",
            "XB": "X5",
            "ZA": "Z4",
            "ZB": "Z12",
        },
        "coords": [-1.1725, 1.614],
    },
    {
        "qubit": "D18",
        "role": "data",
        "stab_type": None,
        "ind": 29,
        "neighbors": {
            "XA": "X4",
            "XB": "X6",
            "ZA": "Z5",
            "ZB": "Z10",
        },
        "coords": [-1.341, 0.0675],
    },
    {
        "qubit": "D19",
        "role": "data",
        "stab_type": None,
        "ind": 30,
        "neighbors": {
            "XA": "X1",
            "XB": "X10",
            "ZA": "Z5",
            "ZB": "Z6",
        },
        "coords": [-1.0455, -0.8425],
    },
    {
        "qubit": "D20",
        "role": "data",
        "stab_type": None,
        "ind": 31,
        "neighbors": {
            "XA": "X1",
            "XB": "X4",
            "ZA": "Z5",
            "ZB": "Z12",
        },
        "coords": [-1.8975, -0.6165],
    },
    {
        "qubit": "D21",
        "role": "data",
        "stab_type": None,
        "ind": 32,
        "neighbors": {
            "XA": "X1",
            "XB": "X11",
            "ZA": "Z6",
            "ZB": "Z7",
        },
        "coords": [0, -0.853],
    },
    {
        "qubit": "D22",
        "role": "data",
        "stab_type": None,
        "ind": 33,
        "neighbors": {
            "XA": "X2",
            "XB": "X11",
            "ZA": "Z7",
            "ZB": "Z8",
        },
        "coords": [0.811, -0.264],
    },
    {
        "qubit": "D23",
        "role": "data",
        "stab_type": None,
        "ind": 34,
        "neighbors": {
            "XA": "X3",
            "XB": "X11",
            "ZA": "Z8",
            "ZB": "Z9",
        },
        "coords": [0.501, 0.6905],
    },
    {
        "qubit": "D24",
        "role": "data",
        "stab_type": None,
        "ind": 35,
        "neighbors": {
            "XA": "X4",
            "XB": "X11",
            "ZA": "Z9",
            "ZB": "Z10",
        },
        "coords": [-0.501, 0.6905],
    },
    {
        "qubit": "D25",
        "role": "data",
        "stab_type": None,
        "ind": 36,
        "neighbors": {
            "XA": "X5",
            "XB": "X11",
            "ZA": "Z6",
            "ZB": "Z10",
        },
        "coords": [-0.8115, -0.2635],
    },
    {
        "qubit": "D26",
        "role": "data",
        "stab_type": None,
        "ind": 37,
        "neighbors": {
            "XA": "X7",
            "XB": "X10",
            "ZA": "Z6",
            "ZB": "Z11",
        },
        "coords": [-0.2245, -0.3365],
    },
    {
        "qubit": "D27",
        "role": "data",
        "stab_type": None,
        "ind": 38,
        "neighbors": {
            "XA": "X6",
            "XB": "X8",
            "ZA": "Z7",
            "ZB": "Z11",
        },
        "coords": [0.2445, -0.3365],
    },
    {
        "qubit": "D28",
        "role": "data",
        "stab_type": None,
        "ind": 39,
        "neighbors": {
            "XA": "X7",
            "XB": "X9",
            "ZA": "Z8",
            "ZB": "Z11",
        },
        "coords": [0.3955, 0.1285],
    },
    {
        "qubit": "D29",
        "role": "data",
        "stab_type": None,
        "ind": 40,
        "neighbors": {
            "XA": "X8",
            "XB": "X10",
            "ZA": "Z9",
            "ZB": "Z11",
        },
        "coords": [0, 0.416],
    },
    {
        "qubit": "D30",
        "role": "data",
        "stab_type": None,
        "ind": 41,
        "neighbors": {
            "XA": "X6",
            "XB": "X9",
            "ZA": "Z10",
            "ZB": "Z11",
        },
        "coords": [-0.3955, 0.1285],
    },
]


COORDS = [
    [0, -1.5632],
    [1.4864, -0.4832],
    [0.9186, 1.2648],
    [-0.9186, 1.2648],
    [-1.4864, -0.4832],
    [-0.516, -0.71],
    [0.516, -0.71],
    [0.8346, 0.2712],
    [0, 0.878],
    [-0.8346, 0.2712],
    [0.05, -0.05],
    [-0.05, 0.05],
]
ancillas = {
    f"X{i+1}": {
        "qubit": f"X{i+1}",
        "role": "anc",
        "stab_type": "x_type",
        "ind": i + 30 + 12,
        "neighbors": {},
        "coords": [COORDS[i][0] + 0.05, COORDS[i][1] + 0.05],
    }
    for i in range(12)
}
ancillas |= {
    f"Z{i+1}": {
        "qubit": f"Z{i+1}",
        "role": "anc",
        "stab_type": "z_type",
        "ind": i - 1,
        "neighbors": {},
        "coords": [COORDS[i][0] - 0.05, COORDS[i][1] - 0.05],
    }
    for i in range(12)
}

for qubit_info in data:
    n = qubit_info["qubit"]
    ind_to_label = {k: v for k, v in enumerate("ABCDE")}
    for anc in qubit_info["neighbors"].values():
        l = ind_to_label[len(ancillas[anc]["neighbors"])]
        ancillas[anc]["neighbors"][f"D{l}"] = n

ancillas = list(ancillas.values())
SSD_LAYOUT_DICT["layout"] = data + ancillas

import numpy as np

NEW_LAYOUT = deepcopy(SSD_LAYOUT_DICT["layout"])
for k, q_info in enumerate(NEW_LAYOUT):
    a, b = q_info["coords"]
    factor = 5
    SSD_LAYOUT_DICT["layout"][k]["coords"] = [
        float(np.round(a * factor, decimals=5)),
        float(np.round(b * factor, decimals=5)),
    ]

from surface_sim import Layout
from surface_sim.layouts import plot
import matplotlib.pyplot as plt

layout = Layout(SSD_LAYOUT_DICT)

fig, ax = plt.subplots()
plot(ax, layout, add_patches=False)
plt.show()
fig, ax = plt.subplots()
plot(ax, layout, add_patches=True)
plt.show()

print(SSD_LAYOUT_DICT)
# print(layout.to_dict())
# print(SSD_LAYOUT_DICT["layout"])
