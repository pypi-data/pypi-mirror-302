"""QPU Computation registry"""

import importlib

from qstone.apps.PyMatching import PyMatching
from qstone.apps.RB import RB
from qstone.apps.VQE import VQE

# Regstiries mapping computation name to its class
_computation_registry = {
    "VQE": VQE,
    "RB": RB,
    "PyMatching": PyMatching,
}


def get_computation_src(src: str):
    """Extracts the computation src either from the standard set or from the user"""
    if src in _computation_registry:
        computation_src = _computation_registry[src]  # type: ignore [abstract]
    else:
        try:
            src_module, src_class = src.rsplit(".", 1)
            computation_src = getattr(importlib.import_module(src_module), src_class)
        except NameError as exc:
            raise Exception(
                f"{src} app not found in standard list or as a folder"
            ) from exc
    return computation_src
