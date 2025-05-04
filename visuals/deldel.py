### ./visuals/deldel.py

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from lvtlaw.a_utils import save, mag, img_out_path, process_step, col_das, col_lin, abs_bands, col_dot,regression, dis_flag, wes_cols
#import plotly.graph_objects as go
#from plotly.subplots import make_subplots
#import plotly.io as pio  

def plotdeldel_(col,d,res_data):
    fig, axarr = plt.subplots(6, sharex = True, gridspec_kw={'hspace': 0, 'wspace': 0})
    fig = plt.gcf()
    fig.set_size_inches(9, 6)
    for i,ax in enumerate(axarr):
        ax.plot(res_data['r_'+mag[i]+col+d],res_data['r0_'+mag[i]+d], col_dot[i], label = mag[i])
        ax.plot(res_data['r_'+col[0]+col+d],res_data['r0_'+mag[i]+d], 'k.', label = mag[i])
        ax.text(0.4, -0.5, '%s,%s'%(mag[i],mag[i]+col))
    plt.legend()
    plt.xlabel('PW Residue (%s)'%(d))
    plt.ylabel('PL Residue (%s)'%(d))
    title = '%s'%(col+d)
    save(title,2)
    plt.show()

def plotdeldel(i, ta, col, res, dSM, dis, s=0):
# 1. Extracting x-y axis
    m = mag[i]
    y = res['r_' + m + '0' + dis]
    
    x1 = res['r_' + col[0] + col + dis]
    M = m + col[0] + col
    predM = dSM[2][1]['p_' + M + dis]
    residualsM =  dSM[1][1]['d_' + M + dis] 

    x2 = res['r_' + m + col + dis]
    S = m + m + col
    predS = dSM[2][0]['p_' + S + dis]
    residualsS =  dSM[1][0]['d_' + S + dis] 

    if dis == '_i':
        alphaM = dSM[0][1][M].iloc[4]
        gammaM = dSM[0][1][M].iloc[5]
        alphaS = dSM[0][0][S].iloc[4]
        gammaS = dSM[0][0][S].iloc[5]
    else:
        alphaM = dSM[0][1][:4][M].iloc[0]
        gammaM = dSM[0][1][:4][M].iloc[1]
        alphaS = dSM[0][0][:4][S].iloc[0]
        gammaS = dSM[0][0][:4][S].iloc[1]
# === Plotting ===
    fig, axs = plt.subplots(1, 3, figsize=(18, 4))

# 1. Deterministic model
#axs[0].plot(t, x1, 'k-', label='Deterministic: $s = vt$', marker='x')
    axs[0].scatter(x1, y, color='gray', s=ta['EBV']*40, marker='o', label='Residue Correlation: %s'%(M))
    #axs[0].set_title('Absolute Mag')
    for i in range(len(ta)):
        if i == 0:
            label = "Madore"
        else:
            label = None
        axs[0].plot([x1[i], x1[i]], [y[i], predM[i]], color='red', linestyle='--', alpha=0.5, label=label)
    axs[0].plot(x1, predM, 'b-', label='$\Delta$%s = %f $\Delta$%s%s + %f'%(m,alphaM,col[0],col,gammaM))
    axs[0].set_ylabel('PL residue ($\Delta$ %s)'%(m))
    axs[0].set_xlabel('PW residue ($\Delta$ %s)'%(M[1:]))


# 2. Statistical model with linear regression fit
    axs[1].scatter(x2, y, color='gray', s=ta['EBV']*40, label='Residue Correlation: %s'%(S))
    for i in range(len(ta)):
        if i == 0:
            label = "Shubham"
        else:
            label = None
        axs[1].plot([x2[i], x2[i]], [y[i], predS[i]], color='red', linestyle='--', alpha=0.5, label=label)
    axs[1].plot(x2, predS, 'g-', label='$\Delta$%s = %f $\Delta$%s%s + %f'%(m,alphaS,m,col,gammaS))
    axs[1].set_xlabel('PW residue ($\Delta$ %s)'%(S[1:]))
#axs[1].set_title(' Linear Fit')

# 3. Histogram of residuals
    labelM = 'Range: %f'%(max(residualsM)-min(residualsM))
    labelS = 'Range: %f'%(max(residualsS)-min(residualsS))
    axs[2].hist(residualsM, bins=15, edgecolor='black', color='steelblue',label = labelM)
    axs[2].hist(residualsS, bins=15, edgecolor='black', color='green',label = labelS, alpha = 0.5)
    #axs[2].set_title('Histogram of Model Residuals')
    axs[2].set_xlabel('Residual (true - pred)')
    axs[2].set_ylabel('Count')
    axs[2].grid(True)
    axs[2].legend()

    for ax in axs[:2]:
        ax.grid(True)
        ax.legend()
        for spine in ax.spines.values():
            spine.set_visible(False)

    plt.tight_layout()
    title = '%i_del_%s_%s%s'%(len(x1), col,m, dis)
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

