from collections.abc import Sequence

from surface_sim import Detectors
from surface_sim.setup import CircuitNoiseSetup
from surface_sim.models import CircuitNoiseModel
from surface_sim.layouts import ssd_code
from surface_sim.experiments.small_stellated_dodecahedron_code import memory_experiment

from qec_util.distance import get_circuit_distance


def get_circuit_distance_from_schedule_for_ssd(
    schedule: dict[str, Sequence[str | None]]
) -> int:
    layout = ssd_code(interaction_order=schedule)
    setup = CircuitNoiseSetup()
    setup.set_var_param("prob", 1e-3)
    detectors = Detectors.from_layouts("pre-gate", layout, include_gauge_dets=False)

    d_circ = 999
    for rot_basis in [False, True]:
        model = CircuitNoiseModel.from_layouts(setup, layout)
        circuit = memory_experiment(
            layout=layout,
            model=model,
            detectors=detectors,
            num_rounds=2,
            anc_reset=True,
            rot_basis=rot_basis,
        )
        d_circ = min([d_circ, get_circuit_distance(circuit)])

    return d_circ
