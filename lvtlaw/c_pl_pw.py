### File: ./lvtlaw/c_pl_pw.py
from lvtlaw.a_utils import process_step, regression, colors, mag, ap_bands, abs_bands, data_dir, input_data_file, data_out, dis_flag, dis_list, s, wes_show, nreg

import pandas as pd, numpy as np
from functools import reduce
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

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

def pl_dis(data, dis: str, bands: list):
    # Initialize the structure for storing results
    PL_name, PL_slope, PL_intercept = [], [], []
    err_slope, err_intercept = [], []
    residue = pd.DataFrame({'name': data['name'], 'logP': data['logP']})
    prediction = residue.copy()   
    # Store regression results
    PLW_struct = [PL_name, PL_slope, PL_intercept, prediction, residue, err_slope, err_intercept]    
    print('Absolute Magnitude \n#######  m - mu = alpha (logP - 1) + gamma     #################')
    for i in range(len(mag)):  # Iterate over magnitudes
        a, b, c, d, e, f = regression(data['logP'] - 1, data[bands[i] + dis], '(logP - 1)', bands[i] + dis, 1)
        PLW_struct = append_PLW(PLW_struct, mag[i], a, b, c, d, e, f, dis)
    
    print('True Absolute Magnitude \n#######  m - mu - R*E(B-V) = alpha (logP - 1) + gamma     #####')
    for i in range(len(mag)):  # True absolute magnitudes
        a, b, c, d, e, f = regression(data['logP'] - 1, data[bands[i] + '0' + dis], '(logP -1)', bands[i] + '0' + dis, 1)
        PLW_struct = append_PLW(PLW_struct, mag[i] + '0', a, b, c, d, e, f, dis)
    
    for color in wes_show:
        print(f'Wesenheit Magnitude for color index: {color} \n#######  m - mu - R*({color}) = alpha (logP - 1) + gamma     #####')
        for i in range(len(mag)):
            a, b, c, d, e, f = regression(data['logP'] - 1, data[mag[i] + color + dis], '(logP - 1)', mag[i] + color + dis, 1)
            PLW_struct = append_PLW(PLW_struct, mag[i] + color, a, b, c, d, e, f, dis)
    
    # Convert the results into a DataFrame
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

def pl_reg(data, s=1, dis_flag: list = dis_flag, bands = abs_bands):
    reg = pd.DataFrame()
    res = pd.DataFrame()
    pre = pd.DataFrame()
    for dis in dis_flag:
        PLW, residue, prediction = pl_dis(data, dis, bands)
        reg = pd.concat([reg, PLW], axis=1)
        res = pd.concat([res, residue], axis=1)
        pre = pd.concat([pre, prediction], axis=1)
    res = res.loc[:, ~res.columns.duplicated()]
    # Transpose regression DataFrame, and use the first row as column names
    reg = reg.T
    reg.columns = reg.iloc[0]
    reg = reg.drop(reg.index[0])
    if s==1:
        res.to_csv('%s%i_residue.csv'%(data_out+process_step[1],len(res)))
        pre.to_csv('%s%i_prediction.csv'%(data_out+process_step[1],len(pre)))
        reg.to_csv('./%s%i_%i_regression.csv'%(data_out+process_step[1],len(res),nreg))
    return reg, res, pre
####################################################################################
