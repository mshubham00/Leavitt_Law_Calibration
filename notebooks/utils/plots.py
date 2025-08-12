import matplotlib.pyplot as plt
import pandas as pd
import statistics
#from scipy import stats
from utils.utils import *

def plot(x,y,col: int, xlable: str, s=0, ant = []):
    plt.figure(figsize=(5,5))
    plt.scatter(x, y, c= col)
    for i in ant:
        plt.annotate('%s'%(data.name.iloc[i]), xy =(x.iloc[i], y.iloc[i])) 
    plt.colorbar() 
    #plt.gca().invert_yaxis()
    plt.xlabel(xlable)
    if s==1:
        save(xlable)
    plt.show()


def plot_corr(df, Y, title, s=0, f=12):
    # To visualize first row of seaborn pairplot
    plt.figure()
    sns.set_context("paper", rc={"axes.labelsize":f})
    sns.pairplot(data=df, x_vars=df.columns[::], y_vars=Y, kind = 'scatter')
    if s==1:
        save(title)
#    plt.title(title)
    plt.show()




def plot_pair(data_arr, title, s=0):
    plt.figure() 
    g = sns.PairGrid(data_arr)
    g.map_upper(sns.scatterplot)
    g.map_lower(sns.kdeplot)
    g.map_diag(sns.kdeplot, lw=3, legend=False)
    if s==1:
        save(title)
    plt.show()
    plt.figure()
    sns.heatmap(data.select_dtypes(include = 'number').corr(), annot=True)
    if s==1:
        save('heat%s'%(title))
    plt.savefig()
    plt.show()

def pltfill(x, y1,y2,col):
    area = f'{np.trapz(np.abs(y2 - y1), x):.2f}'
    plt.plot(x, y1, col+'--')
    plt.plot(x, y1, col+'--')
    plt.fill_between(x,  y1, y2, alpha=.5, color=col)
    mid_x = (x.iloc[0] + x.iloc[-1]) / 2
    mid_y = (np.max(y1) + np.min(y2)) / 2
    return area
    #plt.text(-0.5, mid_y, f'{np.trapz(np.abs(y2 - y1), x):.2f}', ha='center', fontsize=8)

def plottransformation(c1 = 'JH', c2 = 'HK', title = 'magnitude_comparision', s=1):
    plt.figure(figsize=(6,6))
    disg = '_g'
    data['logP'] = data['logP']-1
    raw['logP'] = raw['logP']-1
    for i in range(0,1):
        jh = pltfill(data['logP'], w[mag[0]+c1+disg],w[mag[5]+c1+disg],'g')
        hk = pltfill(data['logP'], w[mag[0]+c2+disg],w[mag[5]+c2+disg],'c')
        tabs = pltfill(data['logP'], data[bands[0]+'0'],data[bands[5]+'0'],'y')
        ra = pltfill(raw['logP'], raw[ap_bands[0]],raw[ap_bands[5]],'r')
        abs = pltfill(raw['logP'], data[bands[0]+'0'] + data['plx'],data[bands[5]+'0'] + data['plx'],'m')
        plt.text(0, -10.4, f'Wesenheit Magnitude ({c1}) : {hk}', color='g')
        plt.text(0.52, -7.0, f'({c2})  : {hk}', color='k')
        plt.text(0, -2.2, f'True Absolute Magnitude  : {tabs}',color='grey')
        plt.text(0, 14.2, f'Apparent Magnitude : {ra}',color='red')  
        plt.text(0, 2.5, f'True Apparent Magnitude : {abs}',color='m')
    plt.xlabel('Period (logP-1)')
    plt.ylabel('Luminosity')
    plt.gca().invert_yaxis()
    if s ==1:
        save(title)


def plotreg(x_data, y_data, label = '', x_axis_str='x', y_axis_str='y', index=0, y_invert_flag_1=0, s=0):
    slope, intercept, prediction,residue, slope_error, intercept_error = regression(x_data, y_data, x_axis_str, y_axis_str)
#    intercept, slope, prediction, residue, slope_error, intercept_error = regression(x_data, y_data, nil1, nil2, x_name, y_name)
    model =  '%s = %f ($\pm$ %f) %s + %f ($\pm$ %f)'%(y_axis_str, slope, slope_error, x_axis_str, intercept, intercept_error)
    plt.plot(x_data, prediction , col_lin[index])
    plt.plot(x_data, y_data , col_dot[index], label = label)
    plt.annotate(label,(x_data[0] - 0.04,prediction[0]-0.08), fontsize=12)
    if y_invert_flag_1==1:
        plt.gca().invert_yaxis()
    return model

def compare_pl(data, correction, band, flag, dis):
    plt.figure(figsize=(5,8))
    model = plotreg(data.logP, data[f'M_{band}0{dis}'], label = f'${band}^0$')
    cols = color_index()
    for i, c in enumerate(cols):
        plotreg(correction.logP, correction[f'{band}{flag}{c}{dis}']+i+2, index=i%7, label = f'{c}')
    plt.title(band + f' band ({flag}) calibration', fontsize = 13)
    #plt.legend()
    #plt.show()

def plot_mu_red_col(star, cols, data_load , cepheid, data, err, dis,s=0):
    a,b = pick_star(star, data_load, cepheid)
    plt.figure(figsize=(8,8))
#    plt.xlim(-0.5, 0.5)  # Set x-axis range
#    plt.ylim(-0.3, 0.3) 
    x = []
    y = []
    for c1 in cols:
        plt.plot(err[f'muS{c1}{dis}'].iloc[star],err[f'rdS{c1}{dis}'].iloc[star], 'rx')
        plt.plot(err[f'muM{c1}{dis}'].iloc[star],err[f'rdM{c1}{dis}'].iloc[star], 'b+')
        x.append(err[f'muS{c1}{dis}'].iloc[star])
        y.append(err[f'rdS{c1}{dis}'].iloc[star])
        plt.annotate(c1,(err[f'muS{c1}{dis}'].iloc[star],err[f'rdS{c1}{dis}'].iloc[star]), fontsize=12)
        plt.annotate(c1,(err[f'muM{c1}{dis}'].iloc[star],err[f'rdM{c1}{dis}'].iloc[star]), fontsize=12)
#    plt.plot(err['muSBV'].iloc[star],err['rdSBV'].iloc[star], 'k<', label = '$W_{BV}$')
#    plt.plot(err['muSHK'].iloc[star],err['rdSHK'].iloc[star], 'k>', label = '$W_{HK}$' )
    xstd = statistics.stdev(x)
    ystd = statistics.stdev(y)
    #plotreg(x,y)
    #plt.legend()
    plt.xlabel(f'Distance $\delta \mu$ {xstd}', fontsize=11)
    plt.ylabel(f'Reddening $\delta EBV$ {ystd}', fontsize=11)
    plt.title(f'{star} {data.name.iloc[star]}', fontsize=13)
    title = f'stars/{cepheid}_{star}'
    if s == 1:
        save(title)  # Assuming 'save()' function is defined elsewhere
    #plt.show()


