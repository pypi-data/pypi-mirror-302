""" Wrapper to run type loads """

import os
import subprocess
import sys
from typing import Optional

from qstone.apps import get_computation_src
from qstone.connectors import connector
from qstone.utils.utils import JobReturnCode

QPU_PORT: int = int(os.environ.get("QPU_PORT", "0"))
QPU_IP_ADDRESS: str = os.environ.get("QPU_IP_ADDRESS", "127.0.0.1")
CONNECTOR_TYPE = connector.ConnectorType[os.environ.get("CONNECTOR", "NO_LINK")]
LOCKFILE: Optional[str] = (
    "qstone.lock" if os.environ.get("QPU_MANAGEMENT") == "LOCK" else None
)


def execute(compute_name: str, num_qubits: int, job_id: str):
    """Execute the computation steps via separate  calls

    Args:
        compute_name: Name of the computation in the registry
        job_id : id of the job to run
        num_qubits: the number of qubits to use in this run

    Returns the return code of query and step subprocess execution
    """

    # Run specific settings
    os.environ["JOB_ID"] = str(job_id)
    os.environ["NUM_QUBITS"] = str(num_qubits)

    jobs_cli = os.path.join(os.environ["EXEC_PATH"], "jobs.py")

    query_conn = connector.Connector(CONNECTOR_TYPE, QPU_IP_ADDRESS, QPU_PORT, LOCKFILE)

    computation_src = get_computation_src(compute_name).from_json()

    type_return_code = JobReturnCode.JOB_COMPLETED

    result = subprocess.run(
        [
            "python",
            jobs_cli,
            "pre",
            "--src",
            compute_name,
            "--cfg",
            computation_src.dump_cfg(),
        ],
        check=False,
    )
    if result.returncode == 0:
        result = subprocess.run(
            [
                "python",
                jobs_cli,
                "run",
                "--src",
                compute_name,
                "--cfg",
                computation_src.dump_cfg(),
            ],
            check=False,
        )
    else:
        return JobReturnCode.PRE_STEP_INCOMPLETE

    if result.returncode == 0:
        result = subprocess.run(
            [
                "python",
                jobs_cli,
                "post",
                "--src",
                compute_name,
                "--cfg",
                computation_src.dump_cfg(),
            ],
            check=False,
        )
    else:
        return JobReturnCode.RUN_STEP_INCOMPLETE

    if result.returncode != 0:
        type_return_code = JobReturnCode.POST_STEP_INCOMPLETE

    return type_return_code


def main():
    """Main wrapper"""
    execute(sys.argv[1], sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    main()
