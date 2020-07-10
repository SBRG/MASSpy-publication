# MASSpy-publication
This repository contains all scripts, notebooks, and data needed to reproduce case studies in MASSpy publication.


## Python Environment
To reproduce the case studies, it is highly recommended to install Conda, an open source package management system and environment management system. Instructions for installation can be found in the [Conda Documentation](https://docs.conda.io/en/latest/miniconda.html)

Using conda, the environment file `masspy-publication-env.yml` can be used to create the environment with the necessary pacakges to run the case studies. After downloading the source code, use the terminal or an Anaconda Prompt to run the following:

    conda env create -f masspy-publication-env.yml

in the `MASSpy-publication` source directory. Additional conda instructions for creating an environment from an environmment file are found [here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file)

### Quadratic programming solvers. 

To run the case studies, a solver with quadratic programming capabilities is required. Both the Gurobi and the CPLEX solvers are available under academic licenses and packages.

For installation instructions:
* [Gurobi installation](https://www.gurobi.com/documentation/9.0/quickstart_mac/ins_the_anaconda_python_di.html)
* [CPLEX installation](

Instructions for obtaining licenses:
* [Gurobi license](https://www.gurobi.com/academia/academic-program-and-licenses/)
* [CPLEX license](https://www.gurobi.com/academia/academic-program-and-licenses/)
## Running Case Studies
