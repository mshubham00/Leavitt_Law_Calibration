### File: plot.py

import matplotlib.pyplot as plt
import matplotlib 
import seaborn as sns
matplotlib.rcParams['savefig.dpi'] = 300
matplotlib.rcParams["figure.dpi"] = 100
from lvtlaw.utils import mag, bands, ap_bands, col_, color_index, img_out_path

def save(title, img_path = output_path):
    plt.savefig('%s2%s.pdf'%(img_path,title))

def vertical_7_colomn_plot(title: str, data, mag_name: list, sav: int, disg = '_g', disi = '_i'):
    fig, axarr = plt.subplots(6, sharex='col',gridspec_kw={'hspace': 0, 'wspace': 0})
    fig = plt.gcf()
    fig.set_size_inches(4,8)
    X = data['logP'] -1
    for i,ax in enumerate(axarr):
        Y = data[mag_name[i]+disi]
        ax.scatter(X, Y, label='$%s$'%(bands[i]), s=data['IRSB'], c = 'k')
        Y = data[mag_name[i]+disg]
        ax.scatter(X, Y, label='$%s$'%(bands[i]), s=data['plx'], c = data['EBV'])
        #ax.legend(loc='upper right', prop={'size':6})
        #ax.yaxis.tick_right()
        ax.annotate('$%s$'%(mag[i]), xy =(0.4, -4)) 
        #ax.invert_yaxis()
        ax.set_ylim([min(data[mag_name[5]+disg])-0.1, max(data[mag_name[0]+disg])+0.1])
        #ax.grid()
        ax.axvline(x=0, color='c', linestyle='--');
    ax.set_ylabel(title, fontsize=10)
    ax.set_xlabel('Period in days (logP -1), colored with reddening')
#ax.set_ylabel('asd')
# change y positioning to be in the horizontal center of all Nlayer, i.e. dynamically Nlayer/2
    ax.yaxis.set_label_coords(-0.1,3)
    #plt.gca().invert_yaxis()
    if sav==1:
        save(title)
    plt.show()

def matrix_plot(title: str, data, mag_name: list, sav: int):
    fig, axarr = plt.subplots(6, len(mag_name), sharex='col',gridspec_kw={'hspace': 0, 'wspace': 0})
    fig = plt.gcf()
    fig.set_size_inches(len(mag_name)*2,6)
    X = data['logP'] -1
    for j in range(0,len(mag_name)):
        for i,ax in enumerate(axarr):
            wes = mag[i]+mag_name[j]
            Y = data[wes]
            ax.scatter(X, Y, label='$%s$'%(wes), s=data[dis_mod], c = data['EBV'])
        #ax.legend(loc='upper right', prop={'size':6})
        #ax.yaxis.tick_right()
            ax.annotate('$%s$'%(mag[i]), xy =(0.4, -4)) 
        #ax.invert_yaxis()
            ax.set_ylim([min(data[mag[5]+mag_name[j]]), max(data[mag[0]+mag_name[j]])])
        #ax.grid()
        ax.axvline(x=0, color='c', linestyle='--');
    ax.set_ylabel(title, fontsize=10)
    ax.set_xlabel('Period in days (logP -1), colored with reddening')
#ax.set_ylabel('asd')
# change y positioning to be in the horizontal center of all Nlayer, i.e. dynamically Nlayer/2
    ax.yaxis.set_label_coords(-0.1,3)
    #plt.gca().invert_yaxis()
    if sav==1:
        save(title)
    plt.show()

def plot(x,y,col: int, xlable: str, sav=0, ant = []):
    #
    plt.figure(figsize=(5,5))
    plt.scatter(x, y, c= col_)
    for i in ant:
        plt.annotate('%s'%(data.name.iloc[i]), xy =(x.iloc[i], y.iloc[i])) 
    plt.colorbar() 
    #plt.gca().invert_yaxis()
    plt.xlabel(xlable)
    if sav==1:
        save(xlable)
    plt.show()


def plot_corr(df, Y, title, sav=0, f=12):
    # To visualize first row of seaborn pairplot
    plt.figure()
    sns.set_context("paper", rc={"axes.labelsize":f})
    sns.pairplot(data=df, x_vars=df.columns[::], y_vars=Y, kind = 'scatter')
    if sav==1:
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
     
