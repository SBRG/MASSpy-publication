Guide for example: validation
=============================

The corresponding section of the MASSpy manuscript:

Validation as a modeling tool through enzyme regulation in MASS models
----------------------------------------------------------------------
Validation of MASSpy as a modeling tool by describing mechanisms of enzyme regulation using enzymes modules as seen in:

  Yurkovich JT, Alcantar MA, Haiman ZB, Palsson BO (2018)
  Network-level allosteric effects are elucidated by detailing how ligand-binding events modulate utilization of catalytic potentials.
  PLOS Computational Biology 14(8): e1006356. https://doi.org/10.1371/journal.pcbi.1006356


Build a Docker image
~~~~~~~~~~~~~~~~~~~~
After completing `Step 1: Build the MASSpy image </docker/README.rst#step-1-build-the-masspy-image>`_, 
use the commands to build and run a Docker container for only the **validation** example::

    # Use the GitHub Repository as the image build context
    docker build --target validation -t sbrg/masspy-publication:validation . && \
    docker run --rm \
        --mount type=volume,src=mass_project,dst=/home/masspy_user/mass_project/ \
        --publish 8888:8888 \
        -it sbrg/masspy-publication:validation

and run ``jupyter notebook --ip=0.0.0.0 --port=8888`` in the shell to get started!

Algorithms and settings utilized
-------------------------------
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