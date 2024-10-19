# QStone

<img width="197" alt="image" src="https://github.com/riverlane/QStone/assets/62563515/85bd4300-df21-40a8-90ef-5bd9b7d28598">

## What

An utility to benchmark the quality of an HPC and Quantum Computers integration. The benchmark allows the definition of a set of users for which a set of configurable quantum applications will be randomly selected. Example of currently supported quantum applications: VQE, PyMatching, RB. Users can create custom applications and use them together with the core applications.
QStone generates different portable files (.tar.gz), each supporting a different user and a different scheduler (currently supporting: slurm, lsf, bare_metal). During execution of the benchmark, QStone gathers information on each steps of the applications, allowing investigations on bottlenecks and/or resource constraints at the interface between Quantum and HPC.

## Why

Building an appropriate hardware/software infrastructure to support HPCQC requires
loads of work. We believe we shoud use a data driven approach in which we measure, fix, measure again with every new version of Quantum Computers, software and HPC hardware.

## Where

Currently supported platforms/architectures:

- MacOS: M1/M2 (Sequoia)
- Intel: x86 (Ubuntu)
- PowerPC: Power9 ()

Tested on Python 3.8, 3.10, 3.12

## How

### Installation (local)

We don't currently have a Pypi package, so you will need to install from the repository:
`pip install https://github.com/riverlane/QStone.git` or
`pip install ./QStone` or

Expect a python package soon!

For installation on [Summit](https://www.olcf.ornl.gov/summit/) - please refer to the guide [summit installation](summit.md)

### Execution

Run QStone using Command Line Interface

- Run the **generator** command

    ```qstone generate -i conf.json```

    Generates tar.gz files that contains all the scripts to run scheduler for each user. Currently supported schedulers: [baremetal, altair/fnc, slurm/schedmd]. QStone expects an input configuration describing the users to want to generate jobs for as well as the description of the quantum computer you are generating jobs for.

    With `config.json`:

```json
{
  "project_name": "proj_name",
  "connector": "NO_LINK",
  "qpu_ip_address": "0.0.0.0",
  "qpu_port": "55",
  "qpu_management": "LOCK",
  "jobs": [
    {
      "type": "VQE",
      "qubit_min": 2,
      "qubit_max": 4,
      "walltime" : 10,
      "nthreads" : 4,
      "lsf/jsrun_opt": "-nnodes=4 "
    },
    {
      "type": "RB",
      "qubit_min": 2,
      "qubit_max": 4,
      "walltime" : 10,
      "nthreads" : 2,
      "slurm/schedmd_opt": "--cpus-per-task=4"
    }
  ],
  "users": [
    {
      "user": "user0",
      "weight": 1,
      "computations": {
        "VQE": 0.05,
        "RB": 0.94,
        "PyMatching": 0.01
      }
    }
  ]
}
```

For more information on the `config.json` format refer to [config](config_json.md).

- Alternatively call the generator in script:

```python
from qstone.generators import generator

def main():
    generator.generate_suite(config="config.json",
        num_calls=100,output_folder=".")

if __name__ == "__main__":
     main()
```


-  Run the **run** command to execute chosen scheduler

    ```qstone run -i scheduler.qstone.tar.gz```


- Alternatively may untar on your machine of choice and run as the selected user.

    - Run the jobs by executing `sh qstone_suite/qstone.sh`

    - Run the profiling tool to extract metrics of interest. 

-  Run the **profile** command providing the initial input configuration and output folder to run profiling tool on run information

    ```qstone profile --cfg conf.json --folder qstone_profile```

### Supported network topologies

- Local no-link runner
- gRPC
- Http

### Examples

- Getting started [notebook](examples/running/getting_started.ipynb)
- How to add a [new type of computation](examples/adding/computation/README.md)
- How to create a simple [gateway](examples/node/README.md)

### Contributing

Guidance on how to [contribute](Contribute.md)


