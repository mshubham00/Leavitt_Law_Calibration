### File: ./lvtlaw/e_error_estimation.py
'''
This file estimates the variation in reddening error with respect to expected distance modulus error trails. 

The output will be saved in 'data/{DatasetName_Rv}/4_reddening/*.csv'

Function contained:
    save_results(): To save the DataFrame as *.csv file.
    select_regression_parameters(dSM, dis): Retrieve slope and intercept from d_del_del.residue_analysis dSM as per color and method.
        Output: m, c
    run_mu_for_reddening(del_mu): estimates reddening error for distance error possibilities. 
        Output: mu_rd_ex_df
    error_over_mu(): saves DataFrame mu_rd_ex_df
        Output: ext0_list, red0_list, mu_rd_ex_df
    process_reddening(col, dis, flag): 
        Output: mu_df_list, ext0_df, red0_df
    reddening_error(): Executes above for different colors, distance and flag
        Output: red0_df_list, mu_df_list_dict
'''

from lvtlaw.a_utils import colors,data_dir, input_data_file, data_out, R, mag, dis_flag, dis_list, process_step, del_mu
import pandas as pd
from lvtlaw.b_data_transform import transformation, extinction_law
from lvtlaw.c_pl_pw import pl_reg     

def save_results(ext0, red0, col, flag, dis):
    ext0.to_csv(f'{data_out}{process_step[3]}{len(ext0)}_ext_err0_{col}_{flag}{dis}.csv', index=False)
    red0.to_csv(f'{data_out}{process_step[3]}{len(red0)}_red_err0_{col}_{flag}{dis}.csv', index=False)

def select_regression_parameters(dSM, dis): 
    if dis == '_i':
        m, c = dSM[0][0].iloc[4].T, dSM[0][0].iloc[5].T
    else:
        m, c = dSM[0][0].iloc[0].T, dSM[0][0].iloc[1].T
    return m, c

def run_mu_for_reddening(ex0, r, slope, intercept,dis):  # later called by error_over_mu()
    # for given star, estimate reddening for different mu
    mu_rd_ex_df = pd.DataFrame() 
    for mu in del_mu: #  
        mu_rd_ex_df[f'ex_{mu}{dis}'] = ex0 + mu * (1 - slope) - intercept
        mu_rd_ex_df[f'rd_{mu}{dis}'] = mu_rd_ex_df[f'ex_{mu}{dis}'] / r
    return mu_rd_ex_df

def error_over_mu(i, dis, wm_str, slope, intercept, dres, s): # later called by process_reddening()
#    r = R[i] / (R[mag.index(col[0])] - R[mag.index(col[1])])  # reddening ratio
    r = R[i] / (R[0] - R[1])  # reddening ratio
    ext0_list = dres[f'd_{wm_str}{dis}'] # extinction error without changing modulus
    red0_list = ext0_list / r  # Convert extinction to reddening E(B-V)
    mu_rd_ex_df = run_mu_for_reddening(ext0_list, r, slope, intercept,dis)
    if s == 1:
        mu_rd_ex_df.to_csv(f'{data_out}{process_step[4]}{len(mu_rd_ex_df)}{dis}{wm_str}.csv', index=False)
    return ext0_list, red0_list, mu_rd_ex_df

def process_reddening(col, dis, slope, intercept, dres, flag, s):# later called by reddening_error()
    mu_df_list = []
    ext0_df, red0_df = pd.DataFrame(), pd.DataFrame()
    for i, band in enumerate(mag):
        wm_str = f"{band}{band}{col}" if flag == "S" else f"{band}{col[0]}{col}"
        slope_ = slope[wm_str]
        intercept_ = intercept[wm_str]
        ext0_list, red0_list, mu_rd_ex_df = error_over_mu(i, dis, wm_str, slope_, intercept_, dres, s)        
        ext0_df[f'{wm_str}{dis}'] = ext0_list
        red0_df[f'{wm_str}{dis}'] = red0_list
        mu_df_list.append(mu_rd_ex_df)
    if s == 1:
        save_results(ext0_df, red0_df, col, flag, dis)
    return mu_df_list, ext0_df, red0_df

def reddening_error(wes_cols, dis_flag, dSM, flags, s=1):
    #Estimate reddening errors (mu_0 uncertainties) for both Shubham and Madore approaches.
    red0_df_list = []        # 4 col x 2 flags in list of red0_df
    mu_df_list_dict = {}     # 4 col x 2 flags in dict of list of mu_rd_df
    for dis in dis_flag: 
        m, c = select_regression_parameters(dSM, dis)
        print(f'\nDistance: {dis}\nWesenheit colors:')
        for flag in flags:
            for col in wes_cols:   
                print(f'  → Processing {col} for {flag}') #
                mu_df_list, ext0_df, red0_df = process_reddening(col, dis, m, c, dSM[1][0], flag, s)
                mu_df_list_dict[f'{col}_{flag}{dis}'] = mu_df_list
                red0_df_list.append(red0_df)    
    return red0_df_list, mu_df_list_dict
