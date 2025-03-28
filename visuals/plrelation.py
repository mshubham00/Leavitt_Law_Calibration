### ./visuals/plrelation.py

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from lvtlaw.utils import save, mag, img_out_path, process_step, col_das, col_lin, abs_bands, col_dot,wes_cols
from visuals.dataload import raw, absolute, PLWresidue
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio  

######################################################

def PLmc(dmc, title = 'slope_intercept', path = img_out_path+process_step[1]):
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
        y = dmc.mg.iloc[6*i:i*6+6]
        err_y = dmc.err_mg.iloc[6*i:(i+1)*6]  # Extract error values
        we = f"{dmc.name.iloc[6*i][1:]}"  # Proper LaTeX formatting    #print(x,y,we)
        fig.add_trace(go.Scatter(x=x_jittered, y=y, 
            error_y=dict(type='data', array=err_y, visible=True), name=we), row=1, col=1)
#fig.add_trace(go.Scatter(x=[1, 2], y=[1, 2],mode="markers", name="(1,2)"), row=1, col=2)
    for i in range(7,11):
        x_jittered = x + np.random.uniform(-0.2, 0.2, size=len(x))
        y = dmc.mg.iloc[6*i:i*6+6]
        err_y = dmc.err_mg.iloc[6*i:(i+1)*6]  # Extract error values
        we = '%s'%dmc.name.iloc[i*6][1:]
    #print(x,y,we)
        fig.add_trace(go.Scatter(x=x_jittered, y=y, 
            error_y=dict(type='data', array=err_y, visible=True), name=we), row=3, col=1)
    for i in range(11,14):
        x_jittered = x + np.random.uniform(-0.2, 0.2, size=len(x))
        y = dmc.mg.iloc[6*i:i*6+6]
        err_y = dmc.err_mg.iloc[6*i:(i+1)*6]  # Extract error values
        we = '%s'%dmc.name.iloc[i*6][1:]
    #print(x,y,we)
        fig.add_trace(go.Scatter(x=x_jittered, y=y, 
            error_y=dict(type='data', array=err_y, visible=True), name=we), row=5, col=1)
    for i in range(14,17):
        x_jittered = x + np.random.uniform(-0.2, 0.2, size=len(x))
        y = dmc.mg.iloc[6*i:i*6+6]
        err_y = dmc.err_mg.iloc[6*i:(i+1)*6]  # Extract error values
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
    fig, axarr = plt.subplots(2, sharex='col',gridspec_kw={'hspace': 0, 'wspace': 0})
    fig = plt.gcf()
    fig.set_size_inches(9, 6)
    X = res_data['logP']
    for i,ax in enumerate(axarr):
        if i ==0:
            for j in range(0,6):
                ax.plot(res_data.logP, res_data['r0_'+mag[j]+'_g'], col_lin[j], label = mag[j])
            ax.text(res_data.logP.iloc[40], 0.6, 'PL Residue with Gaia')

        elif i ==1:
            for j in range(0,6):
                ax.plot(res_data.logP, res_data['r0_'+mag[j]+'_i'], col_lin[j], label = mag[j])
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

