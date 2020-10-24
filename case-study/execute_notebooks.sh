#!/bin/sh

set -e

cd $( cd "$(dirname "$0")/model_construction_notebooks" ; pwd -P )

# Execute notebooks in order
for media in 'glucose' 'pyruvate' ; do \
    for split in '99-01' '75-25' '50-50' '25-75' '01-99' ; do \
        notebook="model_construction_${media}_media_${split}_isozyme_split"
        echo "Executing $notebook.ipynb"
        jupyter nbconvert --execute "$notebook.ipynb" --to notebook \
            --ExecutePreprocessor.timeout=-1 \
            --Application.log_level='CRITICAL' \
            --inplace
    done
done

cd $( cd "$(dirname "$0")/model_analysis_notebooks" ; pwd -P )

# Execute notebooks in order
for notebook in 'analysis_on_gibbs_free_energy_and_enzyme_abundances_for_growth_conditions' \
                'analysis_on_gibbs_free_energy_and_enzyme_abundances_for_isozyme_flux_split_sensitivity' ; do \
    echo "Executing $notebook.ipynb"
    jupyter nbconvert --execute "$notebook.ipynb" --to notebook \
        --ExecutePreprocessor.timeout=-1 \
        --Application.log_level='CRITICAL' \
        --ExecutePreprocessor.store_widget_state=True \
        --inplace
done