### File: ./lvtlaw/d_del_del.py
from lvtlaw.a_utils import A, R, mag, abs_bands, ap_bands, colors, data_dir, input_data_file, data_out, regression, dis_flag, process_step
import pandas as pd
from functools import reduce
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
bands = abs_bands
out_dir = data_out

def residue_correlation(residue_file, dis_flag, col, method_flag): 
    del_mc = pd.DataFrame()         # Stores regression results
    del_predictions = pd.DataFrame({'name': residue_file['name']})  # Star-by-star predictions
    del_residuals = pd.DataFrame({'name': residue_file['name']})    # Star-by-star residuals
    print('\nApproach:', method_flag, '\tColor:', col)
    for diss in dis_flag:
        slopes, intercepts = [], []
        slope_errors, intercept_errors = [], []
        regression_names = []
        for band in mag:
            if method_flag == '_S':
                wesenheit = f"{band}{col}"
            else: 
                wesenheit = f"{col[0]}{col}"
            x_key = 'r_' + wesenheit + diss
            y_key = 'r_' + band + '0' + diss
            regression_name = band + wesenheit
            # Perform regression
            slope, intercept, predicted, residual, slope_err, intercept_err = regression(
                residue_file[x_key], residue_file[y_key], wesenheit, band + '0' + diss, 1)
            regression_names.append(regression_name)
            slopes.append(slope)
            intercepts.append(intercept)
            slope_errors.append(slope_err)
            intercept_errors.append(intercept_err)

            # Save predictions and residuals
            del_residuals[f'd_{regression_name}{diss}'] = residual
            del_predictions[f'p_{regression_name}{diss}'] = predicted

        # Save regression metadata for this distance flag
        del_mc['name'] = regression_names
        del_mc[f'm{diss}'] = slopes
        del_mc[f'c{diss}'] = intercepts
        del_mc[f'me{diss}'] = slope_errors
        del_mc[f'ce{diss}'] = intercept_errors
    return del_residuals, del_predictions, del_mc

def residue_analysis(residue_file, dis_flag:list, cols:list , save=1):
    # Initialize result containers
    dmc_S, dmc_M = [], []
    dres_S = pd.DataFrame({'name': residue_file['name'], 'logP': residue_file['logP'], 'EBV': residue_file['logP']})
    dpre_S = dres_S.copy()
    dres_M = dres_S.copy()
    dpre_M = dres_S.copy()
    for col in cols:
        # Madore method
        res_M, pre_M, mc_M = residue_correlation(residue_file, dis_flag, col, '_M')
        dres_M = pd.merge(dres_M, res_M, on='name')
        dpre_M = pd.merge(dpre_M, pre_M, on='name')
        dmc_M.append(mc_M)
        # Shubham method
        res_S, pre_S, mc_S = residue_correlation(residue_file, dis_flag, col, '_S')
        dres_S = pd.merge(dres_S, res_S, on='name')
        dpre_S = pd.merge(dpre_S, pre_S, on='name')
        dmc_S.append(mc_S)
    # Combine regression dataframes
    del_mc_M = pd.concat(dmc_M, ignore_index=True).drop_duplicates().set_index('name').T
    del_mc_S = pd.concat(dmc_S, ignore_index=True).drop_duplicates().set_index('name').T
    total_relations = len(mag) * len(dmc_S)  # 6 distance flags per color
    print(f'For each method, there will be {total_relations} relations ({len(mag)} bands × {len(cols)} colors, minus duplicates).')
    # Optional: Save to CSV
    if save == 1:
        cepheid_count = len(residue_file)
        out_base = f"{out_dir}{process_step[2]}{cepheid_count}_"
        del_mc_S.to_csv(f'{out_base}del_slope_intercept_S.csv')
        dres_S.to_csv(f'{out_base}del_res_S.csv')
        dpre_S.to_csv(f'{out_base}del_pre_S.csv')
        del_mc_M.to_csv(f'{out_base}del_slope_intercept_M.csv')
        dres_M.to_csv(f'{out_base}del_res_M.csv')
        dpre_M.to_csv(f'{out_base}del_pre_M.csv')
    return dres_S, dpre_S, del_mc_S, dres_M, dpre_M, del_mc_M

