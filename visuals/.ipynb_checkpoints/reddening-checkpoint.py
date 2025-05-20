### file: ./visuals/reddening.py

import matplotlib.pyplot as plt
import pandas as pd
from visuals.dataload import pick_star, correction_red_mu_stars
from lvtlaw.a_utils import wes_show, dis_flag, save, mag, img_out_path, process_step, col_lin, col_dot, del_mu

def plotstar(j, cols, dis, s=0):
# 1. Extracting x-y axis
    abs_del,mu_rd = pick_star(j)
    x = del_mu
    c = correction_red_mu_stars()
    fig, axs = plt.subplots(2, 2, figsize=(13, 5), sharex='col')
    axs = axs.flatten()  # Flatten for easy indexing
    for k, col in enumerate(cols):
        mu = c['mu'+dis+col].iloc[j]
        E = c['rd'+dis+col].iloc[j]
# === Plotting ===
        ax = axs[k]
        for i in range(len(mag)):
            ys = mu_rd[[col+dis+'rd'+str(mu) for mu in del_mu]].iloc[i].values   
            ax.plot(x, ys, col_lin[i], label='%s'%(mag[i]))
        ax.plot(mu, E, 'ko') 
        ax.axhline(y=E, color='gray', linestyle='--')
        ax.annotate(f'{E:.2f}', xy=(x[-1], E), xytext=(5, 0), textcoords='offset points', va='bottom', ha='right', fontsize=10, color='black')
        ax.axvline(x=mu, color='gray', linestyle='--')
        ax.annotate(f'{mu:.2f}', xy=(mu, axs[1].get_ylim()[0]), xytext=(0, 5), textcoords='offset points', va='top', ha='left', fontsize=10, color='black')
        ax.set_xlabel(r'$\Delta \mu - %s$'%(col))
        ax.set_ylabel(r'$\Delta E_{BV}$')
    ax.legend()
    for ax in axs:
#        ax.legend()
        for spine in ax.spines.values():
            spine.set_visible(False)
    plt.tight_layout()
    title = '%i_%i_star_%s%s'%(len(c), j, col, dis)
    print(title)
    if s==1:
        save(title,5,fil='png', p=1)
    plt.show()
