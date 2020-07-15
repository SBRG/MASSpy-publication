# MASSpy-publication
This repository contains all scripts, notebooks, and data needed to reproduce case studies in MASSpy publication.


## Python Environment
To reproduce the case studies, it is highly recommended to install Conda, an open source package management system and environment management system. Instructions for installation can be found in the [Conda Documentation](https://docs.conda.io/en/latest/miniconda.html)

Using conda, the environment file `masspy-publication-env.yml` can be used to create the environment with the necessary pacakges to run the case studies. After downloading the source code, use the terminal or an Anaconda Prompt to run the following:

    conda env create -f masspy-publication-env.yml

in the `MASSpy-publication` source directory. Additional conda instructions for creating an environment from an environmment file are found [here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file).

### Quadratic programming solvers. 

To run the case studies, a solver with quadratic programming capabilities is required. Both the Gurobi and the CPLEX solvers are available under academic licenses.


Instructions for obtaining licenses:
* [Gurobi license](https://www.gurobi.com/academia/academic-program-and-licenses/)
* [CPLEX license](https://www.ibm.com/academic/home)

Both Gurobi and CPLEX solvers are included in the `masspy-publication-env.yml`. For additional installation instructions:
* [Gurobi installation](https://www.gurobi.com/documentation/9.0/quickstart_mac/ins_the_anaconda_python_di.html)
* [CPLEX installation](https://developer.ibm.com/docloud/blog/2017/01/23/cplex-python-now-available-anaconda-cloud/)

### Running Case Studies

Case studies are organized into seperate directories, each containing relevant Jupyter (iPython) notebook files for performing the case study. To view the notebooks, use the terminal or an Anaconda Prompt to run the following:

    jupyter notebook

in the `MASSpy-publication` source directory. Additional information about scripts and files can be found in the README file of the case study.

**Note:** Case studies 2 and 3 rely on MCMC sampling, which contains elements of random number generation (e.g., MCMC sampling). Consequently, case study results may vary slightly when repeated. 

## License
The MASSpy source and case study code is released under both the GPL and LGPL licenses. You may choose which license you choose to use the software under. However, please note that binary packages which include GLPK (such as the binary wheels distributed at https://pypi.python.org/pypi/cobra) and libRoadRunner will be bound by their licenses as well.

