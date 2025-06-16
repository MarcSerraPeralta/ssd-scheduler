import os
import pathlib
import matplotlib.pyplot as plt
import numpy as np

from qec_util.performance import confidence_interval_binomial, read_failures_from_file
from qec_util.performance.plots import plot_line_threshold

# inputs
probs = [1e-5, 2e-5, 5e-5, 1e-4, 2e-4, 5e-4, 1e-3, 2e-3, 5e-3, 1e-2]
bases = ["X", "Z"]
log_dir_name = "logical_performance"
schedules = sorted([f for f in os.listdir(log_dir_name) if f != ".DS_Store"])
noise_model_name = "SI1000NoiseModel"
decoder = "Matching"
num_rounds = 3
data_file_name_format = (
    "{noise_model_name}_{decoder}_b{basis}_r{num_rounds}_p{prob:.5e}.txt"
)
plot_file_name_format = "{noise_model_name}_{decoder}_b{basis}_r{num_rounds}.pdf"

# plot performance of each schedule individually and store in corresponding dir
log_dir = pathlib.Path(log_dir_name)
for schedule in schedules:
    print(f"\r{schedule}", end="")
    for basis in bases:
        pl, pl_upper, pl_lower = [], [], []
        for prob in probs:
            file_name = data_file_name_format.format(
                basis=basis,
                prob=prob,
                noise_model_name=noise_model_name,
                num_rounds=num_rounds,
                decoder=decoder,
            )
            num_failures, num_samples, _ = read_failures_from_file(
                log_dir / schedule / file_name
            )
            pl.append(num_failures / num_samples)
            lower, upper = confidence_interval_binomial(num_failures, num_samples)
            pl_lower.append(lower)
            pl_upper.append(upper)

        pl, pl_upper, pl_lower = np.array(pl), np.array(pl_upper), np.array(pl_lower)
        probs = np.array(probs)

        fig, ax = plt.subplots()
        plot_line_threshold(
            ax,
            probs,
            pl / num_rounds,
            pl_lower / num_rounds,
            pl_upper / num_rounds,
            label="SSD",
        )
        ax.plot(probs, 8 * probs, "--", color="black", label="$8p$")

        m, b = np.polyfit(
            np.log10(probs[probs <= 1e-3]), np.log10(pl[probs <= 1e-3]), 1
        )
        ax.plot(
            probs[probs <= 1e-3],
            10 ** (m * np.log10(probs[probs <= 1e-3]) + b) / num_rounds,
            "--",
            color="gray",
            label=f"${{{b:0.3f}}}p^{{{m:0.2f}}}$",
        )

        ax.set_ylabel("logical error probability per round, $p_L/R$")
        ax.legend(loc="upper left")
        fig.tight_layout()
        plot_file_name = plot_file_name_format.format(
            basis=basis,
            noise_model_name=noise_model_name,
            num_rounds=num_rounds,
            decoder=decoder,
        )
        fig.savefig(log_dir / schedule / plot_file_name, format="pdf")
        plt.close()

print("")
