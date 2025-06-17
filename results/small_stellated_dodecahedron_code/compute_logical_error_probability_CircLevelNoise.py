import pathlib
import os
import pickle

from surface_sim import Detectors
from surface_sim.setup import CircuitNoiseSetup
from surface_sim.models import CircuitNoiseModel
from surface_sim.layouts import ssd_code
from surface_sim.experiments.small_stellated_dodecahedron_code import memory_experiment

from qec_util.performance.samplers import sample_failures

from pymatching import Matching

# input parameters
probs = [1e-5, 2e-5, 5e-5, 1e-4, 2e-4, 5e-4, 1e-3, 2e-3, 5e-3, 1e-2]
bases = ["X", "Z"]
schedules = sorted([f for f in os.listdir("schedules") if f.endswith(".pickle")])
log_dir_name = "logical_performance"
schedules_dir_name = "schedules"

# compute threshold plot
schedules_dir = pathlib.Path(schedules_dir_name)
log_dir = pathlib.Path(log_dir_name)
log_dir.mkdir(exist_ok=True, parents=True)

for schedule_name in schedules:
    print(f"\r{schedule_name}", end="")
    with open(schedules_dir / schedule_name, "rb") as file:
        schedule = pickle.load(file)

    layout = ssd_code(interaction_order=schedule)
    setup = CircuitNoiseSetup()
    model = CircuitNoiseModel.from_layouts(setup, layout)
    detectors = Detectors.from_layouts("pre-gate", layout, include_gauge_dets=False)

    schedule_dir = pathlib.Path(schedule_name[:-7])
    (log_dir / schedule_dir).mkdir(exist_ok=True, parents=True)

    for prob in probs:
        print(f"\r{schedule_name} prob={prob}", end="")

        setup.set_var_param("prob", prob)
        for basis in bases:
            file_name = f"CircuitNoiseModel_Matching_b{basis}_r3_p{prob:.5e}.txt"
            circuit = memory_experiment(
                layout=layout,
                model=model,
                detectors=detectors,
                num_rounds=3,
                anc_reset=True,
                rot_basis=True if basis == "X" else False,
            )
            dem = circuit.detector_error_model()
            dem_decomposed = circuit.detector_error_model(decompose_errors=True)

            sample_failures(
                dem,
                Matching(dem_decomposed),
                max_failures=10_000,
                max_samples=1e8,
                batch_size=1_000_000,
                file_name=log_dir / schedule_dir / file_name,
            )

print("")
