# -*- coding: utf-8 -*-
"""Contains functions for facilitating the E.coli glycolytic case study."""

import os
import re
from collections import defaultdict
from operator import attrgetter, iconcat

import matplotlib as mpl
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Arial"
import numpy as np

import pandas as pd

from six import iteritems

import sympy as sym

from mass import MassMetabolite
from mass.enzyme_modules import (
    EnzymeModule, EnzymeModuleForm, EnzymeModuleReaction)
from mass.io.json import load_json_model
from mass.util.expressions import strip_time


def format_percent_str(percent):
    percent = int(round(percent * 100, 0))
    if percent < 10:
        percent = " " + str(percent).replace(".", "") + " "
    else:
        percent = str(percent).replace(".", "")
    return percent



def _load_models_for_analysis(*args):
    n, model_dir, medium, verbose = args
    trimmed_sorted_model_dir = sorted([
        filename for filename in os.listdir(model_dir)
        if medium[:3] + "_Growth_Glycolysis"in filename])

    if not (isinstance(n, str) and n.lower() == "all"):
        trimmed_sorted_model_dir = trimmed_sorted_model_dir[:n]

    models = [
        load_json_model(os.path.join(model_dir, filename))
        for filename in trimmed_sorted_model_dir]
    if verbose:
        print("Number of models for condition: {0}".format(len(models)))

    return models


def load_all_models_for_growth_condition_analysis(n_models, model_dir, medium,
                                                  isozyme_split_percentages,
                                                  verbose=False):
    models_dict = {}
    for percent in isozyme_split_percentages:
        new_model_dir = os.path.abspath(
            os.path.join(
                model_dir, "models_isozyme_split_{0}_{1}".format(
                    format_percent_str(percent).strip(),
                    format_percent_str(1.00 - percent).strip())))

        models_dict[percent] = _load_models_for_analysis(
            n_models, new_model_dir, medium, verbose)
    return models_dict


def _get_Keq_data(enzyme_id, Keq_df):
    if enzyme_id[:3] in Keq_df.index:
        Keq_data = Keq_df.loc[enzyme_id[:3]].values
    else:
        Keq_data = Keq_df.loc[enzyme_id].values
    return Keq_data


def _make_diseq_expr(rxn_str, Keq):
    arrow = "<=>" if "<=>" in rxn_str else "-->"
    reactants, products = [
        s.strip().split(" + ") for s in rxn_str.split(arrow)]
    reactants = [x for x in reactants if x not in ["h_c", "h2o_c"]]
    products = [x for x in products if x not in ["h_c", "h2o_c", "2.0 * h_c"]]
    mass_action_ratio = "({0}) / ({1})".format(
        " * ".join(products), " * ".join(reactants))
    expr = sym.sympify(
        "({0}) / {1}".format(mass_action_ratio, Keq),
        locals={m: sym.Symbol(m) for m in list(reactants + products)})
    return expr


def _get_gibbs_data_for_conditions(model_dicts, isozyme_split_percentages,
                                   diseq_expr, T, flux_sensitivity=False,
                                   differential=False):
    R = 8.314 / 1000 # kJ / mol·K
    gibbs_energy_data_per_condition = []
    for model_dict in model_dicts.values():
        data = {}
        for percent in isozyme_split_percentages:
            data[percent] = R * T * np.log10(
                np.array([
                    float(diseq_expr.subs({
                        m: model.metabolites.get_by_id(m).ic
                        for m in sorted(
                            list(map(str, diseq_expr.atoms(sym.Symbol))))}))
                    for model in model_dict[percent]
                ])
            )
        df = pd.DataFrame.from_dict(data)
        df.index = [model.id for model in model_dict[percent]]
        gibbs_energy_data_per_condition.append(df)

    if flux_sensitivity:
        if differential:
            gibbs_energy_data_per_condition = [pd.DataFrame(
                gibbs_energy_data_per_condition[0].values 
                - gibbs_energy_data_per_condition[1].values, 
                columns=isozyme_split_percentages)]

        return gibbs_energy_data_per_condition
    
    for medium, df in zip(model_dicts, gibbs_energy_data_per_condition):
        df.index = [x[4:] for x in df.index]
        df.columns = [medium]

    if differential:
        gibbs_energy_data_per_condition = [
            pd.DataFrame(
                gibbs_energy_data_per_condition[0].values
                - gibbs_energy_data_per_condition[1].values,
                columns=isozyme_split_percentages)]
    else:
        gibbs_energy_data_per_condition = [pd.concat([
            df for df in gibbs_energy_data_per_condition], axis=1)]

    return gibbs_energy_data_per_condition


def group_PFK1(enzyme_module_dict):
    e_forms_groupings = {
        "E_PFK1_c": [],
        "E_PFK1_c_f6p": [],
        "E_PFK1_c_f6p_atp": [],
        "E_PFK1_c_fdp": [],
        "E_PFK1_c_fdp_adp": [],
        "E_PFK1_c_pep": []}
    for e_form in enzyme_module_dict.enzyme_module_forms:
        mets = {k.id: v for k, v in e_form.bound_metabolites.items()}

        if "f6p_c" in mets and "atp_c" not in mets:
            e_forms_groupings["E_PFK1_c_f6p"].append(e_form.id)
        elif "f6p_c" in mets and "atp_c" in mets:
            e_forms_groupings["E_PFK1_c_f6p_atp"].append(e_form.id)
        elif "fdp_c" in mets and "adp_c" not in mets:
            e_forms_groupings["E_PFK1_c_fdp"].append(e_form.id)
        elif "fdp_c" in mets and "adp_c" in mets:
            e_forms_groupings["E_PFK1_c_fdp_adp"].append(e_form.id)
        elif "E_PFK1_T_c" in e_form.id:
            e_forms_groupings["E_PFK1_c_pep"].append(e_form.id)
        else:
            e_forms_groupings["E_PFK1_c"].append(e_form.id)

    return e_forms_groupings


def _get_frac_abund_data_for_conditions(enzyme_id, model_dicts,
                                        isozyme_split_percentages,
                                        groupings=None,
                                        flux_sensitivity=False,
                                        differential=False):
    abund_data_per_condition = []
    for model_dict in model_dicts.values():
        e_form_data_per_condition_dict = {}
        for percent in isozyme_split_percentages:
            e_form_values_per_model = defaultdict(list)

            for model in model_dict[percent]:
                enzyme_module_dict = model.enzyme_modules.get_by_id(enzyme_id)
                # Get enzyme total concentration
                e_total = sum([
                    e.ic for e in enzyme_module_dict.enzyme_module_forms])
                if e_total != enzyme_module_dict.enzyme_concentration_total:
                    enzyme_module_dict.enzyme_concentration_total = e_total
                # Get enzyme form concentration and make fractional abundance
                for e_form in enzyme_module_dict.enzyme_module_forms:
                    e_form_values_per_model[e_form.id].append(
                        e_form.ic / e_total)

            e_form_df = pd.DataFrame.from_dict(e_form_values_per_model)
            e_form_df.index = [model.id for model in model_dict[percent]]
            e_form_data_per_condition_dict[percent] = e_form_df

        all_data_for_flux_splits = {}
        for e_form in enzyme_module_dict.enzyme_module_forms:
            all_data_for_flux_splits[e_form.id] = pd.DataFrame.from_dict({
                percent: e_form_data_per_condition_dict[percent].loc[
                    :, e_form.id] for percent in isozyme_split_percentages})

        if groupings is not None:
            all_data_for_flux_splits_grouped = {
                e_group: sum([
                    all_data_for_flux_splits[e_form] for e_form in e_forms])
                for e_group, e_forms in groupings.items()}
            abund_data_per_condition.append(all_data_for_flux_splits_grouped)
        else:
            abund_data_per_condition.append(
                all_data_for_flux_splits)
    if groupings is not None:
        e_form_ids = list(groupings)
    else:
        e_form_ids = list(
            enzyme_module_dict.enzyme_module_forms.list_attr("id"))

    if flux_sensitivity:
        if differential:
            abund_data_per_condition =[{
                e_form: pd.DataFrame(
                    abund_data_per_condition[0][e_form].values
                    - abund_data_per_condition[1][e_form].values,
                    columns=isozyme_split_percentages)
                for e_form in e_form_ids}]
        return abund_data_per_condition

    mediums = list(model_dicts.keys())
    for i, (medium, abund_data) in enumerate(
       dict(zip(mediums, abund_data_per_condition)).items()):
        for df in abund_data.values():
            df.index = [x[4:] for x in df.index]
            df.columns = [medium]
        abund_data_per_condition[i] = abund_data
    
    final_e_form_dfs = {}
    for e_form in e_form_ids:
        if differential:
            final_e_form_dfs[e_form] = pd.DataFrame(
                abund_data_per_condition[0][e_form].values
                - abund_data_per_condition[1][e_form].values,
                columns=isozyme_split_percentages)
        else:
            final_e_form_dfs[e_form] = pd.concat([
                e_form_dfs[e_form] for e_form_dfs in abund_data_per_condition],
                axis=1)

    return [final_e_form_dfs]


def _get_box_positions(n_groups, n_boxes_per_group, scalar=1):
    group_positions = list(range(
        0, n_groups*n_boxes_per_group, n_boxes_per_group))
    all_positions = {}
    for i in range(0, n_boxes_per_group):
        all_positions[i] = [scalar * x + i for x in group_positions]
        for j, val in enumerate(all_positions[i]):
            all_positions[i][j] = val + j

    # Even number of boxes, get center of middle boxes
    if n_boxes_per_group == 1:
        label_positions = all_positions[(len(all_positions) - 1)/2]
    elif n_boxes_per_group % 2 == 0:
        label_positions = [(u + l)/2 for l, u in zip(
            all_positions[np.floor((n_boxes_per_group - 1)/2)],
            all_positions[np.ceil((n_boxes_per_group - 1)/2)])]
    # Odd number of boxes, get center of middle box
    else:
        label_positions = all_positions[(n_boxes_per_group - 1)/2]

    return label_positions, all_positions


def _plot_gibbs(ax, data, colors, enzyme_id, categories, differential,
                flux_sensitivity):
    categories = categories.copy()
    categories.reverse()
    lw = 2
    plot_kwargs = {
        "widths": 0.90,
        "vert": False,
        "patch_artist": True,
        "showfliers": True,
        "showmeans": False,
        "capprops": {"linewidth": lw},
        "boxprops": {"linewidth": lw},
        "whiskerprops": {"linewidth": lw},
        "flierprops": {"markersize": 6, "marker": "D"},
        "medianprops": {"linewidth": lw},
        "meanprops": {"linewidth": lw},
    }

    all_positions = _get_box_positions(1, len(data.columns))[1]
    all_positions = [v[0] for v in all_positions.values()]
    # Line at Equilibrium
    pad = 1
    ylim = (all_positions[0] - pad, all_positions[-1] + pad)

    ax.plot([0, 0], ylim, c="k", ls="--", label="Equilibrium", zorder=2, lw=lw)
    # Plot boxes
    data = data.T.reindex(index=data.T.index[::-1])
    boxes = ax.boxplot(data, positions=all_positions, **plot_kwargs)
    ax.set_ylim(ylim)
    ax.set_yticks([])
    if "_" in enzyme_id:
        enzyme_id = enzyme_id.replace("_", "^{") + "}"
    
    title_str = r"$\mathrm{" + enzyme_id +\
                r"\ Gibbs\ Free\ Energy\ (\Delta G')}\ }$"
    ax.set_title(title_str, fontsize="xx-large")
    ax.yaxis.set_label_coords(-0.1,  0.4)

    for key in ["whiskers", "caps"]:
        color_counter = 0
        for i, item in enumerate(boxes[key], start=0):
            item.set_color(colors[color_counter])
            item.set_linewidth(3)
            color_counter += 1 if (i + 1) % 2 == 0 else 0
    for i, item in enumerate(boxes["boxes"], start=0):
        col = list(mpl.colors.to_rgba(colors[i]))
        col[-1] /= 2
        item.set_facecolor(col)
        item.set_linewidth(2)
    for i, item in enumerate(boxes["medians"], start=0):
        item.set_color("black")
    for i, item in enumerate(boxes["fliers"], start=0):
        col = list(mpl.colors.to_rgba(colors[i]))
        col[-1] /= 2
        item.set_markerfacecolor(col)
        item.set_markeredgewidth(1)
        item.set_markeredgecolor("black")

    legend_kwargs = dict(
        loc="center right",
        bbox_to_anchor=(-0.01, 0.5),
        fontsize="large",
        fancybox=True,
        borderpad=1,
        frameon=False)
    legend_items = list(boxes["boxes"])
    
    if flux_sensitivity:
        legend_items.reverse()
        ax.legend(
            legend_items, [r"{0}%/{1}% split".format(
                format_percent_str(percent),
                format_percent_str(1 - percent)) 
                for percent in categories],
            **legend_kwargs)
    elif not flux_sensitivity and differential:
        legend_items.reverse()
        categories.reverse()
        ax.legend(legend_items, ["{0} - {1}".format(*categories)],
                    **legend_kwargs)
    else:
        legend_items.reverse()
        categories.reverse()
        ax.legend(legend_items, categories, **legend_kwargs)
    
    return ax


def _plot_frac_abundance_for_growth_conditions(ax, data, colors, enzyme_id,
                                               mediums, differential):
    lw = 2
    plot_kwargs = {
        "widths": 0.90,
        "vert": True,
        "patch_artist": True,
        "showfliers": True,
        "showmeans": False,
        "capprops": {"linewidth": lw},
        "boxprops": {"linewidth": lw},
        "whiskerprops": {"linewidth": lw},
        "flierprops": {"markersize": 6, "marker": "D"},
        "medianprops": {"linewidth": lw},
        "meanprops": {"linewidth": lw},
    }

    label_positions, all_positions = _get_box_positions(
        len(data), len(mediums))
    positions = np.array([x for x in all_positions.values()])
    pad = 0.5
    xlim = (positions.min() - pad,  positions.max() + pad)
    if differential:
        ax.plot(xlim, [0, 0], c="xkcd:dark grey", ls=":", zorder=2, lw=lw)
    for i, medium in enumerate(mediums):
        values = []

        for df in data.values():
            values.append(df[medium].values)
        boxes = ax.boxplot(np.array(values).T, positions=all_positions[i],
                           **plot_kwargs)
        for key, color in zip(
           ["whiskers", "caps", "boxes", "fliers", "medians"],
           [colors[i]] * 4 + ["black"]):
            for item in boxes[key]:
                if key in ["boxes", "fliers"]:
                    col = list(mpl.colors.to_rgba(color))
                    col[-1] /= 2
                    if key == "boxes":
                        item.set_facecolor(col)
                        item.set_linewidth(lw)
                    else:
                        item.set_markerfacecolor(color)
                        item.set_markeredgewidth(1)
                        item.set_markeredgecolor("black")
                else:
                    item.set_color(color)

    ax.set_xlim(xlim)
    ax.set_xticks(label_positions)
    def _correct_enzyme_id_xlabel(e_id, enzyme_id):
        
        def split_str(string, search, additional):
            return (string[:search + additional], 
                    string[search + additional:])
        latex_comp_str = "_{c}}"
        e_id = e_id.replace("E_", "").replace("_c", latex_comp_str)
        e_id = e_id.replace(
            enzyme_id, r"\mathrm{{" + enzyme_id.replace("_", r"\_") + "}")
        search = e_id.find(latex_comp_str)
        if e_id[search + len(latex_comp_str)-1:] != "}":
            s1, s2 = split_str(e_id, search, len(latex_comp_str))
            s2 = "^".join(str(r"^\mathrm{" + s2[1:] + "}").split("__"))
            e_id = s1 + r",\ ".join(s2.split("_"))

        return r"$" + e_id + r"}$"

    xticklabels = [_correct_enzyme_id_xlabel(x, enzyme_id)
                   for x in list(data)]

    ax.set_xticklabels(xticklabels, rotation=30, fontsize="x-large",
                       ha="center")
    if "_" in enzyme_id:
        enzyme_id = enzyme_id.replace("_", r"\_")
    if differential:
        title_str = r"$\mathrm{" + enzyme_id +\
                    r"\ Differential\ Fractional\ Abundance}$"
        ax.set_ylim(-1.01, 1.01)
        ax.set_yticks([-1, -0.5, 0, 0.5, 1])
        ax.set_yticklabels([-1, -0.5, 0, 0.5, 1], fontsize="large")
    else:
        title_str = r"$\mathrm{" + enzyme_id +\
                    r"\ Fractional\ Abundance}$"
        ax.set_ylim(-0.05, 1.05)
        ax.set_yticks([0, 0.5, 1])
        ax.set_yticklabels([0, "", 1], fontsize="xx-large")
    ax.set_title(title_str, fontsize="xx-large")


    ylabel = r"$\frac{\mathrm{" + enzyme_id +\
             r"\ enzyme\ form}}{\mathrm{" + enzyme_id +\
             r"_{tot}}}$"
    ax.set_ylabel(ylabel, fontsize="xx-large", rotation=0)
    ax.yaxis.set_label_coords(-0.15,  0.45)

    return ax


def _plot_frac_abundance_for_flux_splits(ax, data, colors, enzyme_id,
                                         isozyme_split_percentages,
                                         differential):
    lw = 2
    plot_kwargs = {
        "widths": 0.90,
        "vert": True,
        "patch_artist": True,
        "showfliers": True,
        "showmeans": False,
        "capprops": {"linewidth": lw},
        "boxprops": {"linewidth": lw},
        "whiskerprops": {"linewidth": lw},
        "flierprops": {"markersize": 6, "marker": "D"},
        "medianprops": {"linewidth": lw},
        "meanprops": {"linewidth": lw},
    }

    label_positions, all_positions = _get_box_positions(
        len(data), len(isozyme_split_percentages))
    positions = np.array([x for x in all_positions.values()])
    pad = 0.5
    xlim = (positions.min() - pad,  positions.max() + pad)
    if differential:
        ax.plot(xlim, [0, 0], c="xkcd:dark grey", ls=":", zorder=2, lw=lw)
    for i, percent in enumerate(isozyme_split_percentages):
        values = []
        for df in data.values():
            values.append(df[percent].values)
        boxes = ax.boxplot(np.array(values).T, positions=all_positions[i],
                           **plot_kwargs)
        for key, color in zip(
           ["whiskers", "caps", "boxes", "fliers", "medians"],
           [colors[i]] * 4 + ["black"]):
            for item in boxes[key]:
                if key in ["boxes", "fliers"]:
                    col = list(mpl.colors.to_rgba(color))
                    col[-1] /= 2
                    if key == "boxes":
                        item.set_facecolor(col)
                        item.set_linewidth(lw)
                    else:
                        item.set_markerfacecolor(color)
                        item.set_markeredgewidth(1)
                        item.set_markeredgecolor("black")
                else:
                    item.set_color(color)

    ax.set_xlim(xlim)
    ax.set_xticks(label_positions)
    def _correct_enzyme_id_xlabel(e_id, enzyme_id):
        
        def split_str(string, search, additional):
            return (string[:search + additional], 
                    string[search + additional:])
        latex_comp_str = "_{c}}"
        e_id = e_id.replace("E_", "").replace("_c", latex_comp_str)
        e_id = e_id.replace(
            enzyme_id, r"\mathrm{{" + enzyme_id.replace("_", r"\_") + "}")
        search = e_id.find(latex_comp_str)
        if e_id[search + len(latex_comp_str)-1:] != "}":
            s1, s2 = split_str(e_id, search, len(latex_comp_str))
            s2 = "^".join(str(r"^\mathrm{" + s2[1:] + "}").split("__"))
            e_id = s1 + r",\ ".join(s2.split("_"))

        return r"$" + e_id + r"}$"

    xticklabels = [_correct_enzyme_id_xlabel(x, enzyme_id)
                   for x in list(data)]

    ax.set_xticklabels(xticklabels, rotation=30, fontsize="x-large",
                       ha="center")
    if "_" in enzyme_id:
        enzyme_id = enzyme_id.replace("_", r"\_")
    if differential:
        title_str = r"$\mathrm{" + enzyme_id +\
                    r"\ Differential\ Fractional\ Abundance}$"
        ax.set_ylim(-1.01, 1.01)
        ax.set_yticks([-1, -0.5, 0, 0.5, 1])
        ax.set_yticklabels([-1, -0.5, 0, 0.5, 1], fontsize="large")
    else:
        title_str = r"$\mathrm{" + enzyme_id +\
                    r"\ Fractional\ Abundance}$"
        ax.set_ylim(-0.05, 1.05)
        ax.set_yticks([0, 0.5, 1])
        ax.set_yticklabels([0, "", 1], fontsize="xx-large")
    ax.set_title(title_str, fontsize="xx-large")


    ylabel = r"$\frac{\mathrm{" + enzyme_id +\
             r"\ enzyme\ form}}{\mathrm{" + enzyme_id +\
             r"_{tot}}}$"
    ax.set_ylabel(ylabel, fontsize="xx-large", rotation=0)
    ax.yaxis.set_label_coords(-0.15,  0.45)

    return ax


def _make_figure(enzyme_id, mediums=None, split_percentages=None,
                 gibbs_data=None, e_form_data=None, differential=False,
                 include_gibbs_energy=True, 
                 flux_sensitivity=False, colors=None):
    if include_gibbs_energy:
        fig = plt.figure(figsize=(10, 10))
    else:
        fig = plt.figure(figsize=(10, 5))
    if include_gibbs_energy:
        gs = fig.add_gridspec(nrows=2, ncols=1, height_ratios=[1, 4])
        # Gibbs energy plot on top axes
        gibbs_ax = fig.add_subplot(gs[0, :])
        # Fractional abundance plots for each enzyme form
        e_form_frac_ax = fig.add_subplot(gs[1, :])
    else:
        gs = fig.add_gridspec(nrows=1, ncols=1)
        e_form_frac_ax = fig.add_subplot(gs[0])

    split_percentages = split_percentages.copy()
    colors = colors.copy()

    if flux_sensitivity:
        e_form_frac_ax = _plot_frac_abundance_for_flux_splits(
            ax=e_form_frac_ax, data=e_form_data, colors=colors,
            enzyme_id=enzyme_id,
            isozyme_split_percentages=split_percentages,
            differential=differential)


        # Reverse for gibbs energy plot so small on top, large on bottom
        if include_gibbs_energy:
            split_percentages.reverse()
            colors.reverse()
            gibbs_ax = _plot_gibbs(
                ax=gibbs_ax, data=gibbs_data, colors=colors, enzyme_id=enzyme_id,
                categories=split_percentages, differential=differential,
                flux_sensitivity=flux_sensitivity)
    else:
        if differential:
            e_form_frac_ax = _plot_frac_abundance_for_growth_conditions(
                ax=e_form_frac_ax, data=e_form_data, colors=colors,
                enzyme_id=enzyme_id,
                mediums=split_percentages,
                differential=differential)
        else:
            e_form_frac_ax = _plot_frac_abundance_for_growth_conditions(
                ax=e_form_frac_ax, data=e_form_data, colors=colors,
                enzyme_id=enzyme_id,
                mediums=mediums,
                differential=differential)
            # Reverse for gibbs energy plot so small on top, large on bottom
            split_percentages.reverse()
            colors.reverse()
            
        if include_gibbs_energy:
            gibbs_ax = _plot_gibbs(
                ax=gibbs_ax, data=gibbs_data, colors=colors,
                enzyme_id=enzyme_id,
                categories=mediums, differential=differential,
                flux_sensitivity=flux_sensitivity)

    fig.tight_layout(w_pad=10, h_pad=3)
    return fig


def create_figures_for_export(enzyme, model_dicts, isozyme_split_percentages,
                              Keq_df, differential=False,
                              include_gibbs_energy=True,
                              flux_sensitivity=False,
                              groupings=None, colors=None,
                              temperature=310.15):
    if differential and len(model_dicts) != 2:
        raise ValueError(
            "Differential with only two growth conditions allowed")

    
    if flux_sensitivity and len(colors) != len(isozyme_split_percentages):
        raise ValueError("Number of colors must equal number of "
                         "isozyme split percentages")
    if not flux_sensitivity:
        if not differential and len(colors) != len(model_dicts):
            raise ValueError("Number of colors must equal number of medium "
                             "conditions")
        if isinstance(colors, str):
            colors = [colors]
        if differential and len(colors) != 1:
            raise ValueError("Number of colors must equal 1 for differential "
                             "conditions")
    all_gibbs_data = _get_gibbs_data_for_conditions(
        model_dicts=model_dicts,
        isozyme_split_percentages=isozyme_split_percentages,
        T=temperature,
        diseq_expr=_make_diseq_expr(*_get_Keq_data(enzyme, Keq_df)),
        flux_sensitivity=flux_sensitivity,
        differential=differential)

    all_e_form_data = _get_frac_abund_data_for_conditions(
        enzyme_id=enzyme,
        model_dicts=model_dicts,
        isozyme_split_percentages=isozyme_split_percentages,
        groupings=groupings,
        flux_sensitivity=flux_sensitivity,
        differential=differential)
    
    figs = []
    for gibbs_data, e_form_data in zip(all_gibbs_data, all_e_form_data):
        figs.append(_make_figure(
                enzyme_id=enzyme,
                mediums=list(model_dicts.keys()),
                split_percentages=isozyme_split_percentages,
                gibbs_data=gibbs_data,
                e_form_data=e_form_data,
                differential=differential,
                include_gibbs_energy=include_gibbs_energy,
                flux_sensitivity=flux_sensitivity,
                colors=colors))

    return figs


def save_figure(enzyme_id, medium, fig_type, fig, svg=True, pdf=True):
    path = "../CS3_data/analysis_figures/{0}/".format(fig_type)
    try:
        os.listdir(path)
    except FileNotFoundError:
        os.mkdir(path)
    if svg:
        save_path = path + "_".join((medium, enzyme_id)) + ".svg"
        fig.savefig(save_path)
        print("Saved at " + save_path)
    if pdf:
        save_path = path + "_".join((medium, enzyme_id)) + ".pdf"
        fig.savefig(save_path)
        print("Saved at " + save_path)
    


def create_all_enzyme_gibbs_energy_figure(all_enzymes, model_dicts, 
                                          isozyme_split_percentages,
                                          Keq_df=None, differential=False,
                                          flux_sensitivity=False,
                                          colors=None, excluded_isozymes=None,
                                          temperature=310.15):
    
    if isinstance(all_enzymes, str):
        all_enzymes = [all_enzymes]
    fig = plt.figure(figsize=(10, len(all_enzymes)*2))
    ax = fig.add_subplot()
    lw=2
    plot_kwargs = {
        "widths": 0.90,
        "vert": False,
        "patch_artist": True,
        "showfliers": True,
        "showmeans": False,
        "capprops": {"linewidth": lw},
        "boxprops": {"linewidth": lw},
        "whiskerprops": {"linewidth": lw},
        "flierprops": {"markersize": lw*3, "marker": "D"},
        "medianprops": {"linewidth": lw},
        "meanprops": {"linewidth": lw},
    }
    
    all_enzymes = [e for e in all_enzymes if e not in excluded_isozymes]
    all_gibbs_data_per_enzyme = {}
    for enzyme in all_enzymes:
        diseq_expr = _make_diseq_expr(*_get_Keq_data(enzyme, Keq_df))
        gibbs_data = _get_gibbs_data_for_conditions(
            model_dicts, isozyme_split_percentages, diseq_expr, temperature,
            flux_sensitivity, differential)[0]
        all_gibbs_data_per_enzyme[enzyme] = gibbs_data
        
    if flux_sensitivity:
        categories = isozyme_split_percentages
    else:
        categories = list(model_dicts)
    
    pad = 1
    labelsize = 15
    label_positions, all_positions = _get_box_positions(
        len(all_enzymes), len(categories), scalar=pad)
    positions = np.array([x for x in all_positions.values()])
        
    xlim = [None, None]
    
    legend_items = {}
    for i, category in enumerate(categories):
        data = pd.DataFrame.from_dict({
            enzyme: all_gibbs_data_per_enzyme[enzyme][category]
            for enzyme in all_enzymes})
        data = data.T.reindex(index=data.T.index[::-1])
        
        if xlim[0] is None or data.min().min() < xlim[0]:
            xlim[0] = np.floor(data.min().min())
        if xlim[-1] is None or data.max().max() > xlim[-1]:
            xlim[-1] = np.ceil(data.max().max())
        
        boxes = ax.boxplot(data, **plot_kwargs, positions=all_positions[i])
        for key, color in zip(
           ["whiskers", "caps", "boxes", "fliers", "medians"],
           [colors[i]] * 4 + ["black"]):
            for item in boxes[key]:
                if key in ["boxes", "fliers"]:
                    col = list(mpl.colors.to_rgba(color))
                    col[-1] /= len(categories)
                    if key == "boxes":
                        item.set_facecolor(col)
                        item.set_linewidth(lw)
                    else:
                        item.set_markerfacecolor(color)
                        item.set_markeredgewidth(1)
                        item.set_markeredgecolor("black")
                else:
                    item.set_color(color)
        legend_items[category] = list(boxes["boxes"])

    ax.legend([v[0] for v in legend_items.values()],
              list(legend_items.keys()), **dict(
                  loc="upper center",
                  bbox_to_anchor=(0.5, 1.075),
                  fontsize= 60 / len(categories) * 1.5,
                  fancybox=True,
                  borderpad=1,
                  frameon=False,
                  ncol=len(categories)))
    ylim = (positions.min() - pad,  positions.max() + pad)
    line = ax.plot([0, 0], ylim, c="k", ls="--", label="Equilibrium", zorder=2, 
                  lw=lw)
    ax.annotate("Equilibrium", xy=(line[0].get_xdata()[-1],
                                   line[0].get_ydata()[-1]),
                xytext=(-50, 10),
                xycoords="data", textcoords="offset points",
                size=20, va="center")
    
    xlim = [-max(abs(np.array(xlim))), max(abs(np.array(xlim)))]
    
    for i in range(*ylim, int((ylim[1] - ylim[0]) / len(all_enzymes))):
        ax.plot(xlim, [i, i], c="xkcd:light grey", ls="-", zorder=2, lw=lw/2)
    ax.set_xlim(xlim)
    ax.tick_params(axis='x', which='major', labelsize=labelsize)
    ax.set_ylim(ylim)
    ax.set_yticks(label_positions)
    labels = [
        all_enzymes[i-1][:3] if all_enzymes[i-1][:3] in [e[:3]
        for e in excluded_isozymes]
        else all_enzymes[i-1] for i in range(len(all_enzymes), 0, -1)]
    labels = [r"$\mathrm{" + enzyme_id.replace("_", r"\_") + r"}$"
              if "_" in enzyme_id
              else r"$\mathrm{" + enzyme_id + r"}$"for enzyme_id in labels]
    ax.set_yticklabels(labels, rotation=0, fontsize=2*labelsize)
    
    fig.tight_layout(w_pad=10, h_pad=3)
    return fig
    