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
from lvtlaw.a_utils import A, R, mag, abs_bands, ap_bands, colors, data_dir, data_out, regression, dis_flag, process_step
import pandas as pd
from functools import reduce
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
out_dir = data_out

def residue_correlation(residue_file, dis_flag, col, flag): 
    del_mc = pd.DataFrame()         # Stores regression results
    del_predictions = pd.DataFrame({'name': residue_file['name']})  # Star-by-star predictions
    del_residuals = del_predictions.copy()   # Star-by-star residuals
    print('\tColor:', col)
    for diss in dis_flag:
        regression_names = []
        slopes, intercepts = [], []
        slope_errors, intercept_errors = [], []
        for band in mag:
            y_key = 'r_' + band + '0' + diss
            wesenheit = f"{band}{col}" if flag == "S" else f"{col[0]}{col}"
            x_key = 'r_' + wesenheit + diss
            regression_name = band + wesenheit
            # Perform regression
            slope, intercept, predicted, residual, slope_err, intercept_err = regression(
                residue_file[x_key], residue_file[y_key], wesenheit, band + '0' + diss, 1)
            regression_names.append(regression_name)
            slopes.append(slope)
            intercepts.append(intercept)
            slope_errors.append(slope_err)
            intercept_errors.append(intercept_err)
            del_residuals[f'd_{regression_name}{diss}'] = residual
            del_predictions[f'p_{regression_name}{diss}'] = predicted
        # Save regression metadata for this distance flag
        del_mc['name'] = regression_names
        del_mc[f'm{diss}'] = slopes
        del_mc[f'c{diss}'] = intercepts
        del_mc[f'me{diss}'] = slope_errors
        del_mc[f'ce{diss}'] = intercept_errors
    return del_residuals, del_predictions, del_mc

def residue_analysis(residue_file, dis_flag:list, cols:list , flags:list, s=1):
    # Initialize result containers
    dmc = []
    dres = pd.DataFrame({'name': residue_file['name'], 'logP': residue_file['logP'], 'EBV': residue_file['EBV']})
    dpre = dres.copy()
    for flg in flags:
        for col in cols:
            res, pre, mc = residue_correlation(residue_file, dis_flag, col, flg)
            dres = pd.merge(dres, res[[cl for cl in res.columns if cl not in dres.columns or cl == 'name']], on='name')
            dpre = pd.merge(dpre, pre[[cl for cl in pre.columns if cl not in dpre.columns or cl == 'name']], on='name')
            dmc.append(mc) 
    # Combine regression dataframes
    del_mc = pd.concat(dmc, ignore_index=True).drop_duplicates().set_index('name').T
    # Optional: Save to CSV
    if s == 1:
        out_base = f"{out_dir}{process_step[2]}{len(residue_file)}_"
        del_mc.to_csv(f'{out_base}del_slope_intercept.csv')
        dres.to_csv(f'{out_base}del_res.csv')
        dpre.to_csv(f'{out_base}del_pre.csv')
    return dres, dpre, del_mc

