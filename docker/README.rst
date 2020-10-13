Using Docker
============
The following guide provides instructions on how to create a working Docker container for the
examples outlined in the MASSpy Publication. To simplify the reading of this guide:

    1. **validation**: Validation of MASSpy simulations
    2. **ensemble-modeling**: Demonstration of ensemble modeling features
    3. **case-study**: Case Study: Computing Functional States of Ecoli Proteome

In order to run the **ensemble-modeling** and **case study** examples, an optimization solver is required.
It can be one of the following:

    * *ILOG CPLEX Optimization Studio 12.10*
    * *Gurobi Optimizer 9.0.3*

See the `MASSpy documentation on optimization solvers <https://masspy.readthedocs.io/en/v0.1.1/installation/solvers.html>`_
for more information on obtaining a license and the solver.

Running the publication code
----------------------------
In order to replicate identical publication results, the image must be built with the
*ILOG CPLEX Optimization Studio 12.10* (CPLEX). Therefore, this guide will assume the use of CPLEX.

Building the MASSpy image
~~~~~~~~~~~~~~~~~~~~~~~~~
The following build context is used::

    MASSpy                  # Source directory
    └── docker              # Root directory for build context
        ├── Dockerfile      # Dockerfile from VCS (https://github.com/SBRG/MASSpy/blob/v0.1.1/docker/Dockerfile)
        └── cplex           # Required to install CPLEX
            ├── cplex_studio1210.linux-x86-64.bin
            └── cplex.install.properties

Once the CPLEX installer has been obtained, create an image for MASSpy (v0.1.1)  using the following::

    docker build \
        --build-arg python_version=3.7 \
        --build-arg mass_version=0.1.1 \
        -t sbrg/masspy:0.1.1 ./docker

Building the MASSpy-publication image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
After the MASSpy image has been created, the next step is to create the image for the MASSpy-publication.
The following build context is used::

    MASSpy-publication          # Source directory (also root directory for build context)
        ├── Dockerfile          # https://github.com/SBRG/MASSpy/blob/v0.1.1/docker/Dockerfile
        ├── validation          # Directory for example
        ├── ensemble-modeling   # Directory for example
        └── case-study          # Directory for example


Building the image for a specific example
+++++++++++++++++++++++++++++++++++++++++
By default, all examples from the repository are included in the Docker. This is equivalent to the following
build command::
    
    docker build \
        --target all \
        -t sbrg/masspy-publication:all .

However, the Docker container can be reduced in order to look at only one specific example.
To build an image for a specific example...

**validation**::

    docker build \
        --target validation \
        -t sbrg/masspy-publication:validation .

**ensemble-modeling**::

    docker build \
        --target ensemble-modeling \
        -t sbrg/masspy-publication:ensemble-modeling .

**case-study**::

    docker build \
        --target case-study \
        -t sbrg/masspy-publication:case-study .

Using Gurobi 
~~~~~~~~~~~~
The *Gurobi Optimizer* can be used instead of the CPLEX solver to produce similar results.
A floating license is required to use Gurobi in a Docker container. Consult the
`MASSpy documentation on optimization solvers <https://masspy.readthedocs.io/en/v0.1.1/installation/solvers.html>`_ for
more information.