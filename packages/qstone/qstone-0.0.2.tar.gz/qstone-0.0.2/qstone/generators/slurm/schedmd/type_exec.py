""" Wrapper to run different loads """

import os
import subprocess
import sys

from qstone.apps import get_computation_src
from qstone.connectors import connector

QPU_PORT: int = int(os.environ.get("QPU_PORT", "0"))
QPU_IP_ADDRESS: str = os.environ.get("QPU_IP_ADDRESS", "1.1.1.1")
CONNECTOR_TYPE = connector.ConnectorType[
    os.environ.get("CONNECTOR", "NO_LINK")
]  # type: ignore [arg-type]
LOCKFILE: str = os.environ.get("LOCKFILE", "qstone.lock")


def execute(compute_name: str, num_qubits: int, job_id: str):
    """Execute the computation steps via separate  calls

    Args:
        compute_name: Name of the computation in the registry
        job_id : id of the job to run
        num_qubits: the number of qubits to use in this run

    Returns the return code of query and step subprocess execution
    """

    # Run specific settings
    os.environ["JOB_ID"] = job_id
    os.environ["NUM_QUBITS"] = str(num_qubits)

    sbatch_src = os.path.join(
        os.environ["EXEC_PATH"], f"type_exec_{compute_name}.sbatch"
    )

    query_conn = connector.Connector(CONNECTOR_TYPE, QPU_IP_ADDRESS, QPU_PORT, LOCKFILE)

    computation_src = get_computation_src(compute_name).from_json()
    # Note: the qs_cfg dictionary is encoded to pass it unchanged as an env variable.
    computation_env_vars = {
        "qs_src": compute_name,
        "qs_cfg": computation_src.dump_cfg().encode("utf-8"),
    }

    result = subprocess.run(
        ["sbatch", sbatch_src],
        env={**os.environ, **computation_env_vars},
        check=False,
    )
    return result.returncode


def main():
    """Main wrapper"""
    execute(sys.argv[1], sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    main()
