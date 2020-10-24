#!/bin/sh

set -e

cd $( cd "$(dirname "$0")" ; pwd -P )

# Execute notebooks in order
for notebook in 'glycolysis' \
                'hemoglobin' \
                'hex1' \
                'pfk' \
                'pyk' \
                'bon-personalized_model_construction' \
                'non-personalized_model_validation' \
                'fig2_panels' ; do \
    echo "Executing $notebook.ipynb"
    jupyter nbconvert --execute "$notebook.ipynb" --to notebook \
        --ExecutePreprocessor.timeout=-1 \
        --Application.log_level='CRITICAL' \
        --ExecutePreprocessor.store_widget_state=True \
        --inplace
done