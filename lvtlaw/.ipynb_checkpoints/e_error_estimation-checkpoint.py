### File: ./lvtlaw/e_error_estimation.py
from lvtlaw.a_utils import colors,data_dir, input_data_file, data_out, R, mag, dis_flag, dis_list, process_step, del_mu
import pandas as pd
from lvtlaw.b_data_transform import transformation, extinction_law
from lvtlaw.c_pl_pw import pl_reg     

def select_regression_parameters(dSM, dis): 
    if dis == '_i':
        m, c = dSM[0][0].iloc[4].T, dSM[0][0].iloc[5].T
    else:
        m, c = dSM[0][0].iloc[0].T, dSM[0][0].iloc[1].T
    return m, c

def run_mu_for_reddening(ex0, r, slope, intercept):  # later called by error_over_mu()
    # for given star, estimate reddening for different mu
    mu_run = pd.DataFrame() 
    for mu in del_mu: #  
        mu_run[f'ex_{mu}'] = ex0 + mu * (1 - slope) - intercept
        mu_run[f'rd_{mu}'] = mu_run[f'ex_{mu}'] / r
    return mu_run

def error_over_mu(i, col, dis, wm_str, slope, intercept, dres, s): # later called by process_reddening()
    r = R[i] / (R[0] - R[1])  # reddening ratio with respect to B-V
    ext0 = dres[f'd_{wm_str}{dis}'] # extinction error without changing modulus
    red0 = ext0 / r  # Convert extinction to reddening E(B-V)
    mu_run = run_mu_for_reddening(ext0, r, slope, intercept)
    if s == 1:
        mu_run.to_csv(f'{data_out}{process_step[4]}{len(mu_run)}{dis}{wm_str}.csv', index=False)
    return ext0, red0, mu_run

def process_reddening(col, dis, slope, intercept, dres, s):# later called by reddening_error()
    wes_mu = []
    ext0_df, red0_df = pd.DataFrame(), pd.DataFrame()
    for i, band in enumerate(mag):
        wm_str = f"{band}{col}" if flag == "S" else f"{col[0]}{col}"
        slope_ = slope[wm_str]
        intercept_ = intercept[wm_str]
        ext0, red0, mu_run = error_over_mu(i, col, dis, wm_str, slope_, intercept_, dres, s)        
        ext0_df[f'{wm_str}{dis}'] = ext0
        red0_df[f'{wm_str}{dis}'] = red0
        wes_mu.append(mu_run)
    return wes_mu, ext0_df, red0_df

def save_results(ext0, red0):
    ext0.to_csv(f'{data_out}{process_step[3]}{len(ext0)}_ext_err0.csv', index=False)
    red0.to_csv(f'{data_out}{process_step[3]}{len(red0)}_red_err0.csv', index=False)

def reddening_error(wes_cols, dis_flags, dSM, s=1):
    #Estimate reddening errors (mu_0 uncertainties) for both Shubham and Madore approaches.
    ex_rd_mu = []
    for dis in dis_flags:
        # Select regression slopes and intercepts based on distance flag
        m, c = select_regression_parameters(dSM, dis)
        print(f'\nDistance: {dis}\nWesenheit colors:')
        dis_mu_dict = {}
        for col in wes_cols:
            print(f'  → Processing {col}')
            wes_mu, ext0_df, red0_df = process_reddening(col, dis, m, c, dSM[1][0], s)
            dis_mu_dict[f'{col}'] = wes_mu
        ex_rd_mu.append(dis_mu_dict)    # []{}[]
    # Output results
    red_SM = [red0_df]
    if save == 1:
        save_results(ext0_df, red0_df)
    return red_SM, ex_rd_mu
