 ### File: ./lvtlaw/c_pl_pw.py
'''
This file deduded period-luminosity and period-wesenheit relations using prepared_regression_data DataFrame. (output of b_data_transform)

The output will be saved in 'data/{DatasetName_Rv}/1_prepared/*.csv'

Function contained:
    append_PLW(): This function collects all the processed information and store it in a list. 
    pl_dis(data, dis, mag): calculate regression for PL and PW relations and return residue, PLW and prediction 
    pl_reg(data, dis_flag, mag): save the output and returns dataframes
'''
module = 'c_pl_pw'
#####################################################################
from data.datamapping import R, mag, data_dir, file_name, dis_flag, data_out, dis_list, process_step, k, s, z, wes_show, nreg, col_dot, col_lin, mode
from lvtlaw.a_utils import regression, merge_12, pr_value,imgsave
import pandas as pd, numpy as np
from functools import reduce
import matplotlib.pyplot as plt
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
#####################################################################
def append_PLW(PLW_struct : list,name : str,m : float,c : float,p : list,r : list,me :float,ce :float,dis :str):
    # framing multiple regression output into one structure
    PLW_struct[0].append(name) 
    PLW_struct[1].append(m)
    PLW_struct[2].append(c)
    PLW_struct[3]['p_'+name+dis] = p   
    PLW_struct[4]['r_'+name+dis] = r
    PLW_struct[5].append(me)
    PLW_struct[6].append(ce)
    return PLW_struct
#####################################################################
def plw_relation(merged_data, dis: str, mag: list, wes_show = wes_show):
    residue = pd.DataFrame({'name': merged_data['name'], 'logP': merged_data['logP'], 'EBV': merged_data['EBV']})
    residue[dis_list[dis_flag.index(dis)]] = merged_data[dis_list[dis_flag.index(dis)]]
    prediction = residue.copy()   
    PL_name, PL_slope, PL_intercept, err_slope, err_intercept  = [], [], [], [], []
    PLW_struct = [PL_name, PL_slope, PL_intercept, prediction, residue, err_slope, err_intercept]    

    print('Leavitt Law : Absolute Magnitude \n#######  m  - mu = alpha (logP - 1) + gamma  #################\n')
    for ab in mode:
        for i in range(len(mag)):  # Iterate over magnitudes
            m, c, prediction, residue, m_error, c_error = regression(merged_data['logP'] - 1, merged_data['M_'+mag[i] + ab+ dis], '(logP - 1)', mag[i] + ab + dis, 1)
            PLW_struct = append_PLW(PLW_struct, mag[i]+ab, m, c, prediction, residue, m_error, c_error, dis)

    print('\nLeavitt Law : Wesenheit Magnitude \n#######  m - mu - R*(B-V) = alpha (logP - 1) + gamma     #####')
    for color in wes_show:
        print(f'\nWesenheit Magnitude for color index: {color} \n#######  m - mu - R*({color[0]} - {color[1]}) = alpha (logP - 1) + gamma     #####')
        for i in range(len(mag)):
            m, c, prediction, residue, m_error, c_error = regression(merged_data['logP'] - 1, merged_data[mag[i] + color + dis], '(logP - 1)', mag[i] + color + dis, 1)
            PLW_struct = append_PLW(PLW_struct, mag[i] + color, m, c, prediction, residue, m_error, c_error, dis)


    # Convert the results into a DataFrame
    PLW = pd.DataFrame({
        'name': PLW_struct[0],
        f'm{dis}': PLW_struct[1],
        f'c{dis}': PLW_struct[2],
        f'err_m{dis}': PLW_struct[5],
        f'err_c{dis}': PLW_struct[6]
    })
    prediction = PLW_struct[3]
    residue = PLW_struct[4]
    return PLW, residue, prediction
#####################################################################
def pl_reg(merged_data, s=s, dis_flag = dis_flag, mag = mag):
    reg = pd.DataFrame() # collecting slope and intercept parameter
    res = pd.DataFrame() # to collect residuals
    pre = pd.DataFrame() # to collect prediction
    for dis in dis_flag:
        PLW, residue, prediction = plw_relation(merged_data, dis, mag)
        res = pd.concat([res, residue], axis=1)
        pre = pd.concat([pre, prediction], axis=1)
        reg = pd.concat([reg, PLW], axis=1)
    res = res.loc[:, ~res.columns.duplicated()]
    pre = pre.loc[:, ~pre.columns.duplicated()]
    reg = reg.T
    reg.columns = reg.iloc[0]
    reg = reg.drop(reg.index[0])
    merged_data = merge_12(merged_data, res, on = ['name', 'logP', 'EBV'])
    merged_data = merge_12(merged_data, pre, on = ['name', 'logP', 'EBV'])
    if s==1:
        merged_data.to_csv('%s%i_merged_data.csv'%(data_out+process_step[1],len(res)))    
        res.to_csv('%s%i_residue.csv'%(data_out+process_step[1],len(res)))
        pre.to_csv('%s%i_prediction.csv'%(data_out+process_step[1],len(pre)))
        reg.to_csv('./%s%i_%i_regression.csv'%(data_out+process_step[1],len(res),nreg))
        print(f'\nData saved in ./{data_out+process_step[1]}')
    return reg, res, pre, merged_data
####################################################################################
def plotPL6(merged_data, reg, ab, dis=dis_flag[0], s=s):
    x = merged_data['logP'] - 1
    title = f"{file_name}_{ab}{''.join(mag)}{dis}"
    fig, axs = plt.subplots(2, 3, figsize=(18, 8), sharex='col')
    axs = axs.flatten()  # Flatten for easy indexing
    for i, m in enumerate(mag[0:6]):
        y = merged_data['M_' + m + ab + dis]
        # Get regression coefficients
        if dis == '_i':
            alpha = reg[m+ab].iloc[4]
            gamma = reg[m+ab].iloc[5]
        else:
            alpha = reg[m+ab].iloc[0]
            gamma = reg[m+ab].iloc[1]
        pred = merged_data['p_' + m + ab + dis]
        residuals = merged_data['r_' + m + ab + dis]
        r_std = round(residuals.std(ddof=0), 3)
        ax = axs[i]
        ax.plot(x, y, col_dot[i], label=f'{m+ab} Band | $\sigma$ = {r_std}')
        ax.plot(x, pred, col_lin[i], label=f'$M_{m+ab}$ = {alpha:.3f}(logP - 1) + {gamma:.3f}')
        # Residual lines
        for j in range(len(merged_data)):
            label = r"$Residue = \delta \mu + R_{%s} * E_{{BV}}$"%(m) if j == 0 else None
            ax.plot([x[j], x[j]], [y[j], pred[j]], color='red', linestyle='--', alpha=0.5, label=label)
        ax.invert_yaxis()
        if ab == '0':
            ax.set_ylabel('True Absolute Magnitude')
        else:
            ax.set_ylabel('Absolute Magnitude')
        #ax.grid(True)
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
    plt.suptitle(f'{title[3:-2]} Leavitt Law')
    plt.tight_layout()
    if s == 1:
        imgsave(title, step=1)
    plt.show()
    plotPLWres(merged_data, reg, ab, col='')
#####################################################################
def plotPW6(data, reg, col, dis=dis_flag[0], s=s):
    print('Wesenheit ', col)
    x = data['logP'] - 1
    title = f"{file_name}_{col}_{''.join(mag)}{dis}"
    fig, axs = plt.subplots(2, 3, figsize=(18, 8), sharex='col')
    axs = axs.flatten()
    for i, m in enumerate(mag[0:6]):
        w_str = m + col
        y = data[w_str + dis]
        p1, _ = pr_value(x, y)
        # Coefficients from regression
        if dis == '_i':
            alpha = reg[w_str].iloc[4]
            gamma = reg[w_str].iloc[5]
        else:
            alpha = reg[:4][w_str].iloc[0]
            gamma = reg[:4][w_str].iloc[1]
        pred = data['p_' + w_str + dis]
        residuals = data['r_' + w_str + dis]
        r_std = round(residuals.std(ddof=0), 3)
        # Plot
        ax = axs[i]
        ax.plot(x, y, col_dot[i], label=f'{w_str} Wesenheit | $\sigma$ = {r_std}')
        ax.plot(x, pred, col_lin[i], label=f'{w_str} = {alpha:.2f}(logP - 1) + {gamma:.2f}')

        # Residual lines
        for j in range(len(data)):
            label = r"$Residue = \delta \mu$" if j == 0 else None
            ax.plot([x[j], x[j]], [y[j], pred[j]], color='red', linestyle='--', alpha=0.5, label=label)
        #ax.grid(True)
        ax.invert_yaxis()
        ax.set_ylabel('Wesenheit Magnitude')
        ax.legend()

    # Set x-axis labels only on bottom row
    for i, ax in enumerate(axs):
        if i >= 3:
            ax.set_xlabel('Period (logP - 1)')
        else:
            ax.tick_params(labelbottom=False)
    plt.suptitle(f'{title[3:-2]} Wesenheit-Leavitt Law')
    plt.tight_layout()
    # Title
    if s == 1:
        imgsave(title, 1)
    plt.show()
    plotPLWres(data, reg, ab = '', col = col)
#####################################################################
def plotPLWres(res, reg, ab, col='', dis=dis_flag[0],s=s):
    x = res['logP'] - 1
    title = f"{file_name}_{''.join(mag)}_{col}{ab}{dis}"
    fig_res, axs_res = plt.subplots(2, 3, figsize=(18, 6))
    axs_res = axs_res.flatten()
    for i, m in enumerate(mag[0:6]):
        if dis == '_i':
            alpha_e = round(reg[m+ab+col].iloc[6], 3)
            gamma_e = round(reg[m+ab+col].iloc[7], 3)
        else:
            alpha_e = round(reg[m+ab+col].iloc[2], 3)
            gamma_e = round(reg[m+ab+col].iloc[3], 3)
        residuals = res['r_' + m + ab + col + dis]
        ax_res = axs_res[i]
        stdd = round(residuals.std(ddof=0), 3)
        ax_res.plot(x, residuals, col_dot[i], label=f'{m+ab} $ \\sigma = $ {stdd}')
        ax_res.axhline(2*np.std(residuals), color='gray', linestyle='--', linewidth=1)
        ax_res.axhline(0, color='red', linestyle='--', linewidth=1)
        ax_res.axhline(-2*np.std(residuals), color='gray', linestyle='--', linewidth=1)
        xlabel = f'Errors in slope: {alpha_e} | intercept: {gamma_e}'
        ax_res.set_xlabel(xlabel)
        ax_res.set_ylabel(f'{m+ab} Band Residuals')
        #ax_res.grid(True)
        ax_res.tick_params(direction='in', top=True, right=True)
        ax_res.legend()
        for spine in ax_res.spines.values():
            spine.set_visible(False)

    for j in range(len(mag[0:6]), 6):  # Hide any unused axes
        axs_res[j].set_visible(False)
    plt.tight_layout()
    plt.suptitle(f'{title[3:-2]} Residuals')
    if s == 1:
        imgsave(title + "_residuals", 1)
    plt.show()
#####################################################################
print(f'* * {module} module loaded!')
