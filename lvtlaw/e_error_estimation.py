### File: ./lvtlaw/e_error_estimation.py
'''
This file estimates the variation in reddening error with respect to expected distance modulus error trails. 

The output will be saved in 'data/{DatasetName_Rv}/4_reddening/*.csv'

Function contained:
    select_regression_parameters(dSM, dis): Retrieve slope and intercept from d_del_del.residue_analysis dSM as per color and method.
        Output: m, c
    error_over_mu(): Estimates reddening error for distance error possibilities, saves DataFrame mu_rd_ex_df
        Output: ext0_list, red0_list, mu_rd_ex_df
    process_reddening(col, dis, flag): 
        Output: mu_df_list, ext0_df, red0_df
    reddening_error(): Executes above for different colors, distance and flag
        Output: red0_df_list, mu_df_list_dict
'''
module = 'e_error_estimation'
from lvtlaw.datamapping import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from lvtlaw.a_utils import merge_12, imgsave
from lvtlaw.b_data_transform import transformation, extinction_law
from lvtlaw.c_pl_pw import pl_reg     
#####################################################################
def select_regression_parameters(dmc, dis): 
    # this function selects particular slope and intercept from del-del correlation
    if dis == '_i':
        m, c = dmc.iloc[4].T, dmc.iloc[5].T
    else:
        m, c = dmc.iloc[0].T, dmc.iloc[1].T
    return m, c #lists
#####################################################################
def error_over_mu(dres, m, dis, col, slope, intercept, flag, R=R, s=s): # called by process_reddening()
    r = R[mag[m]]#+col]  # reddening ratio
    mu_rd_ex_df = pd.DataFrame({'name': dres['name'], 'logP': dres['logP'], 'EBV': dres['EBV']})
    for ab in mode: 
        wm_str = f"{mag[m]}{ab}{mag[m]}{col}" if flag == "S" else f"{mag[m]}{ab}{col[0]}{col}"
        slope_ = slope[wm_str]
        print('   ', wm_str, '   ',1-slope_)
        intercept_ = intercept[wm_str]
        ext0_list = dres[f'd_{wm_str}{dis}'] # extinction error  without changing modulus from d_residue_analysis()
        red0_list = ext0_list / r  # Convert extinction to reddening E(B-V)
        for mu in del_mu: # 
            mu_rd_ex_df[f'ex_{ab}{col}{mu}{dis}'] = ext0_list + mu * (1 - slope_) 
            mu_rd_ex_df[f'rd_{ab}{col}{mu}{dis}'] = mu_rd_ex_df[f'ex_{ab}{col}{mu}{dis}'] / r
    if s == 1:
        mu_rd_ex_df.to_csv(f'{data_out}{process_step[4]}{len(mu_rd_ex_df)}_mu_rd_ex{dis}{wm_str}.csv', index=False)
    return wm_str, ext0_list, red0_list, mu_rd_ex_df
#####################################################################
def process_reddening(dres, col, dis, slope, intercept, flag):# later called by reddening_error()
    mu_df_list = []
    ext0_df = pd.DataFrame({'name': dres['name'], 'logP': dres['logP'], 'EBV': dres['EBV']})
    red0_df = ext0_df.copy()
    print(f'  → For {flag} method and color {col}') #
    print(f'     rho \t    1 - rho')
    for m, band in enumerate(mag):
        wm_str, ext0_list, red0_list, mu_rd_ex_df = error_over_mu(dres, m, dis, col, slope, intercept, flag)
        ext0_df[f'ex_{wm_str}{dis}'] = ext0_list
        red0_df[f'rd_{wm_str}{dis}'] = red0_list
        mu_df_list.append(mu_rd_ex_df)
    return mu_df_list, ext0_df, red0_df                                           
#####################################################################
def error_reddening(dres, dmc, del_mu=del_mu,z=z, wes_show=wes_show, dis_flag = dis_flag, plots=plots, flags = flags, s=s):
    mu_df_list_dict = {}     # 4 col x 2 flags in dict of list of mu_rd_df
    ex_df = pd.DataFrame({'name': dres['name'], 'logP': dres['logP'], 'EBV': dres['EBV']})
    rd_df = ex_df.copy()
    for dis in dis_flag: 
        slope, intercept = select_regression_parameters(dmc, dis) # lists of del-del slope and intercept 
        print(f'\nDistance: {dis}\nWesenheit colors:')
        for col in wes_show:   
            print(f'\t {col}')
            for flag in flags:
                mu_df_list, ext0_df, red0_df = process_reddening(dres, col, dis, slope, intercept, flag)
                mu_df_list_dict[f'{col}_{flag}{dis}'] = mu_df_list
                ex_df = pd.merge(ex_df, ext0_df[[cl for cl in ext0_df.columns if cl not in ex_df.columns or cl == 'name']], on='name')
                rd_df = pd.merge(rd_df, red0_df[[cl for cl in red0_df.columns if cl not in rd_df.columns or cl == 'name']], on='name')
    if s == 1:
        ex_df.to_csv(f'{data_out}{process_step[3]}{len(ex_df)}_ext_err0.csv', index=False)
        rd_df.to_csv(f'{data_out}{process_step[3]}{len(rd_df)}_red_err0.csv', index=False)
    if plots == 1:
        for i in range(0, len(dres),plot_every_n_star):                                                                  
            for d in dis_flag:
                for ab in mode:
                    for col in wes_show:                                                                   
                        print(i,d,ab, col)
                        plot_star_rd0(i, rd_df, col, flags, ab, d)
    return ex_df,rd_df, mu_df_list_dict
#####################################################################    
def plot_star_rd0(i, red0, col, flag, ab, dis = dis_flag[0], s=s):
    plt.figure(figsize=(7, 2))  # width=10, height=5 (in inches)
    for f in flag:
        rd = [red0[f"rd_{m}{ab}{m if f == 'S' else col[0]}{col}{dis}"].iloc[i] for m in mag]
        plt.plot([x for x in range(len(mag))], rd, '-o', label = f)
    #plt.ylim(-0.2, 0.2)
        plt.axhline(y=np.mean(rd), color='gray', linestyle='--')
        plt.annotate(f'avg: {np.mean(rd):.3f}', xy=(len(mag)-1, np.mean(rd)), xytext=(5, 0), textcoords='offset points', va='bottom', ha='right', fontsize=10, color='black')
        plt.xticks(ticks=range(len(mag)), labels=mag)  # Set x-axis ticks to values in mag
        plt.suptitle(f'{i} {red0.name.iloc[i]} ({col})')
    plt.ylabel('Reddening Error')
    plt.legend()
    if s == 1:
        imgsave(file_name + f"_{i}_{col}_{ab}", 3, fil='pdf', p=1)
    plt.show()
#####################################################################    
def plot_star_rd0SM(i, red0, col, ab, dis = dis_flag, s=s):
    plt.figure(figsize=(7, 2))  # width=10, height=5 (in inches)
    for dis in dis_flag:
        rd = [red0[f"rd_{m}{ab}{m}{col}{dis}"].iloc[i] for m in mag]
        plt.plot([x for x in range(len(mag))], rd, '-o', label = f'S : {np.mean(rd) :.3f}')
        plt.axhline(y=np.mean(rd), color='blue', linestyle='--')
    #plt.annotate(f'avg: {np.mean(rd):.3f}', xy=(len(mag)-1, np.mean(rd)), xytext=(5, 0), textcoords='offset points', va='bottom', ha='right', fontsize=10, color='black')
        rd = [red0[f"rd_{m}{ab}{col[0]}{col}{dis}"].iloc[i] for m in mag]
        plt.plot([x for x in range(len(mag))], rd, '-*', label = f'M : {np.mean(rd) :.3f}')
        plt.axhline(y=np.mean(rd), color='orange', linestyle='--')
    #plt.annotate(f'avg: {np.mean(rd):.3f}', xy=(len(mag)-1, np.mean(rd)), xytext=(5, 0), textcoords='offset points', va='bottom', ha='right', fontsize=10, color='black')
    plt.xticks(ticks=range(len(mag)), labels=mag)  # Set x-axis ticks to values in mag
    plt.suptitle(f'{red0.name.iloc[i]} ({col})')
    #plt.ylim(-0.2, 0.2)
    plt.ylabel('Reddening Error')
    plt.legend()
    if s == 1:
        imgsave(file_name + f"rd{''.join(dis_flag)}_{i}_{col}_{ab}SM", 3, fil='pdf', p=1)
    plt.show()

def plot_star_rd0SM_apj(i, red0, col, ab, dis_flag=dis_flag, s=s):
    plt.rcParams.update({
        "font.size": 11,
        "axes.linewidth": 1,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.top": True,
        "ytick.right": True})
    fig, axes = plt.subplots(1, len(dis_flag), figsize=(8,3.5), sharey=True)
    for ax, dis in zip(axes, dis_flag):
        rd_S = np.array([red0[f"rd_{m}{ab}{m}{col}{dis}"].iloc[i] for m in mag])
        rd_M = np.array([red0[f"rd_{m}{ab}{col[0]}{col}{dis}"].iloc[i] for m in mag])
        x = np.arange(len(mag))
        ax.plot(x, rd_S, 'o-', color='black', ms=4, lw=1, label=f'S: {np.mean(rd_S):.3f}')
        ax.plot(x, rd_M, 's-', color='tab:blue', ms=4, lw=1, label=f'M: {np.mean(rd_M):.3f}')
        ax.axhline(np.mean(rd_S), color='black', ls='--', lw=0.8, alpha=0.7)
        ax.axhline(np.mean(rd_M), color='tab:blue', ls='--', lw=0.8, alpha=0.7)
        ax.set_title(dis_label[dis_flag.index(dis)])
        ax.set_xticks(x)
        ax.set_xticklabels(mag)
        ax.set_xlabel("Band")
        ax.legend(frameon=False)
    axes[0].set_ylabel("Reddening Error")
    fig.suptitle(f"{red0.name.iloc[i]} ({col}) | E(B-V) = {red0.EBV.iloc[i]}", y=1.02)
    plt.tight_layout()
    if s == 1:
        imgsave(file_name + f"rd{''.join(dis_flag)}_{i}_{col}_{ab}SM", 3, fil='pdf', p=1)
    plt.show()

#####################################################################
print(f'* * {module} module loaded!')
