
Using a Conda Python Environment
=================================
The following guide provides instructions on how to create a virtual environment to run the examples.
It is recommended to install Conda, an open source package management system and environment management system.
Instructions for installation can be found in the `Conda Documentation <https://docs.conda.io/en/latest/miniconda.html>`_

Using conda, the environment file `masspy-publication-env.yml` can be used to create the environment with the required dependencies.
After downloading the source code, use the terminal or an Anaconda Prompt to run the following::

    conda env create -f masspy-publication-env.yml

in the `MASSpy-publication` source directory. Additional conda instructions for creating an environment from an environmment file are found
`here <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file>`_.

Running the publication code
----------------------------

To run the examples, MASSpy version 0.1.1 is required. The correct version of MASSpy will be installed with the conda environment file. To run the notebooks,
clone the repository and use a shell or an Anaconda Prompt to run the following::

    jupyter notebook

in the `MASSpy-publication` source directory. Additional information about scripts and files can be found in the README file of the case study.