### file: ./visuals/reddening.py

#from visuals.dataload import raw, absolute, wesenheit, dmc_S, extinction, tabsolute, PLWregression, PLWresidue

import matplotlib.pyplot as plt
import pandas as pd
from visuals.dataload import ext_g, ext_i, red_g, red_i, raw
from lvtlaw.utils import wes_cols, dis_flag, save, mag, img_out_path, process_step

def starbystar(star,t):
    name = raw['ID'].iloc[t]
    fig, axes = plt.subplots(nrows=4, ncols=2, sharex=True, figsize=(8, 9))
    for d in range(2):
        for c in range(4):
            savg = sum(star['E0'+wes_cols[c]+dis_flag[d]+'_S'])/len(mag)
            mavg = sum(star['E0'+wes_cols[c]+dis_flag[d]+'_M'])/len(mag)
            axes[c,d].axhline(savg, color='blue', linewidth=1)
            axes[c,d].axhline(mavg, color='red', linewidth=1)
            axes[c,d].plot([x for x in range(6)], star['E0'+wes_cols[c]+dis_flag[d]+'_S'], label = 'S')
            axes[c,d].plot([x for x in range(6)], star['E0'+wes_cols[c]+dis_flag[d]+'_M'], label = 'M')
            axes[c,d].text(1,savg, '$\delta E_S$ = %f'%(savg))
            axes[c,d].text(3,mavg, '$\delta E_M$ = %f'%(mavg))
    axes[3,0].set_xlabel('Gaia')
    axes[3,1].set_xlabel('IRSB')
    axes[0,0].set_xlabel('%i %s'%(t, name))
    axes[0,1].set_xlabel('E(B-V) = %f'%(raw['EBV'].iloc[t]))
    for i in range(4):
        axes[i,0].set_ylabel('%s'%(wes_cols[i]))
#    axes.set_xticks(ticks=[0,1, 2, 3,4,5], labels=mag)
    plt.tight_layout()  # Adjust for suptitle space
    title = f'star_{t}'
    save(title,img_out_path, 3, 'pdf')    
    #plt.show()
