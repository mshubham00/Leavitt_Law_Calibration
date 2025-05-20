### file: ./visuals/reddening.py

import matplotlib.pyplot as plt
import pandas as pd
from visuals.dataload import pick_star, correction_red_mu_stars
from lvtlaw.a_utils import wes_show, dis_flag, save, mag, img_out_path, process_step, col_lin, col_dot, del_mu, pr_value, col_das

def resultPL6(result, r_reg, r_res, r_pre, ta,res, reg, pre, col, dis, s=0):
    fig, axs = plt.subplots(2, 3, figsize=(18, 8), sharex='col')
    axs = axs.flatten()  # Flatten for easy indexing
    x = ta['logP'] - 1
    for i, m in enumerate(mag):
        y = ta['M_' + m + '0' + dis]
        y_cor = result[m + dis + col]
        # Get regression coefficients
        if dis == '_i':
            alpha = reg[m+'0'].iloc[4]
            gamma = reg[m+'0'].iloc[5]
            ralpha = r_reg[m+col].iloc[4]
            rgamma = r_reg[m+col].iloc[5]
        else:
            alpha = reg[m+'0'].iloc[0]
            gamma = reg[m+'0'].iloc[1]
            ralpha = r_reg[m+col].iloc[0]
            rgamma = r_reg[m+col].iloc[1]
        h = x*alpha + gamma
        rpre = r_pre['p_' + m + col + dis]
        rres = r_res['r_' + m + col + dis]
        pred = pre['p_' + m + '0' + dis]
        resd = res['r_' + m + '0' + dis]
        rcorr_coef, _ = pr_value(x, y_cor)
        corr_coef, _ = pr_value(x, y)
        ax = axs[i]
        ax.plot(x, y, col_dot[i], label=f'{m} Band | r = {corr_coef:.3f}')
        ax.plot(x, y_cor, 'ro', label=f'{m} Band | r = {rcorr_coef:.3f}')
        ax.plot(x, rpre, 'r-', label=f'$M_{m}^*$ = {ralpha:.3f}(logP - 1) + {rgamma:.3f}')
        ax.plot(x, h, col_das[i], label=f'$M_{m}$ = {alpha:.3f}(logP - 1) + {gamma:.3f}')
        # Residual lines
        for j in range(len(ta)):
            label = rf"$Residue = \delta \mu + R_{{m}} * E_{{BV}}$" if j == 0 else None
            #ax.plot([x[j], x[j]], [y[j], pred[j]], color='red', linestyle='--', alpha=0.5, label=label)
        ax.invert_yaxis()
        ax.set_ylabel('True Absolute Magnitude')
        ax.grid(True)
        ax.tick_params(direction='in', top=True, right=True)
        ax.legend()
        # Clean up spines
        for spine in ax.spines.values():
            spine.set_visible(False)
    # Set x-axis label only on bottom row
    for i, ax in enumerate(axs):
        if i >= 3:  # Bottom row
            ax.set_xlabel('Period (logP - 1)')
        else:
            ax.tick_params(labelbottom=False)
    plt.tight_layout()
    title = f'{len(ta)}_PL_{col}{dis}'
    if s == 1:
        save(title, 7, fil='png', p=1)
    plt.show()

def print_PL(reg, r_reg, dis):
    print('PL \t : \t Slope \t \t Intercept')
    for m in mag:
        if dis == '_i':
            alpha = reg[m+'0'].iloc[4]
            gamma = reg[m+'0'].iloc[5]
            em = reg[m+'0'].iloc[6]
            ec = reg[m+'0'].iloc[7]
        else:
            alpha = reg[m+'0'].iloc[0]
            gamma = reg[m+'0'].iloc[1]
            em = reg[m+'0'].iloc[2]
            ec = reg[m+'0'].iloc[3]
        
        print(f'\n \n Raw:\n{m}{dis} \t : {alpha} \t {gamma}')
        print(f'Error \t : {em} \t {ec} \n Calibrated:')
        #        print('\t \t :', alpha, gamma)
        for col in wes_show:
            if dis == '_i':
                ralpha = r_reg[m+col].iloc[4]
                rgamma = r_reg[m+col].iloc[5]
            else:
                ralpha = r_reg[m+col].iloc[0]
                rgamma = r_reg[m+col].iloc[1]
            print(f'{col} \t : {ralpha} \t {rgamma}')
        for col in wes_show:
            if dis == '_i':
                ealpha = r_reg[m+col].iloc[6]
                egamma = r_reg[m+col].iloc[7]
            else:
                ealpha = r_reg[m+col].iloc[2]
                egamma = r_reg[m+col].iloc[3]
            print(f'Error {col} : {ealpha} \t {egamma}')