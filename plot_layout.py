import matplotlib.pyplot as plt

from surface_sim import Layout
from surface_sim.layouts import plot
from surface_sim.layouts.library.small_stellated_dodecahedron_code import (
    SSD_LAYOUT_DICT,
)

layout = Layout(SSD_LAYOUT_DICT)

fig, ax = plt.subplots()
plot(ax, layout, add_patches=False)
plt.show()
