MASSpy Publication
==================
This repository contains all scripts, notebooks, and data needed to reproduce case studies in MASSpy publication.
To simplify the reading of this guide, the following abbreviations will be used to reference specific sections of the
MASSpy publication manuscript:

1. **validation**: Validation as a modeling tool through enzyme regulation in MASS models
2. **ensemble-modeling**: Demonstration of features through ensemble sampling, assembly, and modeling
3. **case-study**: Case study: computing functional states of the *E. coli* proteome

The recommended method to explore the code in this repository is to use a `Docker <https://docs.docker.com/>`_ container.
Instructions for running a Docker container are found in the `Docker README </docker/README.rst>`_

However, the environment file ``masspy-publication-env.yml`` has been provided in order to create a virtual environment using the
`Conda <https://docs.conda.io/projects/conda/en/latest/index.html>`_ package manager.

To utilize the code in this repository, MASSpy v0.1.1 is required. The source code for 
MASSpy v0.1.1 can be found `here <https://github.com/SBRG/MASSpy/tree/v0.1.1>`_. 

Building the Docker container or using the ``masspy-publication-env.yml`` environment file with Conda will ensure the correct version of MASSpy and
is installed as well as compatible versions of other dependencies.

MASSpy Source Code
------------------
For the latest distribution of MASSpy, check out the MASSpy `GitHub <https://github.com/SBRG/MASSpy>`_. 

Optimization solvers
--------------------
To run the **ensemble-modeling** and **case-study** code, a solver with quadratic programming capabilities is required.
See the `MASSpy documentation on optimization solvers <https://masspy.readthedocs.io/en/v0.1.1/installation/solvers.html>`_
for more information.

Using Docker
------------

Instructions for running a Docker container are found in the
README for `Using Docker </docker/README.rst>`_ for the MASSpy-publication.


Using a Conda Python Environment
--------------------------------
To reproduce the case studies without Docker, it is recommended to install Conda, an open source package management system and environment management system.
Instructions for installation can be found in the `Conda Documentation <https://docs.conda.io/en/latest/miniconda.html>`_

Using conda, the environment file `masspy-publication-env.yml` can be used to create the environment with the required dependencies.
After downloading the source code, use the terminal or an Anaconda Prompt to run the following::

    conda env create -f masspy-publication-env.yml

in the `MASSpy-publication` source directory. Additional conda instructions for creating an environment from an environmment file are found
`here <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file>`_.

To run the examples, MASSpy version 0.1.1 is required. The correct version of MASSpy will be installed with the conda environment file. To run the notebooks,
clone the repository and use a shell or an Anaconda Prompt to run the following::

    jupyter notebook

in the `MASSpy-publication` source directory. Additional information about scripts and files can be found in the README file of the case study.

**Note:** The **ensemble-modeling** and **case-study** examples rely on MCMC sampling, which contains elements of random number generation (e.g., MCMC sampling).
Consequently, results may vary slightly when repeated in a conda environment depending on the dependency versions installed. 