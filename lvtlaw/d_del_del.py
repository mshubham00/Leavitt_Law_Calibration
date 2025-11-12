### File: ./lvtlaw/d_del_del.py
'''
This file correlates the residues of PL and PW relations.

The output will be saved in 'data/{DatasetName_Rv}/3_deldel/*.csv'

Function contained:
    residue_correlation(residue): for given color and flag, perform residual correlation for different distance
        Outout (DataFrame): del_residuals, del_predictions, del_mc
    residue_analysis(residue): For every color and method, residual correlation implimented for every for PL-PW residuals for two version of methods. 
        Output (DataFrame): dres, dpre, del_mc
'''
module = 'd_del_del'
from lvtlaw.a_utils import regression, merge_12, imgsave
from data.datamapping import file_name, data_cols, dis_list, dis_flag, col_dot, col_lin, mag, flags, data_out, wes_show, process_step,z, s, plots, mode
import pandas as pd
import numpy as np
from functools import reduce
import matplotlib.pyplot as plt
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
out_dir = data_out
#####################################################################
def residue_correlation(residue, col, flag, dis_flag = dis_flag): 
    # this function correlates the PL and PW residuals
    del_mc = pd.DataFrame()         # Stores del-del regression slope and intercept
    del_predictions = pd.DataFrame({'name': residue['name'],'logP': residue['logP'],'EBV': residue['EBV'] })  # Star-by-star predictions
    del_residuals = del_predictions.copy()   # collects deldel residuals
    print('\tColor:', col, '\tMethod:', flag)
    for diss in dis_flag:
        regression_names, d_std = [], []
        slopes, intercepts = [], []
        slope_errors, intercept_errors = [], []
        for ab in mode:
            for band in mag:
                y_key = 'r_' + band + ab + diss
                wesenheit = f"{band}{col}" if flag == "S" else f"{col[0]}{col}"
                x_key = 'r_' + wesenheit + diss
                regression_name = band + ab + wesenheit
            # Perform regression
                slope, intercept, predicted, residual, slope_err, intercept_err, stdd = regression(
                    residue[x_key], residue[y_key], wesenheit, band + ab + diss, 1)
                regression_names.append(regression_name)
                d_std.append(stdd)
                slopes.append(slope)
                intercepts.append(intercept)
                slope_errors.append(slope_err)
                intercept_errors.append(intercept_err)
                del_residuals[f'd_{regression_name}{diss}'] = residual #list
                del_predictions[f'p_{regression_name}{diss}'] = predicted
        # Save regression metadata for this distance flag
        del_mc['name'] = regression_names
        del_mc[f'm{diss}'] = slopes
        del_mc[f'c{diss}'] = intercepts
        del_mc[f'me{diss}'] = slope_errors
        del_mc[f'ce{diss}'] = intercept_errors
        del_mc[f'std{diss}'] = d_std
    return del_residuals, del_predictions, del_mc
#####################################################################
def residue_analysis(residue, plots=plots,s=s, dis_flag = dis_flag, cols = wes_show, flags = flags):
    # This function calls residue_correlation() for different different wesenheits
    dmc = []
    dres = pd.DataFrame({'name': residue['name'], 'logP': residue['logP'], 'EBV': residue['EBV']})
    dpre = dres.copy()
    for flg in flags:
        for col in cols:
            res, pre, mc = residue_correlation(residue, col, flg)
            dres = pd.merge(dres, res[[cl for cl in res.columns if cl not in dres.columns or cl == 'name']], on='name')
            dpre = pd.merge(dpre, pre[[cl for cl in pre.columns if cl not in dpre.columns or cl == 'name']], on='name')
            dmc.append(mc) 
    # Combine regression dataframes
    del_mc = pd.concat(dmc, ignore_index=True).drop_duplicates().set_index('name').T
    merged_data = merge_12(residue, dres, on = ['name', 'EBV', 'logP'])    
    merged_data = merge_12(merged_data, dpre, on = ['name', 'EBV', 'logP'])    
   # Optional: Save to CSV
    if s == 1:
        out_base = f"{out_dir}{process_step[2]}{len(residue)}_"
        del_mc.to_csv(f'{out_base}del_slope_intercept.csv')
        dres.to_csv(f'{out_base}del_res.csv')
        dpre.to_csv(f'{out_base}del_pre.csv')
        merged_data.to_csv(f'{out_base}merged_data.csv')
        print(f'Data saved in ./{data_out+process_step[2]}')
    if plots==1:
        for flg in flags:
            for col in cols:
                for dis in dis_flag:
                    plotdeldel6(merged_data, del_mc, col, dis, flg, '0', s)
    return dres, dpre, del_mc, merged_data
#####################################################################
def plotdeldel6(data, dmc, col, dis, flag, ab, s):
# 1. Extracting x-y axis
    print(col)
    fig, axs = plt.subplots(2, 3, figsize=(18, 8), sharex='col')
    axs = axs.flatten()  # Flatten for easy indexing
    for i, m in enumerate(mag[0:6]):
        wes_str = f"{m}{col}" if flag == "S" else f"{col[0]}{col}"
        x = data['r_' + wes_str + dis]
        y = data['r_' + m + ab + dis]
        pred = data['p_' + m + ab+ wes_str + dis]
        residuals =  data['d_' + m + ab+ wes_str + dis]
        if dis == '_i':
            alpha = dmc[m+ab+wes_str].iloc[4]
            gamma = dmc[m+ab+wes_str].iloc[5]
        else:
            alpha = dmc[:4][m+ab+wes_str].iloc[0]
            gamma = dmc[:4][m+ab+wes_str].iloc[1]
#        corr_coef, _ = pr_value(x, y)
        ax = axs[i]
        ax.plot(x, y, col_dot[i], label=f'{m+ab}{wes_str}')
        ax.plot(x, pred, col_lin[i], label=f'Slope: {alpha:.3f}')
        # Residual lines
        for j in range(len(data)):
            label = r"$\delta E_{{BV}} = \Delta M_{%s} / R_{%s}$"%(m,m) if j == 0 else None
            ax.plot([x[j], x[j]], [y[j], pred[j]], color='red', linestyle='--', alpha=0.5, label=label)
        ax.set_ylabel(f'PL Residue: $\\Delta M_{m+ab}$')
        ax.set_xlabel(f'PW Residue: $\\Delta$ {wes_str}')
#        for k in range(len(data)):
#            ax.annotate('%i'%(k), xy =(x.iloc[k], y.iloc[k]), fontsize = 11) 
        #ax.grid(True)
        ax.tick_params(direction='in', top=True, right=True)
        ax.legend()   
        # Clean up spines
        for spine in ax.spines.values():
            spine.set_visible(False)
    # Set x-axis label only on bottom row
#    for i, ax in enumerate(axs):
#        if i >= 3:  # Bottom row
#            ax.set_xlabel(f'{mag[i]}{col}')
#        else:
#            ax.tick_params(labelbottom=False)
    title = f"{file_name}_deldel_{flag}_{ab}{col}{dis}"
    plt.suptitle(f'PL-PW Residuals Correlation {col}')
    plt.tight_layout()
    if s == 1:
        imgsave(title, 2, fil='pdf', p=1)
    plt.show()
    #plotdeldelres(data, dmc, col, dis, flag, ab, s)
#####################################################################
def plotdeldelres(data, dmc, col, dis, flag, ab, s):
    fig_res, axs_res = plt.subplots(2, 3, figsize=(18, 6))
    axs_res = axs_res.flatten()
    x = data['logP'] - 1
    for i, m in enumerate(mag[0:6]):
        wes_str = f"{m}{ab}{m}{col}" if flag == "S" else f"{m}{ab}{col[0]}{col}"
        pred = data['p_' + wes_str + dis]
        y = data['d_' + wes_str + dis]
        if dis == '_i':
            alpha_e = dmc[wes_str].iloc[6]
            gamma_e = dmc[wes_str].iloc[7]
        else:
            alpha_e = dmc[:4][wes_str].iloc[2]
            gamma_e = dmc[:4][wes_str].iloc[3]
        ax_res = axs_res[i]
        stdd = round(y.std(ddof=0), 3)
        ax_res.plot(x, y, col_dot[i], label=f'{m}{col} $\\sigma = $ {stdd}')
        ax_res.axhline(2*np.std(y), color='gray', linestyle='--', linewidth=1)
        ax_res.axhline(0, color='red', linestyle='--', linewidth=1)
        ax_res.axhline(-2*np.std(y), color='gray', linestyle='--', linewidth=1)
        xlabel = f'Error in slope: {alpha_e:.3f} | intercept {gamma_e:.3f}' 
        ax_res.set_xlabel(xlabel)
        ax_res.set_ylabel(f'{m + ab} Band Residuals')
        #ax_res.grid(True)
        ax_res.tick_params(direction='in', top=True, right=True)
        ax_res.legend()
        for spine in ax_res.spines.values():
            spine.set_visible(False)
    for j in range(len(mag), 6):  # Hide any unused axes
        axs_res[j].set_visible(False)
    plt.tight_layout()
    title=f"{file_name}_{flag}_{ab}{col}{dis}"
    if s == 1:
        imgsave(title + "_residuals", 2, fil='png', p=1)
    plt.show()
#####################################################################
print(f'* * {module} module loaded!')
