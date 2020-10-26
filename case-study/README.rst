Guide for example: case-study
=============================

* All files and instructions are available in the `MASSpy-publication GitHub Repository <https://github.com/SBRG/MASSpy-publication>`_.
* It is highly recommended to clone the repository and build a ``Docker`` container to follow along with this example.

The corresponding section of the MASSpy manuscript:

Case study: computing functional states of the {\it E. coli} proteome
----------------------------------------------------------------------
Case study to illustrate how MASSpy is utilized to gain insight into distribution of catalytic activities
of enzymes for the different metabolic states of a network. 

.. note::
    * This example will utilize the IBM CPLEX Optimizer. The Gurobi Optimizer can be utilized as an alternative option;
      but the use of a different optimization solver may result in small deviations.
    * This example utilizes MCMC sampling, which involves a seeding random number generation process in **NumPy**
      currently through the ``numpy.random.seed`` method.


Build a Docker image
~~~~~~~~~~~~~~~~~~~~
After completing `Step 1: Build the MASSpy image <https://github.com/SBRG/MASSpy-publication/blob/master/docker/README.rst>`_, 
use the commands to build and run a Docker container for only the **case-study** example::

    # Using the MASSpy-publication GitHub Repository as the image build context
    docker build --target case-study -t sbrg/masspy-publication:case-study ./docker && \
    docker run --rm \
        --mount type=volume,src=mass_project,dst=/home/masspy_user/mass_project/ \
        --mount type=volume,src=licenses,dst=/home/masspy_user/opt/licenses \
        --publish 8887:8887 \
        -it sbrg/masspy-publication:case-study

and run ``jupyter notebook --ip=0.0.0.0 --port=8887`` in the shell to get started!


Algorithms and settings utilized
-------------------------------
* NumPy pseudo random number generation: 

  - Algorithm: `Mersenne Twister <https://numpy.org/doc/stable/reference/random/bit_generators/mt19937.html#numpy.random.MT19937>`_.
  - All seeds utilized are set at ``seed=int(4)``.

* Optimization for concentration sampling

  - Performed using CPLEX optimizer 12.10
  
* Integrator

  - Algorithm: ``CVODE``
  - Simulations always start at ``t=0``.
  - Default integrator settings for all simulations using ``Simulation.simulate``
    or ``Simulation.find_steady_state(strategy="simulate")`` unless explicitly changed in notebook::

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

Directory and File Descriptions
-------------------------------

- **model_construction_notebooks**: Contains scripts to construct ensembles of *E. coli* glycolysis models, seperated by growth condition.

  - **model_construction_glucose_media_99-01_isozyme_split.ipynb**: Construction notebook for glucose growth conditions, with 99% of flux assigned to the first isozyme and 1% of flux assigned to the second isozyme.
  - **model_construction_glucose_media_75-25_isozyme_split.ipynb**: Construction notebook for glucose growth conditions, with 75% of flux assigned to the first isozyme and 25% of flux assigned to the second isozyme.
  - **model_construction_glucose_media_50-50_isozyme_split.ipynb**: Construction notebook for glucose growth conditions, with 50% of flux assigned to the first isozyme and 50% of flux assigned to the second isozyme.
  - **model_construction_glucose_media_25-75_isozyme_split.ipynb**: Construction notebook for glucose growth conditions, with 25% of flux assigned to the first isozyme and 75% of flux assigned to the second isozyme.
  - **model_construction_glucose_media_01-99_isozyme_split.ipynb**: Construction notebook for glucose growth conditions, with 1% of flux assigned to the first isozyme and 99% of flux assigned to the second isozyme.
  - **model_construction_pyruvate_media_99-01_isozyme_split.ipynb**: Construction notebook for pyruvate growth conditions, with 99% of flux assigned to the first isozyme and 1% of flux assigned to the second isozyme.
  - **model_construction_pyruvate_media_75-25_isozyme_split.ipynb**: Construction notebook for pyruvate growth conditions, with 75% of flux assigned to the first isozyme and 25% of flux assigned to the second isozyme.
  - **model_construction_pyruvate_media_50-50_isozyme_split.ipynb**: Construction notebook for pyruvate growth conditions, with 50% of flux assigned to the first isozyme and 50% of flux assigned to the second isozyme.
  - **model_construction_pyruvate_media_25-75_isozyme_split.ipynb**: Construction notebook for pyruvate growth conditions, with 25% of flux assigned to the first isozyme and 75% of flux assigned to the second isozyme.
  - **model_construction_pyruvate_media_01-99_isozyme_split.ipynb**: Construction notebook for pyruvate growth conditions, with 1% of flux assigned to the first isozyme and 99% of flux assigned to the second isozyme.
  - **construction_functions.py**: A python script containing various functions used in constructing the *E. coli* glycolysis models and all associated enzyme modules.
  - **table_export.py**: Export functions for tables of model values and ODEs.

- **model_analysis_notebooks**:  Contains scripts to analyze ensembles of *E. coli* glycolysis models.

  - **analysis_functions.py**: A python script containing various functions used in analyzing the ensembles of *E. coli* glycolysis models.
  - **analysis_on_gibbs_free_energy_and_enzyme_abundances_for_growth_conditions.ipynb**: Analysis of the Gibbs free energy for reactions and the fractional abundances of enzyme forms, with emphasis on the differences between glucose and pyruvate growth conditions. Used for generating Figure 4 and S2 Figure in MASSpy publication.
  - **analysis_on_gibbs_free_energy_and_enzyme_abundances_for_isozyme_flux_split_sensitivity.ipynb**: Analysis of the Gibbs free energy for reactions and the fractional abundances of enzyme forms, with emphasis on the sensitivity of the flux split between isozyme pairs. Used for generating S1 Figure in MASSpy publication.

- **data**:

  - **analysis_figures**: Contains PDFs of individually generated plots, used as panels for publication figures.
  - **enzyme_module_data**: Contains all data necessary for constructing individual enzyme modules. Data obtained and exported from `MASSef <https://github.com/opencobra/MASSef>`__ package.
  - **models_isozyme_split_99_1**: Contains models genereated for both growth conditions with 99% of flux assigned to the first isozyme and 1% of flux assigned to the second isozyme during construction. Models are available in both JSON and SBML formats.
  - **models_isozyme_split_75_25**: Contains models genereated for both growth conditions with 75% of flux assigned to the first isozyme and 25% of flux assigned to the second isozyme during construction. Models are available in both JSON and SBML formats.
  - **models_isozyme_split_50_50**: Contains models genereated for both growth conditions with 50% of flux assigned to the first isozyme and 50% of flux assigned to the second isozyme during construction. Models are available in both JSON and SBML formats.
  - **models_isozyme_split_25_75**: Contains models genereated for both growth conditions with 25% of flux assigned to the first isozyme and 75% of flux assigned to the second isozyme during construction. Models are available in both JSON and SBML formats.
  - **models_isozyme_split_1_99**: Contains models genereated for both growth conditions with 1% of flux assigned to the first isozyme and 99% of flux assigned to the second isozyme during construction. Models are available in both JSON and SBML formats.
  - **ecoli_cobra**: Contains the reconstruction of *E. coli* iML1515 as both JSON and SBML files.
  - **iML1515_Glycolysis_map.json**: An Escher map of the glycolytic subnetwork for *E. coli* iML1515 as a JSON file.  
  - **model_creation_data.xlsx**: An excel sheet containing additional data necessary for contructing the kinetic model of *E. coli* glycolysis. Data includes flux and concentration growth data, equilibrium constants, values necessary for converting from grams of cellular dry weight (gDW) to liters (L). 
  **tables**: Contains value tables in CSV format for all models utilized in each notebook. Also contains CSV files for sheets in **model_creation_data.xlsx**.

- **execute_notebooks.sh**: Shell script to execute notebooks in order and inplace.

