from lvtlaw.a_utils import process_step, colors, mag, ap_bands, abs_bands, data_dir, input_data_file, data_out, dis_flag, dis_list, s, data_out, wes_show, del_mu, regression, R, nreg
import pandas as pd

def get_error_pair(star):
    # star: dataframe containing star                 
    mu_rd_var = {}    # 
    for d in dis_flag: 
        for col in wes_show: 
            var_cols = [f'{col}{d}rd{mu}' for mu in del_mu]
            var_vals = pd.to_numeric(star.loc['var', var_cols], errors='coerce')
            min_var_idx = var_vals.idxmin()
            min_mu = float(min_var_idx[6:])  # collect mu
            mean_rd = float(star.loc['mean', min_var_idx])                
            mu_rd_var[f'var{d}{col}'] = var_vals.min()
            mu_rd_var[f'mu{d}{col}'] = min_mu
            mu_rd_var[f'rd{d}{col}'] = mean_rd
    return mu_rd_var

def correction_rd_mu(stars, save=1):
    stars_correction = [] 
    for i in range(len(stars)):
        mu_rd_var = get_error_pair(stars[i])
        stars_correction.append(mu_rd_var)
    correction_red_mu_stars = pd.DataFrame(stars_correction)
    if save==1:
        correction_red_mu_stars.to_csv('%s%i_error_rms_mu_rd.csv'%(data_out+process_step[6],len(stars)))
    return correction_red_mu_stars    

def correction_apply(tabsolute, correction, save=1):
    corrected = pd.DataFrame()
    corrected['logP'] = tabsolute['logP'] 
    for d in dis_flag:
        for col in wes_show:
            corrected['mu'+d+col] = tabsolute[dis_list[dis_flag.index(d)]]+correction['mu'+d+col]
            corrected['EBV'+d+col]  = tabsolute['EBV']+correction['rd'+d+col]
            for i in range(len(mag)):
                ex = -R[i]*correction['rd'+d+col]
                corrected[mag[i]+d+col]=tabsolute['M_'+mag[i]+'0'+d] + ex +correction['mu'+d+col]
    if save==1:
        corrected.to_csv('%s%i_corrected.csv'%(data_out+process_step[7],len(corrected)))
    return corrected

def append_PLW(PLW_struct : list,i : int,a : float,b : float,c : list,d : list,e :float,f :float,dis :str):
    # collect different regression output into one structure
    PLW_struct[0].append(i)
    PLW_struct[1].append(a)
    PLW_struct[2].append(b)
    PLW_struct[3]['p_'+i+dis] = c   
    PLW_struct[4]['r_'+i+dis] = d
    PLW_struct[5].append(e)
    PLW_struct[6].append(f)
    return PLW_struct


def corrected_PL(tabsolute, corrected, dis, s=1):
    PL_name, PL_slope, PL_intercept = [], [], []
    err_slope, err_intercept = [], []
    residue = pd.DataFrame({'name': tabsolute['name'], 'logP': tabsolute['logP'], 'EBV': tabsolute['EBV']})
    prediction = residue.copy()   
    # Store regression results
    PLW_struct = [PL_name, PL_slope, PL_intercept, prediction, residue, err_slope, err_intercept]    

    for col in wes_show:
        print('\t Color: ', col, '\t Distance: ', dis[1])
        for i in range(len(mag)):
            regression(tabsolute['logP']-1, tabsolute['M_'+mag[i]+'0'+dis], '(logP - 1)', 'M__'+mag[i], 1)
            a,b,c,d,e,f = regression(corrected['logP']-1,corrected[mag[i]+dis+col], '(logP - 1)', 'M*_%s'%(mag[i]), p = s)
            PLW_struct = append_PLW(PLW_struct, mag[i] + col, a, b, c, d, e, f, dis)
    PLW = pd.DataFrame({
        'name': PLW_struct[0],
        f'm{dis}': PLW_struct[1],
        f'c{dis}': PLW_struct[2],
        f'err_m{dis}': PLW_struct[5],
        f'err_c{dis}': PLW_struct[6]
    })
    prediction = PLW_struct[3]
    residue = PLW_struct[4]
    return PLW, residue, prediction        

def corrected_reg(tabsolute, corrected, dis_flag, s=1):
    reg = pd.DataFrame()
    res = pd.DataFrame()
    pre = pd.DataFrame()
    for dis in dis_flag:
        PLW, residue, prediction = corrected_PL(tabsolute, corrected, dis, s)
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
