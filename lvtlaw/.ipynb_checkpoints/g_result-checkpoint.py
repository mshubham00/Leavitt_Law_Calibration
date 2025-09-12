### File: ./lvtlaw/f_star_wise.py
'''
This file 

The output will be saved in 'data/{DatasetName_Rv}/1_prepared/*.csv'

Function contained:

'''

from lvtlaw.a_utils import process_step, colors, mag, ap_bands, abs_bands, data_dir, data_out, dis_flag, dis_list, s, data_out, wes_show, del_mu, regression, R, nreg, flags
import pandas as pd

def get_error_pair(star, flags = flags, wes_show = wes_show, del_mu = del_mu):
    # star: dataframe containing star                 
    mu_rd_var = {}    # 
#    print(star)
    for d in dis_flag:   
        for f in flags: 
            for col in wes_show: 
                var_cols = [f'{f}{col}{d}rd_{mu}' for mu in del_mu] # column names
                var_vals = pd.to_numeric(star.loc['var', var_cols], errors='coerce') # collect all variation
                min_var_idx = var_vals.idxmin() # find minimum variance index name
                min_mu = float(min_var_idx[8:])  # collect mu of minimum vairance
                mean_rd = float(star.loc['mean', min_var_idx]) #               
                mu_rd_var[f'var{f}{col}{d}'] = var_vals.min()
                mu_rd_var[f'mu{f}{col}{d}'] = min_mu
                mu_rd_var[f'rd{f}{col}{d}'] = mean_rd
    return mu_rd_var

def correction_rd_mu(stars, raw, s=1):
    stars_correction = []
    for i in range(len(stars)):
        mu_rd_var = get_error_pair(stars[i])
        stars_correction.append(mu_rd_var)
    correction_red_mu_stars = pd.DataFrame(stars_correction)
    correction_red_mu_stars['name'] = raw.name
    
    if s==1:
        correction_red_mu_stars.to_csv('%s%i_error_rms_mu_rd.csv'%(data_out+process_step[6],len(stars)))
    return correction_red_mu_stars    

def correction_apply(tabsolute, correction, flags, s=1):
    corrected = pd.DataFrame()
    corrected['logP'] = tabsolute['logP'] 
    for d in dis_flag:
        for f in flags:
            for col in wes_show:
                corrected['mu'+f+col+d] = tabsolute[dis_list[dis_flag.index(d)]]-correction['mu'+f+col+d]
                corrected['EBV'+f+col+d]  = tabsolute['EBV']- correction['rd'+f+col+d]
                for i in range(len(mag)):
                    ex = R[i]*correction['rd'+f+col+d]
                    corrected[mag[i]+f+col+d]=tabsolute['M_'+mag[i]+'0'+d] + correction['mu'+f+col+d] -ex
    if s==1:
        corrected.to_csv('%s%i_corrected.csv'%(data_out+process_step[7],len(corrected)))
    return corrected

def append_PLW(PLW_struct : list,i : int,a : float,b : float,c : list,d : list,e :float,f :float, flag, dis):
    # collect different regression output into one structure
    PLW_struct[0].append(i)    # PL_name
    PLW_struct[1].append(a)    # slope
    PLW_struct[2].append(b)    # intercept
    PLW_struct[3]['p_'+i+flag+dis] = c   # PL prediction
    PLW_struct[4]['r_'+i+flag+dis] = d   # PL residue
    PLW_struct[5].append(e)    # slope error
    PLW_struct[6].append(f)    # intercept error
    return PLW_struct


def corrected_PL(tabsolute, corrected, dis, flag, s=1):
    PL_name, PL_slope, PL_intercept = [], [], []
    err_slope, err_intercept = [], []
    residue = pd.DataFrame({'name': tabsolute['name'], 'logP': tabsolute['logP'], 'EBV': tabsolute['EBV']})
    prediction = residue.copy()   
    # Store regression results
    PLW_struct = [PL_name, PL_slope, PL_intercept, prediction, residue, err_slope, err_intercept]    
    for col in wes_show:
        print('\t Color: ', col, '\t Method: ', flag)
        for i in range(len(mag)):
            regression(tabsolute['logP']-1, tabsolute['M_'+mag[i]+'0'+dis], '(logP - 1)', 'M__'+mag[i], 1)
            a,b,c,d,e,f = regression(corrected['logP']-1,corrected[mag[i]+flag+col+dis], '(logP - 1)', 'M%s_%s'%(flag,mag[i]), p = s)
            PLW_struct = append_PLW(PLW_struct, mag[i] + col, a, b, c, d, e, f, flag, dis)
    PLW = pd.DataFrame({
        'name': PLW_struct[0],
        f'm': PLW_struct[1],
        f'c': PLW_struct[2],
        f'err_m': PLW_struct[5],
        f'err_c': PLW_struct[6]
    })
    prediction = PLW_struct[3]
    residue = PLW_struct[4]
    return PLW, residue, prediction        

def corrected_reg(tabsolute, corrected, dis, flags, s=1):
    reg = pd.DataFrame()
    res = pd.DataFrame()
    pre = pd.DataFrame()
    for f in flags:
        PLW, residue, prediction = corrected_PL(tabsolute, corrected, dis, f, s)
        reg = pd.concat([reg, PLW], axis=1)
        res = pd.concat([res, residue], axis=1)
        pre = pd.concat([pre, prediction], axis=1)
    res = res.loc[:, ~res.columns.duplicated()]
    # Transpose regression DataFrame, and use the first row as column names
    reg = reg.T
    reg.columns = reg.iloc[0]
    reg = reg.drop(reg.index[0])
    if s==1:
        res.to_csv('%s%i_result_residue.csv'%(data_out+process_step[7],len(res)))
        pre.to_csv('%s%i_result_prediction.csv'%(data_out+process_step[7],len(pre)))
        reg.to_csv('./%s%i_%i_result_regression.csv'%(data_out+process_step[7],len(res),nreg))
    return reg, res, pre 
        
'''
    if s==2:
        res.to_csv('%s%i_residue.csv'%(data_out+process_step[7],len(res)))
        pre.to_csv('%s%i_prediction.csv'%(data_out+process_step[7],len(pre)))
        reg.to_csv('./%s%i_regression.csv'%(data_out+process_step[7],len(reg)))    

'''
