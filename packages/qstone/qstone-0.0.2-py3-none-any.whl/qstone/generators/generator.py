"""
Generation of the testbench.
"""

import argparse
import os
import tarfile
from typing import List

import numpy
import pandas as pd
from jinja2 import Template

from qstone.utils.utils import (
    JOB_SCHEMA,
    USER_SCHEMA,
    QpuConfiguration,
    get_config_environ_vars,
    load_jobs,
    load_users,
)

SCHEDULERS = ["slurm/schedmd", "bare_metal", "lsf/jsrun"]
SCHEDULER_ARGS = {"walltime": "3", "nthreads": "1"}


def _get_value(job_cfg: pd.DataFrame, key: str, default: str):
    val = default
    try:
        val = job_cfg[key].values[0]
    except (KeyError, IndexError):
        pass
    if val is numpy.nan:
        val = default
    return str(val)


def _render_templates(sched: str, subs: dict, job_types: List[str], jobs_cfg: dict):
    # Find all the jinja files and apply
    rendered = []
    for filename in os.listdir(sched):
        if filename.endswith(".jinja"):
            fullpath = os.path.join(sched, filename)
            with open(fullpath, encoding="utf-8") as fid:
                source = fid.read()
            if "{app}" in filename:
                for t in job_types:
                    outfile = fullpath.replace(".jinja", "").replace("{app}", t)
                    for s in SCHEDULERS:
                        if s in sched:
                            sched_opt = f"{s}_opt"
                    j = jobs_cfg[jobs_cfg["type"] == t]
                    args = {}
                    for key, val in SCHEDULER_ARGS.items():
                        args[key] = _get_value(j, key, val)
                    extra_args = _get_value(j, sched_opt, "")
                    Template(source).stream(
                        {**subs, **args, **{"extra_args": extra_args}}
                    ).dump(outfile)
                    rendered.append(outfile)
            else:
                outfile = fullpath.replace(".jinja", "")
                Template(source).stream(subs).dump(outfile)
                rendered.append(outfile)
    return rendered


def _render_and_pack(
    sched: str, output_filename: str, subs: dict, job_types: List[str], jobs_cfg: dict
):
    """
    Renders and packs all the necessary files to run as a user
    """
    sched_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), sched)
    rendered_files = _render_templates(sched_path, subs, job_types, jobs_cfg)
    # Copy the required files.
    with tarfile.open(output_filename, "w:gz") as tar:
        # Adding necessary scripts excluding original templates
        tar.add(
            sched_path,
            arcname="qstone_suite",
            recursive=True,
            filter=lambda tarinfo: None if "jinja" in tarinfo.name else tarinfo,
        )
        for job_type in job_types:
            # Adding user defined apps
            job_cfg = jobs_cfg[jobs_cfg["type"] == job_type]
            app = _get_value(job_cfg, "path", "")
            print(f"{app}")
            if app:
                assert os.path.exists(app)
                tar.add(
                    app,
                    arcname=f"qstone_suite/{os.path.basename(app)}",
                    recursive=False,
                )
    # Clean up generated files
    for rendered_file in rendered_files:
        os.remove(rendered_file)


def _compute_job_pdf(usr_cfg: dict) -> List[float]:
    """Computes the normalized pdf to assign to different jobs based on user
    configurations and speciified qubit capacity
    """

    pdf = [prob for comp, prob in usr_cfg["computations"].items()]

    normalized = [float(p) / sum(pdf) for p in pdf]

    return normalized


def _generate_user_jobs(
    usr_cfg: dict, jobs_cfg: dict, job_pdf: List[float], num_calls: int
):
    """
    Generates the different user jobs provided given the configuration and the number of
    calls.
    """
    runner = 'python "$EXEC_PATH"/type_exec.py'
    job_types = numpy.random.choice(
        list(usr_cfg["computations"].keys()), p=job_pdf, size=(num_calls)
    )
    # Randomise number of qubits
    num_qubits = []
    for j in job_types:
        qubit_range = jobs_cfg[jobs_cfg["type"] == j]
        num_qubits.extend(
            numpy.random.randint(qubit_range["qubit_min"], qubit_range["qubit_max"])
        )

    # Assign job id and pack
    job_ids = list(range(len(job_types)))
    return (
        list(zip([f"{runner} {s}" for s in job_types], num_qubits, job_ids)),
        set(job_types),
    )


def _environment_variables_exports(env_vars: dict) -> List[str]:
    """
    Generates export statements for environment variables.
    """
    exports_list = [f'export {k.upper()}="{v}"' for k, v in env_vars.items()]

    return exports_list


def generate_suite(config: str, num_calls: int, output_folder: str) -> List[str]:
    """
    Generates the suites of jobs for the required users.

    Args:
        config: Input configuration for generate, defines QPU configuration and user jobs
        num_calls: Number of jobs to generate per user
        output_folder: Scheduler tar file output lcoaiton

    Returns list of output file paths
    """
    users_cfg = load_users(config, USER_SCHEMA)
    jobs_cfg = load_jobs(config, JOB_SCHEMA)
    env_vars = get_config_environ_vars(config)
    env_exports = _environment_variables_exports(env_vars)

    qpu_config = QpuConfiguration()
    qpu_config.load_configuration(get_config_environ_vars(config))

    # Generating list of jobs
    output_paths = []
    for prog_id, user_cfg in users_cfg.iterrows():
        pdf = _compute_job_pdf(user_cfg)
        jobs, job_types = _generate_user_jobs(
            user_cfg, jobs_cfg, pdf, int(user_cfg["weight"] * num_calls)
        )

        # generate substitutions for Jinja templates
        formatted_jobs = [" ".join(map(str, job)) for job in jobs]

        user_name = user_cfg["user"]
        usr_env_exports = [
            f'export PROG_ID="{prog_id}"',
            f'export QS_USER="{user_name}"',
        ]
        subs = {
            "exports": "\n".join(env_exports + usr_env_exports),
            "jobs": "\n".join(formatted_jobs),
            "project_name": env_vars["project_name"],
        }
        # Pack project files
        for sched in SCHEDULERS:
            filename = os.path.join(
                output_folder, f'{sched.replace("/","_")}_{user_name}.qstone.tar.gz'
            )
            # render and pack all the files
            _render_and_pack(sched, filename, subs, job_types, jobs_cfg)
            output_paths.append(filename)
    return output_paths


def main():
    """
    Runs the generator phase.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=str)
    parser.add_argument("num_calls", type=int)
    parser.add_argument("output_folder", type=str)
    args = parser.parse_args()
    generate_suite(args.config, args.num_calls, args.output_folder)


if __name__ == "__main__":
    main()
