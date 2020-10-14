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


MASSpy Source Code
------------------
To utilize the code in this repository, MASSpy v0.1.1 is required. The source code for 
MASSpy v0.1.1 can be found `here <https://github.com/SBRG/MASSpy/tree/v0.1.1>`_. 

Building the Docker container or using the ``masspy-publication-env.yml`` environment file with Conda will ensure the correct version of MASSpy and
is installed as well as compatible versions of other dependencies.

For the latest distribution of MASSpy, check out the MASSpy `GitHub <https://github.com/SBRG/MASSpy>`_. 

Optimization solvers
--------------------
To run the **ensemble-modeling** and **case-study** code, a solver with quadratic programming capabilities is required.
See the `MASSpy documentation on optimization solvers <https://masspy.readthedocs.io/en/v0.1.1/installation/solvers.html>`_
for more information.

Running the MASSpy Publication Code
===================================
The recommended method to explore the code in this repository is to use a `Docker <https://docs.docker.com/>`_ container.
Instructions for running a Docker container are found in the `Docker README </docker/README.rst>`_

However, the environment file ``masspy-publication-env.yml`` has been provided in order to create a virtual environment using the
`Conda <https://docs.conda.io/projects/conda/en/latest/index.html>`_ package manager.


Using Docker
------------

Instructions for running a Docker container are found in the
README for `using Docker </docker/README.rst>`_ to run the examples for MASSpy Publication.


Using a Conda Python Environment
--------------------------------
To run the examples without Docker, it is recommended to install Conda, an open source package management system and environment management system.
Instructions to setup and install the environment are found in the README for `using a Conda Python Environment </conda-env/README.rst>`_

**Note:** The **ensemble-modeling** and **case-study** examples rely on MCMC sampling, which contains elements of random number generation (e.g., MCMC sampling).
Consequently, results may vary slightly when repeated in a conda environment depending on the dependency versions installed. 