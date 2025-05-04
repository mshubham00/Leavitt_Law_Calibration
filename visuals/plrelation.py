### ./visuals/plrelation.py

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from lvtlaw.a_utils import save, mag, img_out_path, process_step, col_das, col_lin, abs_bands, col_dot,wes_cols, dis_flag, pr_value
from visuals.dataload import raw, transformation, PLWcorrection
#import plotly.graph_objects as go
#from plotly.subplots import make_subplots
#import plotly.io as pio  

absolute, extinction, tabsolute, wesenheit = transformation()
PLWdata, PLWresidue, PLWregression, PLWprediction = PLWcorrection()
######################################################

def PLmc(dmc, title = 'slope_intercept', path = img_out_path+process_step[1]):
    dmc = dmc.T
    dmc.columns = dmc.iloc[0]
    dmc = dmc.drop(dmc.index[0])
    fig = make_subplots(
        rows=8, cols=4,
        specs=[[{"rowspan": 2, "colspan": 4}, None, None, None],
           [ None, None, None, None],
           [{"rowspan": 2,"colspan": 4}, None, None, None],
           [ None, None, None, None],
           [{"rowspan": 2,"colspan": 4}, None, None, None],
           [ None, None, None, None],
           [{"rowspan": 2,"colspan": 4}, None, None, None],
           [ None, None, None, None]],
        horizontal_spacing=0,
        shared_xaxes=True,  # Share the x-axis between subplots
        print_grid=True)
    x = list(range(0,6))
    for i in range(2,7):
        x_jittered = x + np.random.uniform(-0.2, 0.2, size=len(x))
        print(dmc)
        y = dmc.m_h.iloc[6*i:i*6+6]
        err_y = dmc.err_m_h.iloc[6*i:(i+1)*6]  # Extract error values
        we = 'x'#f"{dmc.name.iloc[6*i][1:]}"  # Proper LaTeX formatting    #print(x,y,we)
        fig.add_trace(go.Scatter(x=x_jittered, y=y, 
            error_y=dict(type='data', array=err_y, visible=True), name=we), row=1, col=1)
#fig.add_trace(go.Scatter(x=[1, 2], y=[1, 2],mode="markers", name="(1,2)"), row=1, col=2)
    for i in range(7,11):
        x_jittered = x + np.random.uniform(-0.2, 0.2, size=len(x))
        y = dmc.m_h.iloc[6*i:i*6+6]
        err_y = dmc.err_m_h.iloc[6*i:(i+1)*6]  # Extract error values
        we = '%s'%dmc.name.iloc[i*6][1:]
    #print(x,y,we)
        fig.add_trace(go.Scatter(x=x_jittered, y=y, 
            error_y=dict(type='data', array=err_y, visible=True), name=we), row=3, col=1)
    for i in range(11,14):
        x_jittered = x + np.random.uniform(-0.2, 0.2, size=len(x))
        y = dmc.m_h.iloc[6*i:i*6+6]
        err_y = dmc.err_m_h.iloc[6*i:(i+1)*6]  # Extract error values
        we = '%s'%dmc.name.iloc[i*6][1:]
    #print(x,y,we)
        fig.add_trace(go.Scatter(x=x_jittered, y=y, 
            error_y=dict(type='data', array=err_y, visible=True), name=we), row=5, col=1)
    for i in range(14,17):
        x_jittered = x + np.random.uniform(-0.2, 0.2, size=len(x))
        y = dmc.m_h.iloc[6*i:i*6+6]
        err_y = dmc.err_m_h.iloc[6*i:(i+1)*6]  # Extract error values
        we = '%s'%dmc.name.iloc[i*6][1:]
    #print(x,y,we)
        fig.add_trace(go.Scatter(x=x_jittered, y=y, 
            error_y=dict(type='data', array=err_y, visible=True), name=we), row=7, col=1)
    fig.add_annotation(
                text="B", 
                x=3, y=-3.4, showarrow=False, font=dict(size=14, color="black"),
                row=1, col=1
            )
    fig.add_annotation(
                text=f"V", 
                x=3, y=-3.4, showarrow=False, font=dict(size=14, color="black"),
                row=3, col=1
            )
    fig.add_annotation(
                text="I", 
                x=3, y=-3.4, showarrow=False, font=dict(size=14, color="black"),
                row=5, col=1
            )
    fig.add_annotation(
                text="J & H", 
                x=3, y=-3.4, showarrow=False, font=dict(size=14, color="black"),
                row=7, col=1
            )
#fig.update_xaxes(title_text="X Axis 1", row=1, col=1)
#fig.update_yaxes(title_text="Y Axis 1", row=1, col=1)
    fig.update_yaxes(autorange="reversed", row=1, col=1)
    fig.update_yaxes(autorange="reversed", row=3, col=1)
    fig.update_yaxes(autorange="reversed", row=5, col=1)
    fig.update_yaxes(autorange="reversed", row=7, col=1)
    fig.update_xaxes(
        tickvals=x,  # Define tick positions
        ticktext=mag)
    fig.update_layout(height=600, width=600)
    pio.write_image(fig, path+title+'.pdf', format='pdf')
    fig.show()

def plotPL(i,a, ta, res, reg, pre, dis, s=0):
    m = mag[i]
    x = a['logP'] -1       
    y1 = a['M_'+m+dis]
    y2 = ta['M_'+m+'0'+dis]
    if dis == '_i':
        alpha = reg[m].iloc[4]
        gamma= reg[m].iloc[5]
    else:
        alpha = reg[:4][m].iloc[0]
        gamma= reg[:4][m].iloc[1]
    pred = pre['p_'+m+'0'+dis]
    residuals =  res['r_'+m+'0'+dis] 
    p1,r1 = pr_value(x,y1)
    p2,r2 = pr_value(x,y2)
    
# === Plotting ===
    fig, axs = plt.subplots(1, 3, figsize=(18, 4))

# 1. Deterministic model
#axs[0].plot(t, x1, 'k-', label='Deterministic: $s = vt$', marker='x')
    axs[0].scatter(x, y1, color='gray', s=a['EBV']*40, marker='o', label='%s Band | r = %f'%(mag[i], p1))
    #axs[0].set_title('Absolute Mag')
    axs[0].set_ylabel('Absolute Magnitude')
    axs[0].invert_yaxis()

# 2. Statistical model with linear regression fit
    axs[1].scatter(x, y2, color='gray', s=a['EBV']*40, label='%s Band | r = %f'%(mag[i], p2))
    axs[1].plot(x, pred, 'b-', label='$M_%s$ = %f (logP - 1) + %f'%(mag[i],alpha,gamma))
    for i in range(len(a)):
        if i == 0:
            label = "Distance-Reddening Error"
        else:
            label = None
        axs[1].plot([x[i], x[i]], [y2[i], pred[i]], color='red', linestyle='--', alpha=0.5, label=label)
    #axs[1].set_title(' Linear Fit')
    axs[1].invert_yaxis()
    axs[1].set_ylabel('True Absolute Magnitude')

# 3. Histogram of residuals
    label = 'Range: %f'%(max(residuals)-min(residuals))
    axs[2].hist(residuals, bins=15, edgecolor='black', color='steelblue', label =label)
    #axs[2].set_title('Histogram of Model Residuals')
    axs[2].set_xlabel('PL Residual (true - pred)')
    axs[2].set_ylabel('Count')
    axs[2].grid(True)
    axs[2].legend()

    for ax in axs[:2]:
        ax.set_xlabel('Period (logP - 1)')
        ax.grid(True)
        ax.legend()
        for spine in ax.spines.values():
            spine.set_visible(False)
            
    plt.tight_layout()
    title = '%i_PL_%s%s'%(len(x), m, dis)
    if s==1:
        save(title,1, fil = 'png', p=1)
    plt.show()

def plotPW(i, ta , w, col, res, reg, pre, dis, s=0):
# 1. Extracting x-y axis
    m = mag[i]
    x = ta['logP'] - 1       
    y1 = ta['M_' + m + '0' + dis]
    y2 = w[m + col + dis]
    p1,r1 = pr_value(x,y1)
    p2,r2 = pr_value(x,y2)
    if dis == '_i':
        alpha = reg[m].iloc[4]
        gamma = reg[m].iloc[5]
    else:
        alpha = reg[:4][m].iloc[0]
        gamma = reg[:4][m].iloc[1]
    pred = pre['p_' + m + col + dis]
    residuals =  res['r_' + m + col + dis] 
# === Plotting ===
    fig, axs = plt.subplots(1, 3, figsize=(18, 4))

# 1. Deterministic model
#axs[0].plot(t, x1, 'k-', label='Deterministic: $s = vt$', marker='x')
    axs[0].scatter(x, y1, color='gray', s=ta['EBV']*40, marker='o', label='%s Band | r = %f'%(mag[i], p1))
    #axs[0].set_title('Absolute Mag')
    axs[0].set_ylabel('True Absolute Magnitude')
    axs[0].invert_yaxis()

# 2. Statistical model with linear regression fit
    axs[1].scatter(x, y2, color='gray', s=ta['EBV']*40, label='$W_%s^{%s}$ Wesenheit | r = %f'%(mag[i],col, p2))
    axs[1].plot(x, pred, 'b-', label='$W_%s^{%s}$ = %f (logP - 1) + %f'%(mag[i],col,alpha,gamma))
    for i in range(len(ta)):
        if i == 0:
            label = "Distance Error"
        else:
            label = None
        axs[1].plot([x[i], x[i]], [y2[i], pred[i]], color='red', linestyle='--', alpha=0.5, label=label)
    #axs[1].set_title(' Linear Fit')
    axs[1].invert_yaxis()
    axs[1].set_ylabel('Wesenheit Magnitude')

# 3. Histogram of residuals
    label = 'Range: %f'%(max(residuals)-min(residuals))
    axs[2].hist(residuals, bins=15, edgecolor='black', color='steelblue',label = label)
    #axs[2].set_title('Histogram of Model Residuals')
    axs[2].set_xlabel('PW Residual (true - pred)')
    axs[2].set_ylabel('Count')
    axs[2].grid(True)
    axs[2].legend()

    for ax in axs[:2]:
        ax.set_xlabel('Period (logP - 1)')
        ax.grid(True)
        ax.legend()
        for spine in ax.spines.values():
            spine.set_visible(False)
            
    plt.tight_layout()
    title = '%i_%s_%s%s'%(len(x),col, m, dis)
    if s==1:
        save(title,1, fil = 'png', p=1)
    plt.show()




def pl6(data, PL_m,PL_c, PW_m,PW_c, path = img_out_path):
    plt.figure(figsize=(6,6))
    for i in range(0,6):
        plt.plot(data.logP-1, PL_m[i]*(data.logP-1) + PL_c[i], col_lin[i], label = mag[i])
    plt.plot(data['logP']-1, data[abs_bands[0]+'0_g'], 'b--')
    plt.plot(data['logP']-1, data[abs_bands[5]+'0_g'], 'g--')
    plt.gca().invert_yaxis()
    plt.xlabel('Period (in days)')
    plt.ylabel('Absolute Luminosity')
    plt.text(data.logP.iloc[4]-0.7, -9, 'Leavitt\'s Law in six bands')
    plt.legend()
    title = 'PL_relations'
    save(title,path, 1)
    plt.show()
    
    
def PLresidue(res_data, path = img_out_path):
    plot = len(dis_flag)
    fig, axarr = plt.subplots(plot, sharex='col',gridspec_kw={'hspace': 0, 'wspace': 0})
    fig = plt.gcf()
    fig.set_size_inches(9, 6)
    X = res_data['logP']
    for i,ax in enumerate(axarr):
        if i ==0:
            for j in range(0,6):
                ax.plot(res_data.logP, res_data['r_'+mag[j]+'0'+dis_flag[i]], col_lin[j], label = mag[j])
            ax.text(res_data.logP.iloc[40], 0.6, 'PL Residue with Gaia')

        elif i ==1:
            for j in range(0,6):
                ax.plot(res_data.logP, res_data['r_'+mag[j]+'0'+dis_flag[i]], col_lin[j], label = mag[j])
            ax.text(res_data.logP.iloc[40], 0.8, 'PL Residue with IRSB')
    plt.legend()
    plt.xlabel('Period (in days)')
    plt.ylabel('Residue')
    title = 'PL_residue'
    save(title,path, 1)
    plt.show()

def PWresidue(res_data, path = img_out_path):
    fig, axarr = plt.subplots(4, sharex='col',gridspec_kw={'hspace': 0, 'wspace': 0})
    fig = plt.gcf()
    fig.set_size_inches(9, 6)
    X = res_data['logP']
    print(res_data)
    for i,ax in enumerate(axarr):
            for j in range(0,6):
                ax.plot(res_data.logP, res_data['r_'+mag[j]+wes_cols[i]+'_g'], col_lin[j], label = mag[j])
            ax.text(res_data.logP.iloc[60], 0.45, 'PW Residue %s'%(wes_cols[i]))
    plt.legend()
    plt.xlabel('Period (in days)')
    plt.ylabel('Residue')
    title = 'PW_residue'
    save(title,path, 1)
    plt.show()

