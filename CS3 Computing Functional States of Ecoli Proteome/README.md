# Case Study 3: Computing Functional States of *E. coli* Proteome
Integration of COBRA and MASS modeling methodologies to create kinetic models of *E. coli* glycolysis from a metabolic reconstruction, providing insight into functional states of the proteome and activities of different isozymes. 

## Directory and file descriptions:
* **model_construction_notebooks**: Contains notebooks to construct ensembles of *E. coli* glycolysis models, seperated by growth condition and assumption made splitting the steady state flux between isozyme pairs.
  * **CS3_construction_functions.py**: A python script containing various functions used in constructing the *E. coli* glycolysis models and all associated enzyme modules.
  * **Model Construction Glucose Media 99-01 isozyme_split.ipynb**: Construction notebook for glucose growth conditions, with 99% of flux assigned to the first isozyme and 1% of flux assigned to the second isozyme.
  * **Model Construction Glucose Media 75-25 isozyme_split.ipynb**: Construction notebook for glucose growth conditions, with 75% of flux assigned to the first isozyme and 25% of flux assigned to the second isozyme.
  * **Model Construction Glucose Media 50-50 isozyme_split.ipynb**: Construction notebook for glucose growth conditions, with 50% of flux assigned to the first isozyme and 50% of flux assigned to the second isozyme.
  * **Model Construction Glucose Media 25-75 isozyme_split.ipynb**: Construction notebook for glucose growth conditions, with 25% of flux assigned to the first isozyme and 75% of flux assigned to the second isozyme.
  * **Model Construction Glucose Media 01-99 isozyme_split.ipynb**: Construction notebook for glucose growth conditions, with 1% of flux assigned to the first isozyme and 99% of flux assigned to the second isozyme.
  * **Model Construction Pyruvate Media 99-01 isozyme_split.ipynb**: Construction notebook for pyruvate growth conditions, with 99% of flux assigned to the first isozyme and 1% of flux assigned to the second isozyme.
  * **Model Construction Pyruvate Media 75-25 isozyme_split.ipynb**: Construction notebook for pyruvate growth conditions, with 75% of flux assigned to the first isozyme and 25% of flux assigned to the second isozyme.
  * **Model Construction Pyruvate Media 50-50 isozyme_split.ipynb**: Construction notebook for pyruvate growth conditions, with 50% of flux assigned to the first isozyme and 50% of flux assigned to the second isozyme.
  * **Model Construction Pyruvate Media 25-75 isozyme_split.ipynb**: Construction notebook for pyruvate growth conditions, with 25% of flux assigned to the first isozyme and 75% of flux assigned to the second isozyme.
  * **Model Construction Pyruvate Media 01-99 isozyme_split.ipynb**: Construction notebook for pyruvate growth conditions, with 1% of flux assigned to the first isozyme and 99% of flux assigned to the second isozyme.
* **model_analysis_notebooks**:  Contains notebooks to analyze ensembles of *E. coli* glycolysis models.
  * **CS3_analysis_functions.py**: A python script containing various functions used in analyzing the ensembles of *E. coli* glycolysis models.
  * **Analysis on Gibbs Free Energy and Enzyme Abundances for Isozyme Flux Split Sensitivity.ipynb**: Analysis of the Gibbs free energy for reactions and the fractional abundances of enzyme forms, with emphasis on the sensitivity of the flux split between isozyme pairs. Used for generating S1 Figure in MASSpy publication.
  * **Analysis on Gibbs Free Energy and Enzyme Abundances for Growth Conditions.ipynb**: Analysis of the Gibbs free energy for reactions and the fractional abundances of enzyme forms, with emphasis on the differences between glucose and pyruvate growth conditions. Used for generating Figure 4 and S2 Figure in MASSpy publication.
* **CS3_data**:
  * **analysis_figures**: Contains PDFs of individually generated plots, used as panels for publication figures.
  * **enzyme_module_data**: Contains all data necessary for constructing individual enzyme modules. Data obtained and exported from [MASSef](https://github.com/opencobra/MASSef) package.
  * **models_isozyme_split_99_1**: Contains models genereated for both growth conditions with 99% of flux assigned to the first isozyme and 1% of flux assigned to the second isozyme during construction.
  * **models_isozyme_split_75_25**: Contains models genereated for both growth conditions with 75% of flux assigned to the first isozyme and 25% of flux assigned to the second isozyme during construction.
  * **models_isozyme_split_50_50**: Contains models genereated for both growth conditions with 50% of flux assigned to the first isozyme and 50% of flux assigned to the second isozyme during construction.
  * **models_isozyme_split_25_75**: Contains models genereated for both growth conditions with 25% of flux assigned to the first isozyme and 75% of flux assigned to the second isozyme during construction.
  * **models_isozyme_split_1_99**: Contains models genereated for both growth conditions with 1% of flux assigned to the first isozyme and 99% of flux assigned to the second isozyme during construction.
  * **iML1515.json**: The reconstruction of *E. coli* iML1515 as a JSON file.  
  * **iML1515_Glycolysis_map.json**: An Escher map of the glycolytic subnetwork for *E. coli* iML1515 as a JSON file.  
  * **model_creation_data.xlsx**: An excel sheet containing additional data necessary for contructing the kinetic model of *E. coli* glycolysis. Data includes flux and concentration growth data, equilibrium constants, values necessary for converting from grams of cellular dry weight (gDW) to liters (L).
  
