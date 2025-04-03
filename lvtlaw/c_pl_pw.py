### File: ./lvtlaw/c_pl_pw.py
from lvtlaw.a_utils import process_step, regression, color_index, mag, ap_bands, abs_bands, data_dir, input_data_file, data_out, dis_flag

import pandas as pd
import numpy as np
from functools import reduce
    # regression(x,y,x_str,y_str,print_flag) -> slope, intercept, prediction, residue, err_slope, err_intercept
    # color_index -> list of all permutation of band filters
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

color_index = color_index()
'''
def regres(dis,x,y,x_str,y_str,p):
    PL_name=[]
    PL_slope = []             # Gaia based slope of period luminosity relation 
    PL_intercept = []
    err_slope = []
    err_intercept = []
    residue = pd.DataFrame()
    prediction = pd.DataFrame()
    prediction['name'] =  residue['name'] = data['name']
    for i in range(0,6):    # absolute_mag : M_B_g
        a,b,c,d,e,f = regression(x, y, x_str, y_str, p)
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
        'err_c%s'%(dis): err_intercept})
    return PLW, residue, prediction


def pl_reg(data, s=1, dis = dis_flag, bands = abs_bands):
    PLW_g = pd.DataFrame(columns = ['name', 'm_g','c_g','err_m_g','err_c_g'])
    PLW_i = pd.DataFrame(columns = ['name', 'm_i','c_i','err_m_i','err_c_i'])
    PLW = {'_g': PLW_g, '_i':PLW_i}
    input('Enter')
    PLmc=[]
    for d in dis:
        print(PLW['_g'])
        l = PLW['%s'%(d)]
        mc, res, pre = regres(d, data['logP']-1, data[bands[i]+d], '(logP - 1)', bands[i]+d, 1)
        l = pd.concat(l, mc, ignore_index=True)
        mc_0, res_0, pre_0 = regres(d, data['logP']-1, data[bands[i]+'0'+disg], '(logP -1)', bands[i]+'0'+disg, 1)
        l = pd.concat(l, mc_0, ignore_index=True)
        mc_w, res_w, pre_w = regres(d, data['logP']-1, data[mag[i]+color+disg], '(logP -1)', mag[i]+color+disg,1)
        l = pd.concat(l, mc_w, ignore_index=True)
        PLmc.append(l)
        if s==1:
            mc_w.to_csv('%s%i_slope_w%s.csv'%(data_out+process_step[1],len(mc_w), d))
            mc.to_csv('%s%i_slope%s.csv'%(data_out+process_step[1],len(mc), d))
            mc_0.to_csv('%s%i_slope_0%s.csv'%(data_out+process_step[1],len(mc_0), d))
            l.to_csv('%s%i_PLW%s.csv'%(data_out+process_step[1],len(mc_w), d))
        print(l.T.head())
    return PLmc

'''

def append_PLW(PLW_struct,i,a,b,c,d,e,f):
    PLW_struc[0].append(mag[i])
    PLW_struc[1].append(a)
    PLW_struc[2].append(b)
    PLW_struc[3]['p_'+mag[i]+disg] = c   
    PLW_struc[4]['r_'+mag[i]+disg] = d
    PLW_struc[5].append(c)
    PLW_struc[6].append(d)
    return PLW_struct


def pl_dis(residue, dis_flag, bands):
    PL_name=[]
    PL_slope = []             # Gaia based slope of period luminosity relation 
    PL_intercept = []
    err_slope = []
    err_intercept = []
    residue = pd.DataFrame()
    prediction = pd.DataFrame()
    prediction['name'] =  residue['name'] = data['name']
    prediction['logP'] =  residue['logP'] = data['logP']
    prediction['%s'%(dis_flag)] =  residue['%s'%(dis_flag)] = data['%s'%(dis_flag)]
    prediction['EBV'] =  residue['EBV'] = data['EBV']
    PLW_struct = [PL_name, PL_slope, PL_intercept, residue, prediction, err_slope, err_intercept]
    for i in range(0,len(mag)):    # absolute_mag : M_B_g
        a,b,c,d,e,f = regression(data['logP']-1, data[bands[i]+disg], '(logP - 1)', bands[i]+disg, 1)
        PLW_struct = append_PLW(PLW_struct, a,b,c,d,e,f)
    for i in range(0,len(mag)):    # true_ absolute_mag : M_B0_g
        a,b,c,d,e,f = regression(data['logP']-1, data[bands[i]+'0'+disg], '(logP -1)', bands[i]+'0'+disg, 1)
        PLW_struct = append_PLW(PLW_struct, a,b,c,d,e,f)
    for color in color_index:   # wesenheit magnitude: BVK_g
        for i in range(0,len(mag)):
            a,b,c,d,e,f = regression(data['logP']-1, data[mag[i]+color+disg], '(logP -1)', mag[i]+color+disg,1)
            PLW_struct = append_PLW(PLW_struct, a,b,c,d,e,f)



    
   def pl_reg(data, s=1, dis_flag = dis_flag, bands = abs_bands):
    disg = dis_flag[0]
    disi = dis_flag[1]
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
    prediction['logP'] =  residue['logP'] = data['logP']
    prediction['plx'] =  residue['plx'] = data['plx']
    prediction['EBV'] =  residue['EBV'] = data['EBV']
    for i in range(0,len(mag)):    # absolute_mag : M_B_g
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
    for i in range(0,len(mag)):    # true_ absolute_mag : M_B0_g
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
        for i in range(0,len(mag)):
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
    if s==1:
        residue.to_csv('%s%i_residue.csv'%(data_out+process_step[1],len(residue)))
        prediction.to_csv('%s%i_prediction.csv'%(data_out+process_step[1],len(prediction)))
        PLW.to_csv('./%s%i_regression.csv'%(data_out+process_step[1],len(PLW)))
    filter_PLW_slope_intercept_data(PLW, s)
    filter_residue(residue, s)
    return PLW, residue, prediction
    
def filter_PLW_slope_intercept_data(data, s=1,n=17):
    relations = []
    for i in range(0,n):
        regress_data = data[i*len(mag):len(mag)*i+len(mag)]
        relations.append(regress_data)
        print(regress_data)
        if s==1:
            regress_data.to_csv('./%s%i_regress_%i.csv'%(data_out+process_step[1],len(regress_data), i))
        # first two are PL and PL0 and remaining 15 are PWs in gaia and IRSB
    return relations


def filter_residue(data, s=1,n=17):
    relations = []
    for i in range(0,n):
        residue_data = data.T[i*12+3:12*i+15]
        #print('\n %i BVIJHK band Residue with Gaia (g) and IRSB (i) cases \n '%(i), residue_data)
        if s==1:
            residue_data.to_csv('./%s%i_residue_%i.csv'%(data_out+process_step[1],len(residue_data), i))
        relations.append(residue_data)
        print(residue_data)
    return relations

    
