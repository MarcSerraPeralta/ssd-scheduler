from surface_sim import Detectors
from surface_sim.setup import CircuitNoiseSetup
from surface_sim.models import CircuitNoiseModel, IncomingNoiseModel
from surface_sim.layouts import ssd_code
from surface_sim.experiments.small_stellated_dodecahedron_code import memory_experiment

from qec_util.distance import get_circuit_distance

layout = ssd_code(interaction_order="parallel-6")
setup = CircuitNoiseSetup()
setup.set_var_param("prob", 1e-3)
detectors = Detectors.from_layouts("pre-gate", layout, include_gauge_dets=False)

for NoiseModel in [IncomingNoiseModel, CircuitNoiseModel]:
    for rot_basis in [False, True]:
        model = NoiseModel.from_layouts(setup, layout)
        circuit = memory_experiment(
            layout=layout,
            model=model,
            detectors=detectors,
            num_rounds=3,
            anc_reset=True,
            rot_basis=rot_basis,
        )
        d_circ = get_circuit_distance(circuit)
        print(
            f"noise_model={NoiseModel.__name__} rot_basis={rot_basis} d_circ={d_circ}"
        )
