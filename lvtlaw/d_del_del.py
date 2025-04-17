### File: ./lvtlaw/d_del_del.py
from lvtlaw.a_utils import A, R, mag, abs_bands, ap_bands, colors, data_dir, input_data_file, data_out, regression, dis_flag, process_step
import os, pandas as pd, numpy as np
from scipy import stats
from functools import reduce
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
bands = abs_bands
out_dir = data_out

def correlation_extraction(residue_file, dis_flag, col, flag):
    # input the PL and PW residues for different distance methods. Flag represents Shubham or Madore approach.  
    del_mc = pd.DataFrame()
    del_pre_WM = pd.DataFrame()
    del_res_WM = pd.DataFrame()
    del_pre_WM['name'] =  del_res_WM['name'] = residue_file['name'] # star-by-star
    print('\n Approach: ', flag, '\t Color: ',col)
    for diss in dis_flag:
        del_m = []
        del_c = [] 
        del_me = []
        del_ce = []
        del_name = [] 
        for i in range(0,len(mag)):
            if flag == 'S':
                wesen = mag[i]+col 
            else:
                wesen = col[0]+col 
            #regression(residue_file['r_'+wesen+diss], residue_file['r_'+mag[i]+diss], wesen, mag[i]+'_'+diss, 1)
            m, c, pr, re, mr, cr = regression(residue_file['r_'+wesen+diss], residue_file['r_'+mag[i]+'0'+diss], wesen, mag[i]+'0'+diss, 1)
            del_name.append(mag[i]+wesen)
            del_m.append(m)
            del_c.append(c)
            del_me.append(mr)
            del_ce.append(cr)
            del_res_WM['d_'+mag[i]+wesen+diss] = re
            del_pre_WM['p_'+mag[i]+wesen+diss] = pr
        del_mc['name'] = del_name
        del_mc['m'+diss] = del_m
        del_mc['c'+diss] = del_c
        del_mc['me'+diss] = del_me
        del_mc['ce'+diss] = del_ce 
    # Function returns regression data for each combination (del_mc) and residue of individual stars.
    return del_res_WM, del_pre_WM, del_mc
    
def residue_analysis(residue_file, dis = dis_flag, cols=['BV','BI','VI'], s=1):
    dres_S = pd.DataFrame()
    dpre_S = pd.DataFrame()
#    residue_file = residue_file.loc[:, ~residue_file.columns.duplicated()]
    dres_S['name'] = dpre_S['name'] = residue_file['name']
    dres_S['logP'] = dpre_S['logP'] = residue_file['logP']
    dmc_S = []
    dres_M = pd.DataFrame()
    dpre_M = pd.DataFrame()
    dres_M['name'] = dpre_M['name'] = residue_file['name']
    dres_M['logP'] = dpre_M['logP'] = residue_file['logP']
    dmc_M = []                       
    # Ensure the result of correlation_extraction is properly handled
    for col in cols:
        Ma, Mb, Mc = correlation_extraction(residue_file, dis, col, 'M')
        dres_M = pd.merge(dres_M, Ma, on='name')
        dpre_M = pd.merge(dpre_M, Mb, on='name')
        dmc_M.append(Mc)  # Convert to string explicitly
        Sa, Sb, Sc = correlation_extraction(residue_file, dis, col, 'S')
        dres_S = pd.merge(dres_S, Sa, on='name')
        dpre_S = pd.merge(dpre_S, Sb, on='name')
        dmc_S.append(Sc)  # Convert to string explicitly
# Concatenate and clean up the dmc_S and dmc_M lists
    del_mc_S = pd.concat(dmc_S, axis=0, join='inner', ignore_index=True)
    del_mc_S = del_mc_S.drop_duplicates().set_index('name').T
    del_mc_M = pd.concat(dmc_M, axis=0, join='inner', ignore_index=True)
    del_mc_M = del_mc_M.drop_duplicates().set_index('name').T                          
    #del_mc =del_mc.T
    print('There will be %i relation s, 12 for %i color minus duplicates.'%((6)*len(dmc_S), len(cols)))
    if s==1:
        cepheid = len(residue_file)
        del_mc_S.to_csv('%s%i_del_slope_intercept_S.csv'%(out_dir+process_step[2],cepheid))
        dres_S.to_csv('%s%i_del_res_S.csv'%(out_dir+process_step[2],cepheid))
        dpre_S.to_csv('%s%i_del_pre_S.csv'%(out_dir+process_step[2],cepheid))
        del_mc_M.to_csv('%s%i_del_slope_intercept_M.csv'%(out_dir+process_step[2],cepheid))
        dres_M.to_csv('%s%i_del_res_M.csv'%(out_dir+process_step[2],cepheid))
        dpre_M.to_csv('%s%i_del_pre_M.csv'%(out_dir+process_step[2],cepheid))
    return dres_S, dpre_S, del_mc_S, dres_M, dpre_M, del_mc_M

 
