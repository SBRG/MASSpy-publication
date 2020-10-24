Guide for example: ensemble-modeling
====================================

The corresponding section of the MASSpy manuscript:

Demonstration of features through ensemble sampling, assembly, and modeling
---------------------------------------------------------------------------
Demonstration of unique MASSpy capabilities using an example workflow using MCMC sampling to parameterize and assemble an ensemble of stable dynamic metabolic models.

.. note::
    * This example will utilize the IBM CPLEX Optimizer. The Gurobi Optimizer can be utilized as an alternative option;
      but the use of a different optimization solver may result in small deviations.
    * This example utilizes MCMC sampling, which involves a seeding random number generation process in **NumPy**
      currently through the ``numpy.random.seed`` method.

Build a Docker image
~~~~~~~~~~~~~~~~~~~~
After completing `Step 1: Build the MASSpy image </docker/README.rst#step-1-build-the-masspy-image>`_, 
use the commands to build and run a Docker container for only the **ensemble-modeling** example::

    # Use the GitHub Repository as the image build context
    docker build --target validation -t sbrg/masspy-publication:ensemble-modeling . && \
    docker run --rm \
        --mount type=volume,src=mass_project,dst=/home/masspy_user/mass_project/ \
        --mount type=volume,src=licenses,dst=/home/masspy_user/opt/licenses \
        --publish 8888:8888
        -it sbrg/masspy-publication:ensemble-modeling

and run ``jupyter notebook --ip=0.0.0.0 --port=8888`` in the shell to get started!

Algorithms and settings utilized
-------------------------------
* NumPy pseudo random number generation: 
  - Algorithm: `Mersenne Twister <https://numpy.org/doc/stable/reference/random/bit_generators/mt19937.html#numpy.random.MT19937>`_.
  - All seeds utilized are set at ``seed=int(1)``.

* Optimization for concentration sampling
  - Performed using CPLEX optimizer 12.10

* Optimization for enzyme module rate constant parameters 
  - Performed using ``scipy.optimize.minimize`` with the ``trust-constr`` for nonlinear convex optimizationmethod.
  - Additional settings: ``{"gtol": 1e-12, "xtol": 1e-12, "maxiter": 1e4}``
  
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
    Alterations to these settings are defined at the time of simulation.
