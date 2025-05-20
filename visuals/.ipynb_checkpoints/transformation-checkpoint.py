### file: ./visuals/transformation.py

import matplotlib.pyplot as plt
import pandas as pd
import os
import subprocess
import seaborn as sns
from lvtlaw.a_utils import save, mag, img_out_path, process_step
from visuals.dataload import raw, transformation, PLWcorrection

########
df = raw[["logP", 'IRSB', 'EBV', "B_mag", 'V_mag', 'I_mag', 'J_mag', 'H_mag', 'K_mag']]

absolute, extinction, tabsolute, wesenheit = transformation()

data = absolute[["logP", 'plx', 'EBV', "M_B_g", 'M_V_g', 'M_I_g', 'M_J_g', 'M_H_g', 'M_K_g']]



def get_apparent(df, extinction):
    p= df['logP']
    b = df['B_mag']
    v = df['V_mag']
    i = df['I_mag']
    j = df['J_mag']
    h = df['H_mag']
    k = df['K_mag']
    w = df['B_mag'] - extinction['A_B']
    x = df['V_mag'] - extinction['A_V']
    y = df['I_mag'] - extinction['A_I']
    y1 = df['J_mag'] - extinction['A_J']
    y2 = df['H_mag'] - extinction['A_H']
    z = df['K_mag'] - extinction['A_K']

    fig, (ax0, ax1) = plt.subplots(1, 2, sharey=True, figsize=(12, 4))
    ax0.scatter(p, (df['plx'] - 7.5)/3.5, c = -df['plx'])
    ax0.plot(p, b)
    ax0.plot(p, v)
    ax0.plot(p, i)
    ax0.plot(p, j)
    ax0.plot(p, h)
    ax0.plot(p, k)
    ax1.plot(p, w, label='B')
    ax1.scatter(p, df['EBV']*1.5, c = -df['EBV'])
    ax1.plot(p, x, label='V')
    ax1.plot(p, y, label='I')
    ax1.plot(p, y1, label='J')
    ax1.plot(p, y2, label='H')
    ax1.plot(p, z, label='K')
    ax0.legend(loc='lower right')
    ax1.legend(loc='lower left')
    ax0.invert_yaxis()  
    ax0.grid(True, axis='y')
    ax1.grid(True, axis='y')

    ax0.annotate('Distance Indicator', 
                 xy=(1.8, 13), xycoords='data', 
                 xytext=(0.9, 0), textcoords='data',
                 fontsize=11, color='black')  
    ax1.annotate('Reddening Indicator', 
                 xy=(1, 4), xycoords='data', 
                 xytext=(0.9, 0), textcoords='data',
                 fontsize=11, color='black')  
# Adjust layout
    ax1.set_ylabel('True Apparent Magnitude')
    ax0.set_ylabel('Apparent Magnitude')
    fig.text(0.5, 0.01, 'Period (in log P)', ha='center', va='center', fontsize=12)
    plt.tight_layout()
    save('raw_data', img_out_path,0)
    plt.show()

def get_absolute(true_absolute):
    p= true_absolute['logP']
    d = '_i'
    w = true_absolute['M_B0'+d]
    x = true_absolute['M_V0'+d]
    y = true_absolute['M_I0'+d]
    y1 = true_absolute['M_J0'+d]
    y2 = true_absolute['M_H0'+d]
    z = true_absolute['M_K0'+d]
    d = '_g'
    w0 = true_absolute['M_B0'+d]
    x0 = true_absolute['M_V0'+d]
    y0 = true_absolute['M_I0'+d]
    y10 = true_absolute['M_J0'+d]
    y20 = true_absolute['M_H0'+d]
    z0 = true_absolute['M_K0'+d]

    fig, (ax0, ax1) = plt.subplots(1, 2, sharey=True, figsize=(12, 4))
    ax0.plot(p, w, label='B')
    ax0.plot(p, x, label='V')
    ax0.plot(p, y, label='I')
    ax0.plot(p, y1, label='J')
    ax0.plot(p, y2, label='H')
    ax0.plot(p, z, label='K')
    ax1.plot(p, w0, label='B')
    ax1.plot(p, x0, label='V')
    ax1.plot(p, y0, label='I')
    ax1.plot(p, y10, label='J')
    ax1.plot(p, y20, label='H')
    ax1.plot(p, z0, label='K')

    ax0.legend(loc='upper left')
    ax0.grid(True, axis='y')
    ax1.grid(True, axis='y')
    ax0.invert_yaxis()  

    ax0.annotate('IRSB Distance', 
                 xy=(1, -5), xycoords='data', 
                 xytext=(1.0, -8), textcoords='data',
                 fontsize=12, color='blue')  
    ax1.annotate('Gaia Distance', 
                 xy=(1, -5), xycoords='data', 
                 xytext=(1.0, -8), textcoords='data',
                 fontsize=12, color='blue')  
# Adjust layout
    ax0.set_ylabel('True Absolute Magnitude')
    fig.text(0.5, 0.01, 'Period (in log P)', ha='center', va='center', fontsize=12)
    plt.tight_layout()
    save('absolute_data', img_out_path,0)   
    plt.show()

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio  
def plt_wes_plotly(data, data2, w, d, title, path=img_out_path+process_step[1]):
    col = ['BV', 'VI', 'VK', 'JK']  # 4 columns (color)
    #mag = ['BV', 'VI', 'VK', 'JK', 'X1', 'X2']  # 6 rows (magnitude)
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'brown']

    # Create a 6x4 subplot grid (6 rows for mag, 4 columns for col)
    fig = make_subplots(rows=6, cols=4, shared_xaxes=True, shared_yaxes=True, 
                        horizontal_spacing=0.05, vertical_spacing=0.05)

    X = data['logP']

    for row_idx, mag_name in enumerate(mag):  # Loop over magnitude rows
        for col_idx, color in enumerate(col):  # Loop over color columns
            Y = data[f'M_{mag_name}0{d}']  # First dataset Y-values
            Z = data2[f'M_{mag_name}{d}']  # First dataset Y-values
            trace1 = go.Scatter(x=X, y=Y,
                                marker=dict(color='black'),
                                name=f"{mag_name} Data")
            trace3 = go.Scatter(x=X, y=Z,
                                marker=dict(color='grey'),
                                name=f"{mag_name} Data")

            Y_w = w[f'{mag_name}{color}{d}']  # Second dataset Y-values
            trace2 = go.Scatter(x=X, y=Y_w,
                                marker=dict(color=colors[row_idx]),
                                name=f"{mag_name} Model")

            fig.add_trace(trace1, row=row_idx+1, col=col_idx+1)
            fig.add_trace(trace2, row=row_idx+1, col=col_idx+1)
            fig.add_trace(trace3, row=row_idx+1, col=col_idx+1)

            # Add annotation (subplot title inside the plot)
            fig.add_annotation(
                text=f"{mag_name} - {color}", 
                xref='x domain', yref='y domain',
                x=0.5, y=0.95, showarrow=False, font=dict(size=14, color="black"),
                row=row_idx+1, col=col_idx+1
            )

    # Invert the y-axis for all subplots
    fig.update_yaxes(autorange="reversed")
    fig.add_annotation(
                text=f"{title}", 
                xref='x domain', yref='y domain',
                x=0.5, y=2, showarrow=False, font=dict(size=14, color="black"),
                row=1, col=2
            )


#    save('wesen_data', img_out_path,0)   
    # Update layout
    fig.update_layout(width=1000, height=800, showlegend=False)
    pio.write_image(fig, path+title+'.pdf', format='pdf')
    fig.show()

# Run the function



#get_apparent(df)

#get_absolute(true_absolute)
