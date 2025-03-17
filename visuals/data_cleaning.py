### ./visuals/data_cleaning.py
# using period-color creteria for finding outliers.
# list of useful color index
#ls = ['BI','VI']#
outliers = [0,7,8,67,81,83,85] 
ls = ['BV', 'BI', 'BK', 'VI','VJ','VK','IJ', 'IH', 'IK', 'JH', 'JK', 'HK']
import matplotlib.pyplot as plt
import pandas as pd
import os
import subprocess
import seaborn as sns

img_out_path = '../data/output/9_plots/'
process_step = ['1_datacleaning/','2_PLPW/','3_deldel/', '4_reddening/', '5_dispersion/','6_rms/','7_errorpair/', '8_result/']

def output_directories(parent_folder = img_out_path, s=1,subdirectories = process_step):
    if s==1:
        for subdirectory in subdirectories:
            path = os.path.join(parent_folder, subdirectory)
            if not os.path.exists(path):
                os.makedirs(path)

output_directories(s=1)

raw_data = pd.read_csv('../data/input/103_raw_data_IRSB.csv')
color=pd.read_csv('../data/input/103_color.csv')
print(raw_data.info(), color.info())

def savefigure(title):
    img_path = '../data/output/9_plots/'
    plt.savefig('%s%s.pdf'%(img_path,title))
   
def plot_outliers(ls = ls, outliers=outliers, s=0, a= 1, color = color):
    for j in range(0,len(ls),2):
        fig, axarr = plt.subplots(1,2, sharey='col',gridspec_kw={'hspace': 0, 'wspace': 0})
        fig = plt.gcf()
        fig.set_size_inches(15, 6)
        Y = color['logP']
        for i,ax in enumerate(axarr):
            X = color[ls[i+j]]
            pcm = ax.scatter(X, Y, label='$%s$'%(ls[i+j]), s=raw_data['mM0_IRSB'], c = raw_data['EBV'])
            ax.yaxis.tick_right()
            if i%2 ==0:
                ax.set_ylabel('Period')
            for k in outliers:
                ax.annotate('%s'%(raw_data.Name.iloc[k]), xy =(X.iloc[k]-0.05, Y.iloc[k]+0.02), fontsize = 11) 
            plt.text(0.05, 0.85, '%s'%(ls[i+j]), transform = ax.transAxes, color = "red",  fontsize = 14)      
        if s==1:
            savefigure('%sPC%i_%s'%(process_step[a],j,ls[i+j]))
    ax.yaxis.tick_left()
    cbar=fig.colorbar(pcm, ax=axarr[1], shrink=1, location='left')
    #cbar.set_label('Color Excess')
    plt.show()

plot_outliers(s=0)
