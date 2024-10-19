""" Click based interface to expose all the subroutines in one single file """

import json
import os
from typing import Optional

import click

from qstone.apps import get_computation_src
from qstone.connectors import connector

QPU_IP_ADDRESS: str = os.environ.get("QPU_IP_ADDRESS", "127.0.0.1")
QPU_PORT: int = int(os.environ.get("QPU_PORT", "0"))
CONNECTOR_TYPE = connector.ConnectorType[os.environ.get("CONNECTOR", "NO_LINK")]
LOCKFILE: Optional[str] = (
    "qstone.lock" if os.environ["QPU_MANAGEMENT"] == "LOCK" else None
)
OUTPUT_PATH = os.environ["OUTPUT_PATH"]
JOB_ID: int = int(os.environ.get("JOB_ID", "0"))
NUM_QUBITS: int = int(os.environ.get("NUM_QUBITS", "0"))


@click.group()
def cli():
    """Groups all the other commands"""


@cli.command()
@click.option("--src", help="Computation src file.")
@click.option("--cfg", help="Computation cfg json.")
def pre(src: str, cfg: str):
    """Run pre step of computation."""
    click.echo(f"pre type {src}")
    computation_src = get_computation_src(src)(json.loads(cfg))
    computation_src.pre(OUTPUT_PATH)


@cli.command()
@click.option("--src", help="Computation src file.")
@click.option("--cfg", help="Computation cfg json.")
def run(src: str, cfg: str):
    """Run QPU run step of computation."""
    click.echo(f"run type {src}")
    computation_src = get_computation_src(src)(json.loads(cfg))
    computation_src.run(
        OUTPUT_PATH,
        connector.Connector(CONNECTOR_TYPE, QPU_IP_ADDRESS, int(QPU_PORT), LOCKFILE),
    )


@cli.command()
@click.option("--src", help="Computation src file.")
@click.option("--cfg", help="Computation cfg json.")
def post(src: str, cfg: str):
    """Run post step of computation"""
    click.echo(f"post type {src}")
    computation_src = get_computation_src(src)(json.loads(cfg))
    computation_src.post(OUTPUT_PATH)


if __name__ == "__main__":

    cli()
