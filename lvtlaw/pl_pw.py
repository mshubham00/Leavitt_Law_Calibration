### File: ./lvtlaw/pl_pw.py

import pandas as pd
import numpy as np
from functools import reduce
from lvtlaw.utils import process_step, regression, color_index, mag, ap_bands, abs_bands, data_dir, data_file, data_out
    # regression(x,y,x_str,y_str,print_flag) -> slope, intercept, prediction, residue, err_slope, err_intercept
    # color_index -> list of all permutation of band filters
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
color_index = color_index()
bands = abs_bands
'''
def regres(d,x,y,x_str,y_str,p):
    PL_name=[]
    PL_slope = []             # Gaia based slope of period luminosity relation 
    PL_intercept = []
    err_slope = []
    err_intercept = []
    residue = pd.DataFrame()
    prediction = pd.DataFrame()
    prediction['name'] =  residue['name'] = data['name']
    for i in range(0,6):    # absolute_mag : M_B_g
        a,b,c,d,e,f = regression(data['logP']-1, data[bands[i]+dis], '(logP - 1)', bands[i]+dis, 1)
        residue['r_'+mag[i]+dis] = d  
        prediction['p_'+mag[i]+dis] = c 
        PL_name.append(mag[i])
        PL_slope.append(a)
        PL_intercept.append(b)
        err_slope.append(e)
        err_intercept.append(f)
    PLW = pd.DataFrame(
        {'name': PL_name,
        'm%s'%(dis): PL_slope,
        'c%s'%(dis): PL_intercept,
        'err_m%s'%(dis): err_slope,
        'err_c%s'%(dis): err_intercept}
    return PLW, residue, prediction


def pl_reg(data, dis, bands = abs_bands):
    for d in dis:
        mc, res, pre = regres(data['logP']-1, data[bands[i]+d], '(logP - 1)', bands[i]+d, 1):
        PLW = pd.merge(PLW, mc, on='name')
'''

def pl_reg(data, disg = '_g', disi='_i', bands = abs_bands):
    PL_name=[]
    PL_slope_g = []             # Gaia based slope of period luminosity relation 
    PL_slope_i  = []            # IRSB based slope of period luminosity relation
    PL_intercept_g = []
    PL_intercept_i = []
    err_slope_g = []
    err_slope_i = []
    err_intercept_g = []
    err_intercept_i = []
    residue = pd.DataFrame()
    prediction = pd.DataFrame()
    prediction['name'] =  residue['name'] = data['name']
    prediction['plx'] =  residue['plx'] = data['plx']
    prediction['EBV'] =  residue['EBV'] = data['EBV']
    for i in range(0,6):    # absolute_mag : M_B_g
        ag,bg,cg,dg,eg,fg = regression(data['logP']-1, data[bands[i]+disg], '(logP - 1)', bands[i]+disg, 1)
        ai,bi,ci,di,ei,fi = regression(data['logP']-1, data[bands[i]+disi], '(logP - 1)', bands[i]+disi, 1)
        residue['r_'+mag[i]+disg] = dg  
        prediction['p_'+mag[i]+disg] = cg 
        residue['r_'+mag[i]+disi] = di  
        prediction['p_'+mag[i]+disi] = ci
        PL_name.append(mag[i])
        PL_slope_g.append(ag)
        PL_intercept_g.append(bg)
        err_slope_g.append(eg)
        err_intercept_g.append(fg)
        PL_slope_i.append(ai)
        PL_intercept_i.append(bi)
        err_slope_i.append(ei)
        err_intercept_i.append(fi)
    for i in range(0,6):    # true_ absolute_mag : M_B0_g
        ag,bg,cg,dg,eg,fg = regression(data['logP']-1, data[bands[i]+'0'+disg], '(logP -1)', bands[i]+'0'+disg, 1)
        ai,bi,ci,di,ei,fi = regression(data['logP']-1, data[bands[i]+'0'+disi], '(logP -1)', bands[i]+'0'+disi, 1)
        residue['r0_'+mag[i]+disg] = dg
        prediction['p0_'+mag[i]+disg] = cg
        residue['r0_'+mag[i]+disi] = di
        prediction['p0_'+mag[i]+disi] = ci
        PL_name.append(mag[i]+'0')
        PL_slope_g.append(ag)
        PL_intercept_g.append(bg)
        err_slope_g.append(eg)
        err_intercept_g.append(fg)
        PL_slope_i.append(ai)
        PL_intercept_i.append(bi)
        err_slope_i.append(ei)
        err_intercept_i.append(fi)
    for color in color_index:   # wesenheit magnitude: BVK_g
        for i in range(0,6):
            ag,bg,cg,dg,eg,fg = regression(data['logP']-1, data[mag[i]+color+disg], '(logP -1)', mag[i]+color+disg,1)
            ai,bi,ci,di,ei,fi = regression(data['logP']-1, data[mag[i]+color+disi], '(logP -1)', mag[i]+color+disi,1)
            residue['r_'+mag[i]+color+disg] = dg
            prediction['p_'+mag[i]+color+disg] = cg
            residue['r_'+mag[i]+color+disi] = di
            prediction['p_'+mag[i]+color+disi] = ci
            PL_name.append(mag[i]+color)
            PL_slope_g.append(ag)
            PL_intercept_g.append(bg)
            err_slope_g.append(eg)
            err_intercept_g.append(fg)
            PL_slope_i.append(ai)
            PL_intercept_i.append(bi)
            err_slope_i.append(ei)
            err_intercept_i.append(fi)
    PLW = pd.DataFrame(
        {'name': PL_name,
        'mg': PL_slope_g,
        'cg': PL_intercept_g,
        'err_mg': err_slope_g,
        'err_cg': err_intercept_g,
        'mi': PL_slope_i,
        'ci': PL_intercept_i,
        'err_mi': err_slope_i,
        'err_ci': err_intercept_i
        })
    #PLW = PLW.set_index('name').T
    residue.to_csv('%s%i_residue.csv'%(data_out+process_step[1],len(residue)))
    prediction.to_csv('%s%i_prediction.csv'%(data_out+process_step[1],len(prediction)))
    PLW.to_csv('./%s%i_regression.csv'%(data_out+process_step[1],len(PLW)))
    return PLW, residue, prediction
