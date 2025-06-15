import pathlib
import matplotlib.pyplot as plt
import numpy as np

from qec_util.performance import confidence_interval_binomial, read_failures_from_file
from qec_util.performance.plots import plot_line_threshold

PROBS = [1e-5, 2e-5, 5e-5, 1e-4, 2e-4, 5e-4, 1e-3, 2e-3, 5e-3, 1e-2]
BASES = ["X", "Z"]

file_name_format = "ssd_CircuitNoiseModel_Matching_b{basis}_r3_p{prob:.5e}.txt"
DATA_DIR = pathlib.Path("data")

for basis in BASES:
    pl, pl_upper, pl_lower = [], [], []
    for prob in PROBS:
        file_name = file_name_format.format(basis=basis, prob=prob)
        num_failures, num_samples, _ = read_failures_from_file(DATA_DIR / file_name)
        pl.append(num_failures / num_samples)
        lower, upper = confidence_interval_binomial(num_failures, num_samples)
        pl_lower.append(lower)
        pl_upper.append(upper)

    pl, pl_upper, pl_lower = np.array(pl), np.array(pl_upper), np.array(pl_lower)
    probs = np.array(PROBS)

    fig, ax = plt.subplots()
    plot_line_threshold(ax, probs, pl / 3, pl_lower / 3, pl_upper / 3, label="SSD")
    ax.plot(probs, 8 * probs, "--", color="black", label="$8p$")
    ax.set_ylabel("logical error probability per round, $p_L/R$")
    ax.legend(loc="upper left")
    plt.show()
