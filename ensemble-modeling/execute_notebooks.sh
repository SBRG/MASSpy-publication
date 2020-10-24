#!/bin/sh

set -e

cd $( cd "$(dirname "$0")" ; pwd -P )

# Execute notebooks in order
for notebook in 'Ensemble_Modeling_Generation' \
                'Ensemble Modeling Analysis' ; do \
    echo "Executing $notebook.ipynb"
    jupyter nbconvert --execute "$notebook.ipynb" --to notebook \
        --ExecutePreprocessor.timeout=-1 \
        --Application.log_level='CRITICAL' \
        --ExecutePreprocessor.store_widget_state=True \
        --inplace
done