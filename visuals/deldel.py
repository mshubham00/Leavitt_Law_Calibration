### ./visuals/deldel.py

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from lvtlaw.a_utils import save, mag, img_out_path, process_step, col_das, col_lin, abs_bands, col_dot,regression, dis_flag, wes_cols
#import plotly.graph_objects as go
#from plotly.subplots import make_subplots
#import plotly.io as pio  

def plotdeldel(i, ta, col, res, dSM, dis, s=0):
# 1. Extracting x-y axis
    m = mag[i]
    y = res['r_' + m + '0' + dis]
    x = res['r_' + m + col + dis]
    S = m + m + col
    pred = dSM[2][0]['p_' + S + dis]
    residuals =  dSM[1][0]['d_' + S + dis] 

    if dis == '_i':
        alpha = dSM[0][0][S].iloc[4]
        gamma = dSM[0][0][S].iloc[5]
    else:
        alpha = dSM[0][0][:4][S].iloc[0]
        gamma = dSM[0][0][:4][S].iloc[1]
# === Plotting ===
    fig, axs = plt.subplots(1, 2, figsize=(18, 4))
# 2. Statistical model with linear regression fit
    axs[0].scatter(x, y, color='gray', s=ta['EBV']*40, label='Residue Correlation: %s'%(S))
    for i in range(len(ta)):
        if i == 0:
            label = "Deviation"
        else:
            label = None
        axs[0].plot([x[i], x[i]], [y[i], pred[i]], color='red', linestyle='--', alpha=0.5, label=label)
    axs[0].plot(x, pred, 'g-', label=r'$\Delta$%s = %f $\Delta$%s%s + %f' % (m, alpha, m, col, gamma))
    axs[0].set_xlabel(r'PW residue ($\Delta$ %s)' % S[1:])
    axs[0].set_ylabel(r'PW residue ($\Delta$ %s)' % (m))
    # 3. Histogram of residuals
    label = 'Range: %f'%(max(residuals)-min(residuals))
    axs[1].hist(residuals, bins=15, edgecolor='black', color='green',label = label, alpha = 0.5)
    axs[1].set_xlabel('Residual (true - pred)')
    axs[1].set_ylabel('Count')
    axs[1].grid(True)
    axs[1].legend()
    for ax in axs[:2]:
        ax.grid(True)
        ax.legend()
        for spine in ax.spines.values():
            spine.set_visible(False)
    plt.tight_layout()
    title = '%i_del_%s_%s%s'%(len(x), col,m, dis)
    print(title)
    if s==1:
        save(title,2)
    plt.show()



def dmc(dmc_M,dmc_S, col=wes_cols, d='_g'):
    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(8, 6))
    fig = plt.gcf()
    fig.set_size_inches(9, 6)
    for j in range(4):
        for i in range(0,6):
            ax1.errorbar(j+0.1, dmc_S[mag[i]+mag[i]+col[j]].iloc[0], yerr=dmc_S[mag[i]+mag[i]+col[j]].iloc[2], fmt='o', capsize=3)
            ax1.errorbar(j-0.1, dmc_M[mag[i]+col[j][0]+col[j]].iloc[0], yerr=dmc_M[mag[i]+col[j][0]+col[j]].iloc[2], fmt='o', label='Data with Error Bars', capsize=3)
            #plt.plot(j-0.1,dmc_M[mag[i]+col[j][0]+col[j]].iloc[0], col_dot[i], label = mag[i])
            #plt.plot(j+0.1,dmc_S[mag[i]+mag[i]+col[j]].iloc[0], col_dot[i], label = mag[i])
            ax1.text(1.2,dmc_S[mag[i]+mag[i]+col[1]].iloc[0], '%s'%(mag[i]))
        ax1.text(j+0.1,-0.76, 'S')
        ax1.text(j-0.15,-0.76, 'M')

    #ax1.xticks(ticks=[0,1, 2, 3], labels=col)
    #plt.legend()
    ax1.grid()    
    ax2.grid()
    #ax1.xlabel('Bands (%s)'%(d))
    #ax1.ylabel('Slope (%s)'%(d))
    for j in range(4):
        for i in range(0,6):
            ax2.errorbar(j+0.1, dmc_S[mag[i]+mag[i]+col[j]].iloc[4], yerr=dmc_S[mag[i]+mag[i]+col[j]].iloc[6], fmt='o', capsize=3)
            ax2.errorbar(j-0.1, dmc_M[mag[i]+col[j][0]+col[j]].iloc[4], yerr=dmc_M[mag[i]+col[j][0]+col[j]].iloc[6], fmt='o', capsize=3)
            #plt.plot(j-0.1,dmc_M[mag[i]+col[j][0]+col[j]].iloc[0], col_dot[i], label = mag[i])
            #plt.plot(j+0.1,dmc_S[mag[i]+mag[i]+col[j]].iloc[0], col_dot[i], label = mag[i])
            ax2.text(1.2,dmc_S[mag[i]+mag[i]+col[1]].iloc[4], '%s'%(mag[i]))
        ax2.text(j+0.1,-0.76, 'S')
        ax2.text(j-0.15,-0.76, 'M')

    ax2.set_xticks(ticks=[0,1, 2, 3], labels=col)
    ax1.set_xticks(ticks=[0,1, 2, 3], labels=col)

    ax2.text(1.5,1.01, 'IRSB')
    ax1.text(1.5,1.01, 'Gaia')

    title = 'deldel'
    save(title,img_out_path, 2)
    plt.show()
    
def _residue(dres_M, dres_S, col='VK', mag=mag, col_lin=col_lin):
    print(dres_M, dres_S)
    #labels = ["B", "V", "I", "J", "H", "K"]
    fig, axes = plt.subplots(nrows=6,ncols=1, figsize=(8, 15), sharex=True)
    for ax, i, m in zip(axes, range(0,6), mag):
        ax.plot(dres_M['logP'], dres_M[f'r_{mag[i]}{col[0]}{col}_g'])
        ax.plot(dres_S['logP'], dres_S[f'r_{mag[i]}{mag[i]}{col}_g'])
        ax.plot(dres_M['logP'], dres_M[f'r_{mag[i]}{col[0]}{col}_i'])
        ax.plot(dres_S['logP'], dres_S[f'r_{mag[i]}{mag[i]}{col}_i'])
        #, c=df["EBV"], cmap="viridis", alpha=0.7, edgecolor="k"
        ax.set_ylabel(f"{m}")
        ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_xlabel(f"{col}")
    title = f'residue_{col}'
    save(title,img_out_path, 2)    
    #fig.subtitle("Period-Luminosity Relation in Multiple Bands")
    plt.show()

def residue(dres_M, dres_S, col='VK'):
    fig, axes = plt.subplots(nrows=6, ncols=2, sharex=True, sharey=True, figsize=(10, 12))
    for i in range(6):
        for j in range(2):
                axes[i, j].plot(dres_M['logP'], dres_M[f'r_{mag[i]}{col[0]}{col}{dis_flag[j]}'])
                axes[i, j].plot(dres_S['logP'], dres_S[f'r_{mag[i]}{mag[i]}{col}{dis_flag[j]}'])
                axes[i, j].text(1.6,0.3, '%s,%s'%(mag[i],col))
                axes[i, j].axhline(0, color='black', linewidth=1)
    axes[0, 0].text(1.3,2, 'Gaia')
    axes[0, 1].text(1.3,2, 'IRSB')
    #fig.suptitle('6 Rows, 2 Columns Subplot with Common Axes', fontsize=16)
    for ax in axes.flat:
        ax.set_ylabel('Y axis')
    ax.set_xlabel('X axis')
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust for suptitle space
    title = f'residue_{col}'
    save(title,img_out_path, 2)    
    plt.show()



def PLPWres(dres_M, dres_S, col='VK'):
    fig, axes = plt.subplots(nrows=6, ncols=2, sharex=True, sharey=True, figsize=(10, 12))
    for i in range(6):
        for j in range(2):
                axes[i, j].plot(dres_M[f'r_{mag[i]}{col[0]}{col}{dis_flag[j]}'], dres_M[f'r0_{mag[i]}{dis_flag[j]}'])
                axes[i, j].plot(dres_S[f'r_{mag[i]}{mag[i]}{col}{dis_flag[j]}'],dres_S[f'r0_{mag[i]}{dis_flag[j]}'])
                axes[i, j].text(1.6,0.3, '%s,%s'%(mag[i],col))
                axes[i, j].axhline(0, color='black', linewidth=1)
    axes[0, 0].text(1.3,2, 'Gaia')
    axes[0, 1].text(1.3,2, 'IRSB')
    #fig.suptitle('6 Rows, 2 Columns Subplot with Common Axes', fontsize=16)
    for ax in axes.flat:
        ax.set_ylabel('Y axis')
    ax.set_xlabel('X axis')
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust for suptitle space
    title = f'PLPWres_{col}'
    save(title,img_out_path, 2)    
    plt.show()

