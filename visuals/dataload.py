### file: ./visuals/dataload.py

import pandas as pd
import os
import subprocess
from lvtlaw.utils import wes_cols, mag, dis_flag

process_step = ['1_prepared/','2_PLPW/','3_deldel/', '4_reddening/', '5_dispersion/','6_rms/','7_errorpair/', '8_result/']

#### 
raw = pd.read_csv('./data/input/cleaned_data.csv')
data_path = './data/output/'

####
absolute = pd.read_csv('%s95_abs_data.csv'%(data_path+process_step[0]))
extinction = pd.read_csv('%s95_ext_data.csv'%(data_path+process_step[0]))
tabsolute = pd.read_csv('%s95_true_abs_data.csv'%(data_path+process_step[0]))
wesenheit = pd.read_csv('%s95_wes_data.csv'%(data_path+process_step[0]))

####
PLWdata = pd.read_csv('%s95_prepared_PLdata.csv'%(data_path+process_step[1]))
PLWresidue = pd.read_csv('%s95_residue.csv'%(data_path+process_step[1]))
PLWregression = pd.read_csv('%s102_regression.csv'%(data_path+process_step[1]))
PLWprediction = pd.read_csv('%s95_prediction.csv'%(data_path+process_step[1]))

#### 
dpre_M = pd.read_csv('%s95_del_pre_M.csv'%(data_path+process_step[2]))
dres_M = pd.read_csv('%s95_del_res_M.csv'%(data_path+process_step[2]))
dmc_M = pd.read_csv('%s95_del_slope_intercept_M.csv'%(data_path+process_step[2]))
dpre_S = pd.read_csv('%s95_del_pre_S.csv'%(data_path+process_step[2]))
dres_S = pd.read_csv('%s95_del_res_S.csv'%(data_path+process_step[2]))
dmc_S = pd.read_csv('%s95_del_slope_intercept_S.csv'%(data_path+process_step[2]))

####
#dpre_M = pd.read_csv('%s95_del_pre_M.csv'%(data_path+process_step[3]))
def load_star(total_stars):
    stars = {}
    for t in range(total_stars):    
        stars[t] = pd.read_csv('%s%i_%i_star.csv' % (data_path + process_step[2], len(mag), t) )
    return stars

stars = load_star(len(raw))    

def ext(dis):
    ext_S = {}
    ext_M = {}
    for c in wes_cols:
        for m in mag:
            ext_S[m+m+c+dis] = pd.read_csv('%s95_ext_%s%s.csv' % (data_path + process_step[3], m + m + c, dis))
            ext_M[m + c[0] + c+dis] = pd.read_csv('%s95_ext_%s%s.csv' % (data_path + process_step[3], m + c[0] + c, dis))
    ext_MS_dic_deldel = [ext_M, ext_S]
    return ext_MS_dic_deldel

ext_g = ext('_g')
ext_i = ext('_i')

def red(dis):
    red_S = {}
    red_M = {}
    for c in wes_cols:
        for m in mag:
            red_S[m+m+c+dis] = pd.read_csv('%s95_red_%s%s.csv' % (data_path + process_step[3], m + m + c, dis))
            red_M[m + c[0] + c+dis] = pd.read_csv('%s95_red_%s%s.csv' % (data_path + process_step[3], m + c[0] + c, dis))
    red_MS_dic_deldel = [red_M, red_S]
    return red_MS_dic_deldel

red_g = red('_g')
red_i = red('_i')


def pick_extred(t,wes_str,dis):
    f = pd.read_csv('%s%i_%s_%s%s.csv'%(data_path + process_step[3],len(raw),t,wes_str,dis))
    return f

#def red(dis):
 #           red_S[m+m+c+dis] = pd.read_csv('%s95_dispersion_g_BV__M_0.000000.csvred_%s%s.csv' % (data_path + process_step[3], m + m + 




