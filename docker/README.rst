Using Docker
============
The following guide provides instructions on how to create a working Docker container for the
examples outlined in the MASSpy Publication. To simplify the reading of this guide, the following abbreviations
will be used to reference specific sections of the MASSpy publication manuscript:

1. **validation**: Validation as a modeling tool through enzyme regulation in MASS models
2. **ensemble-modeling**: Demonstration of features through ensemble sampling, assembly, and modeling
3. **case-study**: Case study: computing functional states of the *E. coli* proteome

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


Step 1: Build the MASSpy image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following build context is used::

    MASSpy                  # Source directory
    └── docker              # Root directory for build context
        ├── Dockerfile      # Dockerfile from VCS (https://github.com/SBRG/MASSpy/blob/v0.1.1/docker/Dockerfile)
        └── cplex           # Required to install CPLEX
            ├─ cplex_studio1210.linux-x86-64.bin
            └─ cplex.install.properties

All files required for the build context can be found in the
`MASSpy GitHub <https://github.com/SBRG/MASSpy/tree/v0.1.1/docker>`_, with the exception of the optimization installer file.

Once the CPLEX installer has been obtained, create an image called ``sbrg/masspy:0.1.1`` via the following::

    docker build \
        --build-arg python_version=3.7 \
        --build-arg mass_version=0.1.1 \
        -t sbrg/masspy:0.1.1 ./docker

After building the image, the next step is to **build the MASSpy-publication image**.

Step 2: Build the MASSpy-publication image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
After creating the MASSpy image ``sbrg/masspy:0.1.1 ``, the next step is to create the image 
``sbrg/masspy-publication`` for the MASSpy-publication. The following build context is used::

    MASSpy-publication          # Source directory (also root directory for build context)
        ├── Dockerfile          # https://github.com/SBRG/MASSpy/blob/v0.1.1/docker/Dockerfile
        ├── validation          # Directory for example
        ├── ensemble-modeling   # Directory for example
        └── case-study          # Directory for example

To create the ``sbrg/masspy-publication`` image with all examples included, use the following command::

    docker build -t sbrg/masspy-publication .

After building the image, the next step is to **build the container**.


Step 3: Build the container
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Once created, the MASSpy-publication image ``sbrg/masspy-publication`` is used to create the
container using the following::

    docker run -rm \
        --mount type=volume,src=licenses,dst=/home/masspy_user/opt/licenses \
        --publish 8888:8888 \
        -it sbrg/masspy-publication

Running the above command will create an interactive shell to use within the container.
To use the iPython notebooks inside the container, run ``jupyter notebook --ip=0.0.0.0 --port=8888``.

Wrap up
+++++++
To exit and remove the container, run ``exit`` using the interactive shell inside the container.


Additional information
----------------------
Some additional information about using the repository code with Docker is provided below.

Using Gurobi 
~~~~~~~~~~~~
The *Gurobi Optimizer* can be used instead of the CPLEX solver to produce similar results.
A floating license is required to use Gurobi in a Docker container. Consult the
`MASSpy documentation on optimization solvers <https://masspy.readthedocs.io/en/v0.1.1/installation/solvers.html>`_ for
more information.

Building the image for a specific example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
All examples from the repository are included in the Docker by default. However, the Docker container can be reduced in order to look at only one specific example.

* To only include  the **validation** example::

    docker build --target validation -t sbrg/masspy-publication:validation .

* To only include  the **ensemble-modeling** example::

    docker build --target ensemble-modeling -t sbrg/masspy-publication:ensemble-modeling .

* To only include the **case-study** example::

    docker build --target case-study -t sbrg/masspy-publication:case-study .
