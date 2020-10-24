import os

import pandas as pd

from mass.io.json import load_json_model

def export_tidy_df_as_csv_value_table(list_of_models, attr,
                                      notebook, filename):
    variable_mapping_dict = {
        "initial_conditions": "init_conds",
        "steady_state_fluxes": "fluxes",
        "_get_all_parameters": "parameters"}

    try:
        df = pd.DataFrame.from_dict({
            model.id: {
                getattr(x, "_id", str(x)): value for x, value in getattr(model, attr).items()}
            for model in list_of_models})
    except AttributeError:
        df = pd.DataFrame.from_dict({
            model.id: {
                getattr(x, "_id", str(x)): value for x, value in getattr(model, attr)().items()}
            for model in list_of_models})
    finally:
        df = df.T.melt(ignore_index=False).reset_index()
        df.rename(columns={"index": "model", "variable": variable_mapping_dict[attr]}, inplace=True)
        df.dropna(inplace=True)
        df.sort_values(by="model", inplace=True)
        df.reset_index(inplace=True, drop=True)

    notebook_dir = os.path.realpath(os.path.join("../data", "tables", notebook))
    try:
        os.listdir(notebook_dir)
    except:
        os.mkdir(notebook_dir)
        
    df.to_csv(os.path.realpath(os.path.join(notebook_dir, filename + ".csv")))

    return

def export_csv_files_for_models(model_list, notebook, prefix="", suffix=""):
    export_tidy_df_as_csv_value_table(
        model_list, "initial_conditions",
        notebook=notebook,
        filename=prefix + "all_model_init_conds" + suffix)
    export_tidy_df_as_csv_value_table(
        model_list, "steady_state_fluxes",
        notebook=notebook,
        filename=prefix + "all_model_fluxes" + suffix)
    export_tidy_df_as_csv_value_table(
        model_list, "_get_all_parameters", 
        notebook=notebook,
        filename=prefix + "all_model_parameters" + suffix)

    print("Exports finished for {0} models".format(str(len(model_list))))

    return