### File: ./lvtlaw/d_del_del.py
from lvtlaw.a_utils import A, R, mag, abs_bands, ap_bands, colors, data_dir, input_data_file, data_out, regression, dis_flag, process_step
import pandas as pd
from functools import reduce
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
bands = abs_bands
out_dir = data_out

def residue_correlation(residue_file, dis_flag, col): 
    del_mc = pd.DataFrame()         # Stores regression results
    del_predictions = pd.DataFrame({'name': residue_file['name']})  # Star-by-star predictions
    del_residuals = pd.DataFrame({'name': residue_file['name']})    # Star-by-star residuals
    print('\tColor:', col)
    for diss in dis_flag:
        slopes, intercepts = [], []
        slope_errors, intercept_errors = [], []
        regression_names = []
        for band in mag:
            wesenheit = f"{band}{col}"
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
    dmc = []
    dres = pd.DataFrame({'name': residue_file['name'], 'logP': residue_file['logP'], 'EBV': residue_file['logP']})
    dpre = dres.copy()
    for col in cols:
        res, pre, mc = residue_correlation(residue_file, dis_flag, col)
        dres = pd.merge(dres, res, on='name')
        dpre = pd.merge(dpre, pre, on='name')
        dmc.append(mc)
    # Combine regression dataframes
    del_mc = pd.concat(dmc, ignore_index=True).drop_duplicates().set_index('name').T
    total_relations = len(mag) * len(dmc)  # 6 distance flags per color
    # Optional: Save to CSV
    if save == 1:
        cepheid_count = len(residue_file)
        out_base = f"{out_dir}{process_step[2]}{cepheid_count}_"
        del_mc.to_csv(f'{out_base}del_slope_intercept.csv')
        dres.to_csv(f'{out_base}del_res.csv')
        dpre.to_csv(f'{out_base}del_pre.csv')
    return dres, dpre, del_mc

