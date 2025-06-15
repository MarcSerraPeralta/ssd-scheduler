import pathlib

from surface_sim import Detectors
from surface_sim.setup import CircuitNoiseSetup
from surface_sim.models import CircuitNoiseModel
from surface_sim.layouts import ssd_code
from surface_sim.experiments.small_stellated_dodecahedron_code import memory_experiment

from qec_util.performance.samplers import sample_failures

from pymatching import Matching


PROBS = [1e-5, 2e-5, 5e-5, 1e-4, 2e-4, 5e-4, 1e-3, 2e-3, 5e-3, 1e-2]

layout = ssd_code(interaction_order="parallel-6")
setup = CircuitNoiseSetup()
model = CircuitNoiseModel.from_layouts(setup, layout)
detectors = Detectors.from_layouts("pre-gate", layout, include_gauge_dets=False)

DATA_DIR = pathlib.Path("data")
DATA_DIR.mkdir(exist_ok=True, parents=True)

for prob in PROBS:
    setup.set_var_param("prob", prob)
    for rot_basis in [False, True]:
        basis = "X" if rot_basis else "Z"
        file_name = (
            f"ssd_{CircuitNoiseModel.__name__}_Matching_b{basis}_r3_p{prob:.5e}.txt"
        )
        circuit = memory_experiment(
            layout=layout,
            model=model,
            detectors=detectors,
            num_rounds=3,
            anc_reset=True,
            rot_basis=rot_basis,
        )
        dem = circuit.detector_error_model()
        dem_decomposed = circuit.detector_error_model(decompose_errors=True)

        print(file_name)
        sample_failures(
            dem,
            Matching(dem_decomposed),
            max_failures=10_000,
            max_samples=1e8,
            batch_size=1_000_000,
            file_name=DATA_DIR / file_name,
        )
