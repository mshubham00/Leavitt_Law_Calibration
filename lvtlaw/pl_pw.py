### File: ./lvtlaw/pl_pw.py

import pandas as pd
import numpy as np
from functools import reduce
from lvtlaw.utils import regression, color_index, mag, bands, data_dir, data_file, data_out
    # regression(x,y,x_str,y_str,print_flag) -> slope, intercept, prediction, residue, err_slope, err_intercept
    # color_index -> list of all permutation of band filters
color_index = color_index()
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

def pl_reg(data, disg = '_g', disi='_i'):
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
    prediction['logP'] = residue['logP'] = data['logP']
    
    for i in range(0,6):    # absolute_mag : M_B_g
        ag,bg,cg,dg,eg,fg = regression(data['logP']-1, data[bands[i]+disg], '(logP -1)', bands[i]+disg, 1)
        ai,bi,ci,di,ei,fi = regression(data['logP']-1, data[bands[i]+disi], '(logP -1)', bands[i]+disi, 1)
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
            PL_slope_g.append(ag)
            PL_intercept_g.append(bg)
            err_slope_g.append(eg)
            err_intercept_g.append(fg)
            PL_slope_i.append(ai)
            PL_intercept_i.append(bi)
            err_slope_i.append(ei)
            err_intercept_i.append(fi)
            PL_name.append(mag[i]+color)

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
    return PLW, residue, prediction
