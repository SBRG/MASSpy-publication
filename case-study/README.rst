Guide for example: case-study
====================================

The corresponding section of the MASSpy manuscript:

Case study: computing functional states of the {\it E. coli} proteome
----------------------------------------------------------------------
Case study to illustrate how MASSpy is utilized to gain insight into distribution of catalytic activities
of enzymes for the different metabolic states of a network. 

.. note::
    * This example will utilize the IBM CPLEX Optimizer. The Gurobi Optimizer can be utilized as an alternative option;
      but the use of a different optimization solver may result in small deviations.
    * This example utilizes MCMC sampling, which involves a seeding random number generation process in **NumPy**
      currently through the ``numpy.random.seed`` method. All seeds utilized in this notebook are set at ``seed=int(1234)``.


Build a Docker image
~~~~~~~~~~~~~~~~~~~~
After completing `Step 1: Build the MASSpy image </docker/README.rst#step-1-build-the-masspy-image>`_, 
use the commands to build and run a Docker container for only the **case-study** example::

    # Use the GitHub Repository as the image build context
    docker build --target validation -t sbrg/masspy-publication:case-study . && \
    docker run --rm \
        --mount type=volume,src=mass_project,dst=/home/masspy_user/mass_project/ \
        --mount type=volume,src=licenses,dst=/home/masspy_user/opt/licenses \
        --publish 8888:8888
        -it sbrg/masspy-publication:case-study

and run ``jupyter notebook --ip=0.0.0.0 --port=8888`` in the shell to get started!


Algorithms and settings utilized
-------------------------------
* NumPy pseudo random number generation: 
  - Algorithm: `Mersenne Twister <https://numpy.org/doc/stable/reference/random/bit_generators/mt19937.html#numpy.random.MT19937>`_.
  - All seeds utilized are set at ``seed=int(1234)``.

* Optimization for concentration sampling
  - Performed using CPLEX optimizer 12.10
  
* Integrator
  - Algorithm: ``CVODE``
  - Simulations always start at ``t=0``.
  - Default integrator settings for all simulations using ``Simulation.simulate``
    or ``Simulation.find_steady_state(strategy="simulate")`` unless explicitly indicated in notebook::

      < roadrunner.Integrator() >
      name: cvode
      settings:
          relative_tolerance: 0.000001
          absolute_tolerance: 0.000000000001
                      stiff: true
          maximum_bdf_order: 5
        maximum_adams_order: 12
          maximum_num_steps: 20000
          maximum_time_step: 0
          minimum_time_step: 0
          initial_time_step: 0
              multiple_steps: false
          variable_step_size: true
    Simulation times and alterations to these settings are defined at the time of simulation and 
    provided in corresponding sections of the notebooks.
