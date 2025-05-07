### File: ./lvtlaw/e_error_estimation.py
from lvtlaw.a_utils import colors,data_dir, input_data_file, data_out, R, mag, dis_flag, dis_list, process_step, del_mu
import pandas as pd
from lvtlaw.b_data_transform import transformation, extinction_law
from lvtlaw.c_pl_pw import pl_reg     

def select_regression_parameters(dSM, dis): 
    # dSM = [[dmc_S,  dmc_M],[dres_S, dres_M]]
    # separate parameters for Madore's and Shubham's approach
    if dis == '_i':
        m_S, c_S = dSM[0][0].iloc[4].T, dSM[0][0].iloc[5].T
        m_M, c_M = dSM[0][1].iloc[4].T, dSM[0][1].iloc[5].T
    else:
        m_S, c_S = dSM[0][0].iloc[0].T, dSM[0][0].iloc[1].T
        m_M, c_M = dSM[0][1].iloc[0].T, dSM[0][1].iloc[1].T
    return m_S, c_S, m_M, c_M

def run_mu_for_reddening(ex0, r, slope, intercept):  # later called by error_over_mu()
    # for given star, estimate reddening for different mu
    mu_run = pd.DataFrame() 
    for mu in del_mu: # 
        mu_run[f'ex_{mu}'] = ex0 + mu * (1 - slope) - intercept
        mu_run[f'rd_{mu}'] = mu_run[f'ex_{mu}'] / r
    return mu_run

def error_over_mu(i, col, dis, flag, wm_str, slope, intercept, dres, s): # later called by process_reddening()
    r = R[i] / (R[0] - R[1])  # reddening ratio with respect to B-V
    ext0 = dres[f'd_{wm_str}{dis}'] # extinction error without changing modulus
    red0 = ext0 / r  # Convert extinction to reddening E(B-V)
    mu_run = run_mu_for_reddening(ext0, r, slope, intercept)
    if s == 1:
        mu_run.to_csv(f'{data_out}{process_step[4]}{len(mu_run)}{dis}{wm_str}{flag}.csv', index=False)
    return ext0, red0, mu_run

def process_reddening(col, dis, flag, slope, intercept, dres, s):# later called by reddening_error()
    wes_mu = []
    ext0_df, red0_df = pd.DataFrame(), pd.DataFrame()
    for i, band in enumerate(mag):
        if flag == '_M':
            wm_str = f"{band}{col[0]}{col}" 
        else: 
            wm_str = f"{band}{band}{col}"
        slope_ = slope[wm_str]
        intercept_ = intercept[wm_str]
        ext0, red0, mu_run = error_over_mu(i, col, dis, flag, wm_str, slope_, intercept_, dres, s)        
        ext0_df[f'{wm_str}{dis}'] = ext0
        red0_df[f'{wm_str}{dis}'] = red0
        wes_mu.append(mu_run)
    return wes_mu, ext0_df, red0_df

def save_results(ext0S, ext0M, red0S, red0M):
    ext0S.to_csv(f'{data_out}{process_step[3]}{len(ext0S)}_ext_err0_S.csv', index=False)
    ext0M.to_csv(f'{data_out}{process_step[3]}{len(ext0M)}_ext_err0_M.csv', index=False)
    red0S.to_csv(f'{data_out}{process_step[3]}{len(red0S)}_red_err0_S.csv', index=False)
    red0M.to_csv(f'{data_out}{process_step[3]}{len(red0M)}_red_err0_M.csv', index=False)

def reddening_error(wes_cols, dis_flags, dSM, save=1):
    #Estimate reddening errors (mu_0 uncertainties) for both Shubham and Madore approaches.
    ex_rd_mu = []
    for dis in dis_flags:
        # Select regression slopes and intercepts based on distance flag
        m_S, c_S, m_M, c_M = select_regression_parameters(dSM, dis)
        print(f'\nDistance: {dis}\nWesenheit colors:')
        dis_mu_dict = {}
        for col in wes_cols:
            print(f'  → Processing {col}')
            # Madore approach
            wes_mu_M, ext0M_df, red0M_df = process_reddening(col, dis, '_M', m_M, c_M, dSM[1][1], save)       
            # Shubham approach
            wes_mu_S, ext0S_df, red0S_df = process_reddening(col, dis, '_S', m_S, c_S, dSM[1][0], save)
            # Store uncertainty arrays
            dis_mu_dict[f'{col}_M'] = wes_mu_M
            dis_mu_dict[f'{col}_S'] = wes_mu_S
        ex_rd_mu.append(dis_mu_dict)    # []{}[]
    # Output results
    red_SM = [red0S_df, red0M_df]
    if save == 1:
        save_results(ext0S_df, ext0M_df, red0S_df, red0M_df)
    return red_SM, ex_rd_mu




