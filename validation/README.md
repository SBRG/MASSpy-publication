# Case Study 1: Enzyme Regulation in MASS Models
Validation of MASSpy as a modeling tool by describing mechanisms of enzyme regulation using enzymes modules as seen in 

> Yurkovich JT, Alcantar MA, Haiman ZB, Palsson BO (2018) Network-level allosteric effects are elucidated by detailing how ligand-binding events modulate utilization of catalytic potentials. PLOS Computational Biology 14(8): e1006356. https://doi.org/10.1371/journal.pcbi.1006356

## Directory and file descriptions:
* **Glycolysis.ipynb**: 
  * A notebook to construct a steady state model of RBC glycolysis using mass action kinetics.
* **Hemoglobin.ipynb**:
  * A notebook to construct a module of hemoglobin to integrate into glycolysis model.
* **HEX1.ipynb**:
  * A notebook to construct an enzyme module of hexokinase (HEX1) to integrate into glycolysis model.
* **PFK.ipynb**:
  * A notebook to construct an enzyme module of phosphofructokinase (PFK) to integrate into glycolysis model.
* **PYK.ipynb**:
  * A notebook to construct an enzyme module of pyruvate kinase (PYK) to integrate into glycolysis model.
* **Non-personalized_Model_construction.ipynb**:
  * A notebook to construct the non-personalized models utilized in [Yurkovich et al.](https://doi.org/10.1371/journal.pcbi.1006356).
* **Non-personalized_Model_validation.ipynb**:
  * A notebook to reproduce [Fig2](https://doi.org/10.1371/journal.pcbi.1006356.g002), [Fig4](https://doi.org/10.1371/journal.pcbi.1006356.g004), and other figures in the [supplement](https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1006356.s001&type=supplementary).
* **Fig2_panels.ipynb**:
  * A notebook to create the panels seen in Figure 2 of the MASSpy publication.
* **CS1_data**:
  * **maps**: Contains Escher maps of Glycolysis with and without PYK enzyme module as JSON files.
  * **models**: Contains all models used in the case study as JSON files.
  * **Non-personalized-data.xlsx**: Excel sheet containing kinetic data necessary to parameterize models as seen in [Yurkovich et al.](https://doi.org/10.1371/journal.pcbi.1006356). Used in **Non-personalized_Model_construction.ipynb**.

