"""Main file for qstone."""

import argparse
import logging
import os
import subprocess
from typing import Optional, Sequence

from qstone.generators import generator
from qstone.profiling import profile


def generate(args: Optional[Sequence[str]] = None) -> None:
    """Qstone cli subcommand for generator."""
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger.info("Generating benchmark tarballs")

    generated_files = generator.generate_suite(
        config=args.src,  # type: ignore[union-attr]
        num_calls=int(args.calls),  # type: ignore[union-attr]
        output_folder=args.dst,  # type: ignore[union-attr]
    )

    logger.info("Generated %s tar balls:", len(generated_files))
    logger.info("\n".join(generated_files))


def run(args: Optional[Sequence[str]] = None) -> None:
    """Qstone cli subcommand for executing scheduler."""
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger.info("Extracting scheduler tar file")

    result = subprocess.run(["tar", "-xvf", args.src], check=False)  # type: ignore[union-attr]
    logger.info("Running scheduler")

    result = subprocess.run(
        ["sh", os.path.join("qstone_suite", "qstone.sh")], check=False
    )
    logger.info("Scheduler ran with status %s", result.returncode)


def prof(args: Optional[Sequence[str]] = None) -> None:
    """Qstone cli subcommand for profiling scheduler exection."""
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger.info("Extracting scheduler tar file")
    profile.profile(args.cfg, args.folder, args.pickle)  # type: ignore[union-attr]


def main(arg_strings: Optional[Sequence[str]] = None) -> None:
    """Qstone main entry point function.

    Args:
        arg_strings: Optionally manually provide argument strings (only used in tests).
    """
    parser = argparse.ArgumentParser(prog="qstone")

    subparsers = parser.add_subparsers(required=True)

    gen_cmd = subparsers.add_parser("generate", help="Generates job scheduler")

    gen_cmd.add_argument(
        "-i",
        "--src",
        help="Path to the input configuration",
        required=True,
        type=str,
    )

    gen_cmd.add_argument(
        "-o",
        "--dst",
        help="Path to the folder where the schedulers will be generated ",
        default=".",
        required=False,
        type=str,
    )

    gen_cmd.add_argument(
        "-n",
        "--calls",
        help="Number of jobs to generate",
        default=100,
        required=False,
        type=str,
    )

    gen_cmd.set_defaults(func=generate)

    runner = subparsers.add_parser("run", help="Run scheduler")

    runner.add_argument(
        "-i",
        "--src",
        help="Path to scheduler tar file",
        required=True,
        type=str,
    )
    runner.add_argument(
        "-o",
        "--dst",
        help="Path to extract scheduler to ",
        required=False,
        type=str,
    )

    runner.set_defaults(func=run)

    profiler = subparsers.add_parser("profile", help="Profile job execution")

    profiler.add_argument(
        "--cfg", type=str, help="Configuration file used to generate the load"
    )
    profiler.add_argument("--folder", type=str, help="Folder that contains the runs")
    profiler.add_argument(
        "--pickle",
        type=str,
        help="Optional Pickle filepath to store pickled dataframe",
        default="./QS_Profile.pkl",
    )

    profiler.set_defaults(func=prof)

    args = parser.parse_args(arg_strings)
    args.func(args)


if __name__ == "__main__":
    main()
