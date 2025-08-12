### file: ./visuals/dataload.py

import pandas as pd
import os
import subprocess
from lvtlaw.a_utils import load_data, nreg, process_step, input_data_file, dis_list, dis_flag, A, R, mag, abs_bands, data_out, wes_show, data_cols
from decimal import Decimal, getcontext
getcontext().prec = 10

#### 
cleaned_data = load_data(input_data_file)
raw = cleaned_data[data_cols].dropna().reset_index(drop=True)
n = len(raw)  # total number of cepheids

n = len(raw)
####
def transformation():
    absolute = pd.read_csv('%s%i_abs_data.csv'%(data_out+process_step[0],n))
    extinction = pd.read_csv('%s%i_ext_data.csv'%(data_out+process_step[0],n))
    tabsolute = pd.read_csv('%s%i_true_abs_data.csv'%(data_out+process_step[0],n))
    wesenheit = pd.read_csv('%s%i_wes_data.csv'%(data_out+process_step[0],n))
    return absolute, extinction, tabsolute, wesenheit
####
def PLWcorrection():
    PLWdata = pd.read_csv('%s%i_prepared_PLdata.csv'%(data_out+process_step[1],n))
    PLWresidue = pd.read_csv('%s%i_residue.csv'%(data_out+process_step[1],n))
    PLWregression = pd.read_csv('%s%i_%i_regression.csv'%(data_out+process_step[1], n, nreg))
    PLWprediction = pd.read_csv('%s%i_prediction.csv'%(data_out+process_step[1],n))
    return PLWdata, PLWresidue, PLWregression, PLWprediction
#### 
def del_del():
    dpre_S = pd.read_csv('%s%i_del_pre.csv'%(data_out+process_step[2],n))
    dres_S = pd.read_csv('%s%i_del_res.csv'%(data_out+process_step[2],n))
    dmc_S = pd.read_csv('%s%i_del_slope_intercept.csv'%(data_out+process_step[2],n))
    dSM = [[dmc_S],[dres_S], [dpre_S]]
    return dpre_S, dres_S, dmc_S, dSM
####
def ext_red():
    ext0S = pd.read_csv('%s%i_ext_err0_S.csv' % (data_out + process_step[3], n))
    red0S = pd.read_csv('%s%i_red_err0_S.csv' % (data_out + process_step[3], n))
    return ext0S, red0S
####
def pick_dispersion(dis, wm_str,flag):
    f = pd.read_csv('%s%i%s%s.csv' % (data_out + process_step[4], n, dis, wm_str))
    return f
####
def pick_star(i):
    f = pd.read_csv('%s%i_star.csv'%(data_out+process_step[9],i), index_col=0)
    ex_red_mu = pd.read_csv('%s%i_%istars_ex_red_mu.csv'%(data_out+process_step[5],n,i), index_col=0) 
    #df = ex_red_mu.drop(ex_red_mu.columns[0], axis=1)
    #df = df.applymap(lambda x: Decimal(x) if x.replace('.', '', 1).isdigit() else x)
    return f, ex_red_mu
####
def correction_red_mu_stars():
    correction = pd.read_csv('%s%i_error_rms_mu_rd.csv'%(data_out+process_step[6],n))  
    return correction

def result():
    result = pd.read_csv('%s%i_corrected.csv'%(data_out+process_step[7],n))      
    reg = pd.read_csv('%s%i_%i_result_regression.csv'%(data_out+process_step[7],n, nreg))      
    res = pd.read_csv('%s%i_result_residue.csv'%(data_out+process_step[7],n))      
    pre = pd.read_csv('%s%i_result_prediction.csv'%(data_out+process_step[7],n))      
    return result, reg, res, pre

#dpre_M = pd.read_csv('%s95_del_pre_M.csv'%(data_path+process_step[3]))
def load_star(total_stars):
    stars = {}
    for t in range(total_stars):    
        stars[t] = pd.read_csv('%s%i_star.csv' % (data_out + process_step[9], t) )
    return stars

#stars = load_star(n)    

def ext(dis):
    ext_S = {}
    ext_M = {}
    for c in wes_cols:
        for m in mag:
            ext_S[m+m+c+dis] = pd.read_csv('%s%i_ext_%s%s.csv' % (data_out + process_step[3],n, m + m + c, dis))
            ext_M[m + c[0] + c+dis] = pd.read_csv('%s%i_ext_%s%s.csv' % (data_out + process_step[3],n, m + c[0] + c, dis))
    ext_MS_dic_deldel = [ext_M, ext_S]
    return ext_MS_dic_deldel

#ext_g = ext('_g')
#ext_i = ext('_i')

def red(dis):
    red_S = {}
    red_M = {}
    for c in wes_cols:
        for m in mag:
            red_S[m+m+c+dis] = pd.read_csv('%s%i_red_%s%s.csv' % (data_out + process_step[3], n, m + m + c, dis))
            red_M[m + c[0] + c+dis] = pd.read_csv('%s%i_red_%s%s.csv' % (data_out + process_step[3],n, m + c[0] + c, dis))
    red_MS_dic_deldel = [red_M, red_S]
    return red_MS_dic_deldel

#red_g = red('_g')
#red_i = red('_i')


def pick_extred(exrd,wes_str,dis):
    f = pd.read_csv('%s%i_%s_%s%s.csv'%(data_out + process_step[3],n,exrd,wes_str,dis))
    return f


def pick_disper(dis,col,flag,mu_str):
    f = pd.read_csv('%s%i_dispersion%s_%s%s_%s.csv'%(data_out+process_step[4],n,dis,col,flag,mu_str))
    return f



