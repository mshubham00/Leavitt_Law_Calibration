### File: ./lvtlaw/e_error_estimation.py
'''
This file estimates the variation in reddening error with respect to expected distance modulus error trails. 

The output will be saved in 'data/{DatasetName_Rv}/4_reddening/*.csv'

Function contained:
    select_regression_parameters(dSM, dis): Retrieve slope and intercept from d_del_del.residue_analysis dSM as per color and method.
        Output: m, c
    error_over_mu(): Estimates reddening error for distance error possibilities, saves DataFrame mu_rd_ex_df
        Output: ext0_list, red0_list, mu_rd_ex_df
    process_reddening(col, dis, flag): 
        Output: mu_df_list, ext0_df, red0_df
    reddening_error(): Executes above for different colors, distance and flag
        Output: red0_df_list, mu_df_list_dict
'''
module = 'e_error_estimation'
#from lvtlaw.a_utils import A, R, mag, abs_bands, ap_bands, colors, data_dir, data_out, regression, dis_flag, process_step, wes_show, merge_12
from data.datamapping import file_name, data_cols, dis_list, dis_flag, R, mag, wes_show, flags,s, plots,z, mode
from data.datamapping import colors,data_dir, data_out, process_step, del_mu
import pandas as pd
from lvtlaw.a_utils import merge_12
from lvtlaw.b_data_transform import transformation, extinction_law
from lvtlaw.c_pl_pw import pl_reg     

def select_regression_parameters(dmc, dis): 
    if dis == '_i':
        m, c = dmc.iloc[4].T, dmc.iloc[5].T
    else:
        m, c = dmc.iloc[0].T, dmc.iloc[1].T
    return m, c #lists


def error_over_mu(dres, m, ab, dis, col, wm_str, slope, intercept, s=s): # called by process_reddening()
    r = R[mag[m]] / (R[col[0]] - R[col[1]])  # reddening ratio
    ext0_list = dres[f'd_{wm_str}{dis}'] # extinction error without changing modulus from d_residue_analysis()
    red0_list = ext0_list / r  # Convert extinction to reddening E(B-V)
    mu_rd_ex_df = pd.DataFrame({'name': dres['name'], 'logP': dres['logP']})
    for mu in del_mu: #  
        mu_rd_ex_df[f'ex{ab}_{col}{mu}{dis}'] = ext0_list + mu * (1 - slope) - intercept
        mu_rd_ex_df[f'rd{ab}_{col}{mu}{dis}'] = mu_rd_ex_df[f'ex{ab}_{col}{mu}{dis}'] / r
    if s == 1:
        mu_rd_ex_df.to_csv(f'{data_out}{process_step[4]}{len(mu_rd_ex_df)}_mu_rd_ex{dis}{wm_str}.csv', index=False)
    return ext0_list, red0_list, mu_rd_ex_df

def process_reddening(dres, col, dis, slope, intercept, flag):# later called by reddening_error()
    mu_df_list, ext0_df = [], pd.DataFrame({'name': dres['name']})
    red0_df = ext0_df.copy()
    for ab in mode:
        print(f'  → Processing {col} {ab} for {flag}') #
        for m, band in enumerate(mag):
            wm_str = f"{band}{ab}{band}{col}" if flag == "S" else f"{band}{ab}{col[0]}{col}"
            slope_ = slope[wm_str]
            intercept_ = intercept[wm_str]
            ext0_list, red0_list, mu_rd_ex_df = error_over_mu(dres, m, ab, dis, col, wm_str, slope_, intercept_)        
            ext0_df[f'ex_{wm_str}{dis}'] = ext0_list
            red0_df[f'rd_{wm_str}{dis}'] = red0_list
            if ab == '' or len(mode)==1:
                df = mu_rd_ex_df
            else:
                mu_rd_ex_df = merge_12(df, mu_rd_ex_df, ['name', 'logP'])
                mu_df_list.append(mu_rd_ex_df)
    return mu_df_list, ext0_df, red0_df                                           

def error_reddening(dres, dmc, del_mu=del_mu,z=z, wes_show=wes_show, dis_flag = dis_flag, plots=plots, flags = flags, s=s):
    mu_df_list_dict = {}     # 4 col x 2 flags in dict of list of mu_rd_df
    ex_df = pd.DataFrame({'name': dres['name'], 'logP': dres['logP']})
    rd_df = ex_df.copy()
    for dis in dis_flag: 
        m, c = select_regression_parameters(dmc, dis) #lists of del-del slope and intercept 
        print(f'\nDistance: {dis}\nWesenheit colors:')
        for flag in flags:
            for col in wes_show:   
                mu_df_list, ext0_df, red0_df = process_reddening(dres, col, dis, m, c, flag)
                mu_df_list_dict[f'{col}_{flag}{dis}'] = mu_df_list
                ex_df = pd.merge(ex_df, ext0_df[[cl for cl in ext0_df.columns if cl not in ex_df.columns or cl == 'name']], on='name')
                rd_df = pd.merge(rd_df, red0_df[[cl for cl in red0_df.columns if cl not in rd_df.columns or cl == 'name']], on='name')
    if s == 1:
        ex_df.to_csv(f'{data_out}{process_step[3]}{len(ex_df)}_ext_err0.csv', index=False)
        rd_df.to_csv(f'{data_out}{process_step[3]}{len(rd_df)}_red_err0.csv', index=False)
    return ex_df,rd_df, mu_df_list_dict
    
print(f'* * {module} module loaded!')
