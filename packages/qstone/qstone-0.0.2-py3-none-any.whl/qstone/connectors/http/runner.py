""" Quantum executor over a HTTP channel """

import json
import secrets

import requests
import waiting

from qstone.connectors import connection
from qstone.utils.utils import ComputationStep, QpuConfiguration, trace


class HttpConnection(connection.Connection):
    """Connection running jobs over Http"""

    def __init__(self):
        """Creates the empty response"""
        self.response = None

    @trace(
        computation_type="CONNECTION",
        computation_step=ComputationStep.PRE,
    )
    def preprocess(self, qasm_ptr: str) -> str:
        """Preprocess the data."""
        # Currently passthrough.
        with open(qasm_ptr, "r", encoding="utf-8") as fid:
            return fid.read()

    @trace(
        computation_type="CONNECTION",
        computation_step=ComputationStep.RUN,
    )
    def postprocess(self, message: str) -> str:
        """Postprocess the data"""
        # If the message is None we return an empty string
        return json.loads(message) if message else ""

    @trace(
        computation_type="CONNECTION",
        computation_step=ComputationStep.QUERY,
        label="_request_and_process",
    )
    def _request_and_process(
        self, qasm_ptr: str, reps: int, hostpath: str, lockfile: str
    ):
        pkt_id = secrets.randbelow(2**31)
        circuit = self.preprocess(qasm_ptr)
        payload = {"circuit": circuit, "pkt_id": pkt_id, "reps": reps}
        headers: dict = {}
        success = False
        self.response = None
        lock = connection.FileLock(lockfile)
        if lock.acquire_lock():
            r = requests.post(
                f"{hostpath}/execute", timeout=1, headers=headers, json=payload
            )
            success = r.status_code == 200
            if success:
                response = requests.get(f"{hostpath}/results", timeout=1)
                self.response = response.text
                success = r.status_code == 200
            lock.release_lock()
        return success

    # mypy: disable-error-code="attr-defined"
    @trace(
        computation_type="CONNECTION",
        computation_step=ComputationStep.POST,
    )
    def run(
        self, qasm_ptr: str, reps: int, host: str, server_port: int, lockfile: str
    ) -> dict:
        """Run the connection to the server"""
        hostpath = f"{host}:{server_port}" if server_port else host
        try:
            waiting.wait(
                lambda: self._request_and_process(qasm_ptr, reps, hostpath, lockfile),
                timeout_seconds=20,
            )
        except waiting.TimeoutExpired:
            pass
        return self.postprocess(self.response)

    @trace(
        computation_type="CONNECTION",
        computation_step=ComputationStep.QUERY,
    )
    def query_qpu_config(self, host: str, server_port: int) -> QpuConfiguration:
        """Query the Qpu configuraiton of the target"""
        hostpath = f"{host}"
        if server_port:
            hostpath += f":{server_port}"
        response = requests.get(f"{hostpath}/qpu/config", timeout=10)
        qpu_config = QpuConfiguration()
        if response.ok:
            qpu_config.load_configuration(json.loads(response.text))
        return qpu_config
