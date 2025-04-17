### File: ./lvtlaw/c_pl_pw.py
from lvtlaw.a_utils import process_step, regression, colors, mag, ap_bands, abs_bands, data_dir, input_data_file, data_out, dis_flag, dis_list, s, wes_show

import pandas as pd
import numpy as np
from functools import reduce
    # regression(x,y,x_str,y_str,print_flag) -> slope, intercept, prediction, residue, err_slope, err_intercept
    # color_index -> list of all permutation of band filters
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)


def append_PLW(PLW_struct,i,a,b,c,d,e,f,dis):
    PLW_struct[0].append(i)
    PLW_struct[1].append(a)
    PLW_struct[2].append(b)
    PLW_struct[3]['p_'+i+dis] = c   
    PLW_struct[4]['r_'+i+dis] = d
    PLW_struct[5].append(e)
    PLW_struct[6].append(f)
    return PLW_struct

def pl_dis(data, dis, bands):
    PL_name=[]
    PL_slope = []             # Gaia based slope of period luminosity relation 
    PL_intercept = []
    err_slope = []
    err_intercept = []
    PLW_struct = [PL_name, PL_slope, PL_intercept, prediction,residue, err_slope, err_intercept]
    residue = pd.DataFrame()
    prediction = pd.DataFrame()
    prediction['name'] =  residue['name'] = data['name']
    prediction['logP'] =  residue['logP'] = data['logP']
    prediction['EBV'] =  residue['EBV'] = data['EBV']
    prediction['%s'%(dis_list[dis_flag.index(dis)])] =  residue['%s'%(dis_list[dis_flag.index(dis)])] = data['%s'%(dis_list[dis_flag.index(dis)])]
    print('Absolute Magnitude \n', '#######  m - mu   =   alpha (logP - 1) + gamma     #################')
    for i in range(0,len(mag)):    # absolute_mag : M_B_g
        a,b,c,d,e,f = regression(data['logP']-1, data[bands[i]+dis], '(logP - 1)', bands[i]+dis, 1)
        PLW_struct = append_PLW(PLW_struct, mag[i], a,b,c,d,e,f,dis)
    print('True Absolute Magnitude \n ', '#######  m - mu - R*E(B-V)  =   alpha (logP - 1) + gamma     #####')
    for i in range(0,len(mag)):    # true_ absolute_mag : M_B0_g
        a,b,c,d,e,f = regression(data['logP']-1, data[bands[i]+'0'+dis], '(logP -1)', bands[i]+'0'+dis, 1)
        PLW_struct = append_PLW(PLW_struct, mag[i]+'0', a,b,c,d,e,f, dis)
    for color in wes_show:
        print('Wesenheit Magnitude for color index: \n #######  m - mu - R*(',color,')  =   alpha (logP - 1) + gamma     #####')   # wesenheit magnitude: BVK_g
        for i in range(0,len(mag)):
            a,b,c,d,e,f = regression(data['logP']-1, data[mag[i]+color+dis], '(logP -1)', mag[i]+color+dis,1)
            PLW_struct = append_PLW(PLW_struct, mag[i]+color, a,b,c,d,e,f, dis)
    PLW = pd.DataFrame(
        {'name': PLW_struct[0],
        'm%s'%(dis): PLW_struct[1],
        'c%s'%(dis):  PLW_struct[2],
        'err_m%s'%(dis):  PLW_struct[5],
        'err_c%s'%(dis): PLW_struct[6],
        })
    prediction = PLW_struct[3]     
    residue = PLW_struct[4]
    return PLW, residue, prediction

def pl_reg(data, s=1, dis_flag = dis_flag, bands = abs_bands):
    reg = pd.DataFrame()
    res = pd.DataFrame()
    pre = pd.DataFrame()
    for dis in dis_flag:
        PLW, residue, prediction = pl_dis(data, dis, bands)
        reg = pd.concat([reg, PLW], axis=1)
        #reg.append(PLW)
        res = pd.concat([res, residue], axis=1)
        pre = pd.concat([pre, prediction], axis=1)
        #res.append(residue)
        #pre.append(prediction)
    res = res.loc[:, ~res.columns.duplicated()]
    reg = reg.T
    reg.columns = reg.iloc[0]
    reg = reg.drop(reg.index[0])
    if s==1:
        res.to_csv('%s%i_residue.csv'%(data_out+process_step[1],len(res)))
        pre.to_csv('%s%i_prediction.csv'%(data_out+process_step[1],len(pre)))
        reg.to_csv('./%s%i_regression.csv'%(data_out+process_step[1],len(reg)))
    return reg, res, pre

####################################################################################
    
