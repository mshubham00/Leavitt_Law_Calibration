### file: ./visuals/h_loadoutput.py
module = 'h_loadoutput'
import pandas as pd
import os
import subprocess
from data.datamapping import *
from lvtlaw.a_utils import load_data, imgsave
from decimal import Decimal, getcontext
getcontext().prec = 10

#### 
input_data, raw, mag, dis = load_data(file_name)
raw = input_data[data_cols].dropna().reset_index(drop=True);
n = len(raw)  # total number of cepheids
####

def transformation_(raw=raw, data_out=data_out, n=n):  # b_data_transform
    raw = raw
    absolute = pd.read_csv('%s%i_abs_data.csv'%(data_out+process_step[0],n))
    extinction = pd.read_csv('%s%i_ext_data.csv'%(data_out+process_step[0],n))
    tabsolute = pd.read_csv('%s%i_true_abs_data.csv'%(data_out+process_step[0],n))
    wesenheit = pd.read_csv('%s%i_wes_data.csv'%(data_out+process_step[0],n))
    merged_data = pd.read_csv('%s%i_prepared_PLdata.csv'%(data_out+process_step[0],n))
    return raw, absolute, extinction, tabsolute, wesenheit, merged_data
####
def PLWcorrection_(data_out=data_out, n=n):     # c_pl_pw
    PLWresidue = pd.read_csv('%s%i_residue.csv'%(data_out+process_step[1],n))
    PLWregression = pd.read_csv('%s%i_regression.csv'%(data_out+process_step[1], n))
    PLWprediction = pd.read_csv('%s%i_prediction.csv'%(data_out+process_step[1],n))
    data = pd.read_csv('%s%i_merged_data.csv'%(data_out+process_step[1],n))        
    return PLWregression, PLWresidue, PLWprediction, data
#### 
def residual_correlation_(data_out = data_out, n=n):     # d_del_del
    dpre = pd.read_csv('%s%i_del_pre.csv'%(data_out+process_step[2],n))
    dres = pd.read_csv('%s%i_del_res.csv'%(data_out+process_step[2],n))
    dmc = pd.read_csv('%s%i_del_slope_intercept.csv'%(data_out+process_step[2],n))
    data = pd.read_csv('%s%i_merged_data.csv'%(data_out+process_step[2],n))        
    return dmc, dpre, dres, data
####
def rd_mu_error_matrix_(data_out=data_out, n=n):    # e_error_estimation
    data = pd.read_csv('%s%i_merged_data.csv'%(data_out+process_step[2],n))        
    ext0 = pd.read_csv('%s%i_ext_err0.csv' % (data_out + process_step[3], n))
    red0 = pd.read_csv('%s%i_red_err0.csv' % (data_out + process_step[3], n))
    mu_df_list_dict = {}
    for dis in dis_flag: 
        for flag in flags:
            for col in wes_show:   
                mu_df_list = []
                for i, band in enumerate(mag):
                    wm_str = f"{band}{mode[-1]}{band}{col}" if flag == "S" else f"{band}{mode[-1]}{col[0]}{col}"
                    mu_rd_ex_df = pd.read_csv('%s%i_mu_rd_ex%s%s.csv' % (data_out + process_step[4], n, dis, wm_str))
                    mu_df_list.append(mu_rd_ex_df)
                mu_df_list_dict[f'{col}_{flag}{dis}'] = mu_df_list
    return ext0, red0, mu_df_list_dict, data
####
def starwise_analysis_(p=0, data_out=data_out, n=n):    # f_star_wise
    data = pd.read_csv('%s%i_merged_data.csv'%(data_out+process_step[2],n))        
    stars_list = []
    stars_ex_red_mu_list = []
    for i in range(n):
        star = pd.read_csv('%s%i_star.csv'%(data_out+process_step[9],i), index_col=0)
        stars_list.append(star)    
        star_df = pd.read_csv(f'{data_out}{process_step[5]}{n}_{i}stars_ex_red_mu.csv')
        stars_ex_red_mu_list.append(star_df)
        correction_red_mu_stars = pd.read_csv('%s%i_error_rms_mu_rd.csv'%(data_out+process_step[6],len(raw)))
        if p ==1:
            print(f'Star: {i} | Name: {data.name.iloc[i]} \n', i, star_df)
    return stars_list, stars_ex_red_mu_list, correction_red_mu_stars, data

def pick_star(i, data_out=data_out, n=n):
    f = pd.read_csv('%s%i_star.csv'%(data_out+process_step[9],i), index_col=0)
    ex_red_mu = pd.read_csv('%s%i_%istars_ex_red_mu.csv'%(data_out+process_step[5],n,i), index_col=0) 
    return f, ex_red_mu

def calibrated_result_(data_out = data_out, n=n):
    merged_data = pd.read_csv('%s%i_merged_data.csv'%(data_out+process_step[7],n))      
    reg = pd.read_csv('%s%i_result_regression.csv'%(data_out+process_step[7],n))      
    res = pd.read_csv('%s%i_result_residue.csv'%(data_out+process_step[7],n))      
    pre = pd.read_csv('%s%i_result_prediction.csv'%(data_out+process_step[7],n))  
    return merged_data, reg, res, pre


import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import Normalize

def print_PL(r, file_name, wes_show):
    slp, inr, esl, ein, stt = {}, {}, {}, {}, {}

    for col in mag:
        cols = [f'{col}0{m}S' for m in wes_show]
        slp[col] = r[cols].rename(columns=dict(zip(cols, wes_show))).iloc[0]
        inr[col] = r[cols].rename(columns=dict(zip(cols, wes_show))).iloc[1]
        esl[col] = r[cols].rename(columns=dict(zip(cols, wes_show))).iloc[2]
        ein[col] = r[cols].rename(columns=dict(zip(cols, wes_show))).iloc[3]
        stt[col] = r[cols].rename(columns=dict(zip(cols, wes_show))).iloc[4]

    slope     = pd.DataFrame(slp)
    intercept = pd.DataFrame(inr)
    serr      = pd.DataFrame(esl)
    ierr      = pd.DataFrame(ein)
    standard  = pd.DataFrame(stt)

    return slope, intercept, serr, ierr, standard


def heatmap_compare(df, er, title="Heatmap Comparison", left ='Values', right ='Column wise normalized Error', cmap="coolwarm", fmt=".4f", name='file', s=0):
    # Global normalization
    norm = Normalize(vmin=df.min().min(), vmax=df.max().max())
    # Per-column normalization
    df_norm = (er - er.min()) / (er.max() - er.min())

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Global scale heatmap
    sns.heatmap(
        df,
        cmap=cmap,
        norm=norm,
        annot=True,
        fmt=fmt,
        linewidths=0.5,
        cbar_kws={"label": "Value"},
        ax=axes[0]
    )

    # Per-column scale heatmap
    sns.heatmap(
        df_norm,
        cmap=cmap,
        annot=er,      # show original values
        fmt=fmt,
        linewidths=0.5,
        cbar=False,
        ax=axes[1]
    )
    axes[0].set_title(left)
    axes[1].set_title(right)

    plt.suptitle(title, fontsize=16)
    plt.tight_layout()
    if s==1:
        imgsave(title=name+title)
    plt.show()
 

print(f'* * {module} module loaded!')

