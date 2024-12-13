### File: ./lvtlaw/residue.py
import os
import pandas as pd
import numpy as np
from scipy import stats
from functools import reduce
from lvtlaw.utils import A, R, mag, bands, ap_bands, colors, data_dir, data_file, data_out, regression
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)


out_dir = './data/output/'
regression_file = '102_regression.csv'       # 102 = absolute (1x6), true_absolute (1x6), wesenheint (15x6) 
residue_file = '95_residue.csv'
#print(data_dir)

regression_file = pd.read_csv(out_dir+regression_file)
residue_file = pd.read_csv(out_dir+residue_file)
#residue_file.info()
#print(residue_file.head(7).T)
#print(len(regression_file))
def filter_PLW_slope_intercept_data(data = regression_file):
    relations = []
    for i in range(0,17):
        regress_data = data[i*6:6*i+6]
        #print('\n \t %i \t Relation  Slope, intercept, respective error in Gaia (g) and IRSB (i) cases \n '%(i), data[i*6:6*i+6])
        relations.append(regress_data)
    return relations

PLW = filter_PLW_slope_intercept_data()

def filter_residue(data=residue_file):
    relations = []
    for i in range(0,17):
        residue_data = data.T[i*12+3:12*i+15]
        #print('\n %i BVIJHK band Residue with Gaia (g) and IRSB (i) cases \n '%(i), residue_data)
        relations.append(residue_data)
    return relations

residue = filter_residue()




disg = '_g'
disi = '_i'

def del_del(col): 
    #input a reference wesenheit color and this function result the delta delta correlation. 
    del_res_WM = pd.DataFrame()
    del_res_WM_M = pd.DataFrame()
    del_pre_WM = pd.DataFrame()
    del_pre_WM_M = pd.DataFrame()
    del_pre_WM['name'] = del_res_WM['name'] = residue_file['name']
    del_pre_WM_M['name'] = del_res_WM_M['name'] = residue_file['name']
  
    del_mg = []
    del_cg = [] 
    del_meg = []
    del_ceg = []
    del_name = [] 
    del_mi = []
    del_ci = [] 
    del_mei = []
    del_cei = []

    del_mg_M = []
    del_cg_M = [] 
    del_meg_M = []
    del_ceg_M = []
    del_name_M = [] 
    del_mi_M = []
    del_ci_M = [] 
    del_mei_M = []
    del_cei_M = []

    for i in range(0,6):
        wesen = mag[i]+col # My approach
        mg, cg, prg, reg , mrg, crg = regression(residue_file['r_'+wesen+disg], residue_file['r_'+mag[i]+disg], wesen, mag[i]+disg,1) 
        mi, ci, pri, rei , mri, cri = regression(residue_file['r_'+wesen+disi], residue_file['r_'+mag[i]+disi], wesen, mag[i]+disi,1) 
        del_name.append(mag[i]+wesen)
        del_mg.append(mg)
        del_cg.append(cg)
        del_meg.append(mrg)
        del_ceg.append(crg)
        del_res_WM['r_'+mag[i]+wesen+disg] = reg
        del_pre_WM['p_'+mag[i]+wesen+disg] = prg

        del_mi.append(mi)
        del_ci.append(ci)
        del_mei.append(mri)
        del_cei.append(cri)
        del_res_WM['r_'+mag[i]+wesen+disi] = rei
        del_pre_WM['p_'+mag[i]+wesen+disi] = pri

        wesen = col[0]+col # Madore approach
        mg, cg, prg, reg , mrg, crg = regression(residue_file['r_'+wesen+disg], residue_file['r_'+mag[i]+disg], wesen, mag[i]+disg,1) 
        mi, ci, pri, rei , mri, cri = regression(residue_file['r_'+wesen+disi], residue_file['r_'+mag[i]+disi], wesen, mag[i]+disi,1) 
        del_name_M.append(mag[i]+wesen)
        del_mg_M.append(mg)
        del_cg_M.append(cg)
        del_meg_M.append(mrg)
        del_ceg_M.append(crg)
        del_res_WM_M['r_'+mag[i]+wesen+disg] = reg
        del_pre_WM_M['p_'+mag[i]+wesen+disg] = prg
        del_mi_M.append(mi)
        del_ci_M.append(ci)
        del_mei_M.append(mri)
        del_cei_M.append(cri)
        del_res_WM_M['r_'+mag[i]+wesen+disi] = rei
        del_pre_WM_M['p_'+mag[i]+wesen+disi] = pri

    del_slope_interecept_M = pd.DataFrame({'name': del_name_M, 
                                         'mg': del_mg_M, 'cg': del_cg_M, 
                                         'err_mg': del_meg_M,'err_cg': del_ceg_M, 
                                         'mi': del_mi_M, 'ci': del_ci_M, 
                                         'err_mi': del_mei_M,'err_ci': del_cei_M})

    del_slope_interecept = pd.DataFrame({'name': del_name, 
                                         'mg': del_mg, 'cg': del_cg, 
                                         'err_mg': del_meg,'err_cg': del_ceg, 
                                         'mi': del_mi, 'ci': del_ci, 
                                         'err_mi': del_mei,'err_ci': del_cei})
    return  del_res_WM, del_pre_WM, del_slope_interecept,  del_res_WM_M, del_pre_WM_M, del_slope_interecept_M

def del_col(ls=['BV', 'VI','JK'], s=0):
    dres = pd.DataFrame()
    dpre = pd.DataFrame()
    dres['name'] = dpre['name'] = residue_file['name']
    dmc = []

    dres_M = pd.DataFrame()
    dpre_M = pd.DataFrame()
    dres_M['name'] = dpre_M['name'] = residue_file['name']
    dmc_M = []
    for k in ls:
        print(k)
        a,b,c,d,e,f = del_del(k)
        dres = pd.merge(dres,a, on='name')
        dpre= pd.merge(dpre,b, on='name')
        dmc.append(c)
        dres_M = pd.merge(dres_M,d, on='name')
        dpre_M= pd.merge(dpre_M,e, on='name')
        dmc_M.append(f)
    
    del_mc = pd.concat(dmc, axis = 0, join = 'inner', ignore_index=True)
    del_mc = del_mc.drop_duplicates().set_index('name').T

    del_mc_M = pd.concat(dmc_M, axis = 0, join = 'inner', ignore_index=True)
    del_mc_M = del_mc_M.drop_duplicates().set_index('name').T
    #del_mc =del_mc.T
    print('There will be %i relations, 12 for %i color minus duplicates.'%((6)*len(dmc), len(ls)))
    if s==1:
        cepheid = len(residue_file)
        del_mc.to_csv('%s%i_del_slope_intercept.csv'%(out_dir,cepheid))
        dres.to_csv('%s%i_del_res.csv'%(out_dir,cepheid))
        dpre.to_csv('%s%i_del_pre.csv'%(out_dir,cepheid))
        del_mc_M.to_csv('%s%i_del_slope_intercept_M.csv'%(out_dir,cepheid))
        dres_M.to_csv('%s%i_del_res_M.csv'%(out_dir,cepheid))
        dpre_M.to_csv('%s%i_del_pre_M.csv'%(out_dir,cepheid))
    return dres, dpre, del_mc, dres_M, dpre_M, del_mc_M

def residue_analysis(colors= colors, s=0):
    for i in range(0,len(residue)):
        print(residue[i])
    input('Show the residual correlation data:')
    dres,dpre,del_mc, dres_M, dpre_M, del_mc_M = del_col(colors,s)
    return dres,dpre,del_mc, dres_M, dpre_M, del_mc_M

