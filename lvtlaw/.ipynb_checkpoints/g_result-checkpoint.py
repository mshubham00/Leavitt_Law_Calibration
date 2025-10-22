### File: ./lvtlaw/g_result.py
'''
This file 

The output will be saved in 'data/{DatasetName_Rv}/1_prepared/*.csv'

Function contained:
    correction_apply()
    append_PLW()
    corrected_PL()
    corrected_reg()
    plotresultPL6()
'''
module = 'g_result'
from data.datamapping import s,plots, flags, dis_flag, wes_show, mag, process_step, data_out, dis_list, col_dot, col_das, R, nreg, mode
from lvtlaw.a_utils import regression, pr_value, imgsave, merge_12
import pandas as pd
import matplotlib.pyplot as plt

def correction_apply(data, correction, wes_show=wes_show, flags=flags, dis_flag=dis_flag, s=s):
    corrected = pd.DataFrame({'name': data.name, 'logP': data['logP']})
    for d in dis_flag:
        for f in flags:
            for col in wes_show:
                for ab in mode:
                    corrected['EBV'+f+ab+col+d]  = data['EBV'] - correction['rd'+f+ab+col+d]
                    corrected['mu'+f+ab+col+d] = data[dis_list[dis_flag.index(d)]] + correction['mu'+f+ab+col+d]
                    for m in mag:
                        corr_ex_mu = - R[m]*correction['rd'+f+ab+col+d] + correction['mu'+f+ab+col+d] # 
                        corrected[m+f+ab+col+d]=data['M_'+m+ab+d] + corr_ex_mu
    if s==1:
        corrected.to_csv('%s%i_corrected.csv'%(data_out+process_step[7],len(corrected)))
    return corrected

def append_PLW(PLW_struct : list,i : int,a : float,b : float,c : list,d : list,e :float,f :float, dis):
    # collect different regression output into one structure
    PLW_struct[0].append(i)    # PL_name
    PLW_struct[1].append(a)    # slope
    PLW_struct[2].append(b)    # intercept
    PLW_struct[3]['p_'+i+dis ] = c   # PL prediction
    PLW_struct[4]['r_'+i+dis ] = d   # PL residue
    PLW_struct[5].append(e)    # slope error
    PLW_struct[6].append(f)    # intercept error
    return PLW_struct


def corrected_PL(data, corrected, dis, flag, s=1):
    PL_name, PL_slope, PL_intercept = [], [], []
    err_slope, err_intercept = [], []
    residue = pd.DataFrame({'name': data['name'], 'logP': data['logP']})
    residue[dis_list[dis_flag.index(dis)]] = data[dis_list[dis_flag.index(dis)]]
    prediction = residue.copy()   
    # Store regression results
    PLW_struct = [PL_name, PL_slope, PL_intercept, prediction, residue, err_slope, err_intercept]  
    for ab in mode:
        for i in range(len(mag)):
            print('\n\t Mag: ', mag[i] + ab, '\t Method: ', flag, '\t Dis:', dis)
        # raw data
            a,b,c,d,e,f = regression(data['logP']-1, data['M_'+mag[i]+ab+dis], '(logP - 1)', 'M__'+mag[i]+ab, 1)
            PLW_struct = append_PLW(PLW_struct, mag[i] + ab, a, b, c, d, e, f, dis)
        # calibrated data
            for col in wes_show:
                a,b,c,d,e,f = regression(corrected['logP']-1,corrected[mag[i]+flag+ab+col+dis], '(logP - 1)', 'M%s%s'%(mag[i]+ab,col), p = 1)
                PLW_struct = append_PLW(PLW_struct, mag[i] +ab+ col+flag, a, b, c, d, e, f, dis)
    PLW = pd.DataFrame({
        'name': PLW_struct[0],
        f'm': PLW_struct[1],
        f'c': PLW_struct[2],
        f'err_m': PLW_struct[5],
        f'err_c': PLW_struct[6]
    })
    prediction = PLW_struct[3]
    residue = PLW_struct[4]
    return PLW, residue, prediction        

def corrected_reg(data, corrected, dis, plots=plots, wes_show = wes_show, flags=flags,s=s):
    reg = pd.DataFrame()
    res = pd.DataFrame()
    pre = pd.DataFrame()
    for f in flags:
        PLW, residue, prediction = corrected_PL(data, corrected, dis, f, s)
        reg = pd.concat([reg, PLW], axis=0)
        res = pd.concat([res, residue], axis=1)
        pre = pd.concat([pre, prediction], axis=1)
    res = res.loc[:, ~res.columns.duplicated()]
    pre = pre.loc[:, ~pre.columns.duplicated()]
    # Transpose regression DataFrame, and use the first row as column names
    reg = reg.T
    reg.columns = reg.iloc[0]
    reg = reg.drop(reg.index[0])
    reg = reg.loc[:, ~reg.columns.duplicated()]
    merged_data = merge_12(data, corrected, on = ['name', 'logP'])    
    merged_data = merge_12(merged_data, res, on = ['name', 'logP']) 
    merged_data = merge_12(merged_data, pre, on = ['name', 'logP'])    
    if s==1:
        res.to_csv('%s%i_result_residue.csv'%(data_out+process_step[7],len(res)))
        pre.to_csv('%s%i_result_prediction.csv'%(data_out+process_step[7],len(pre)))
        reg.to_csv('%s%i_%i_result_regression.csv'%(data_out+process_step[7],len(res),nreg))
        merged_data.to_csv('%s%i_merged_data.csv'%(data_out+process_step[7],len(res)))
    if plots == 1:
        for f in flags:
            for col in wes_show:
                for ab in mode:
                    plotresultPL6(merged_data, reg, col, dis, f, ab)
    return reg, res, pre, merged_data
   
def plotresultPL6(merged_data, merged_reg, col, dis, f, ab, s=s):
    fig, axs = plt.subplots(2, 3, figsize=(18, 8), sharex='col')
    axs = axs.flatten()  # Flatten for easy indexing
    x = merged_data['logP'] - 1
    for i, m in enumerate(mag[:6]):
        y = merged_data['M_' + m + ab + dis]
        y_cor = merged_data[m + f + ab+col + dis]
        # Get regression coefficients
        if dis == '_i':
            alpha = merged_reg[m+ab].iloc[4]
            gamma = merged_reg[m+ab].iloc[5]
            ralpha = merged_reg[m+ab+col+f].iloc[4]
            rgamma = merged_reg[m+ab+col+f].iloc[5]
        else:
            alpha = merged_reg[m+ab].iloc[0]
            gamma = merged_reg[m+ab].iloc[1]
            ralpha = merged_reg[m+ab+col+f].iloc[0]
            rgamma = merged_reg[m+ab+col+f].iloc[1]
        rpre = merged_data['p_' + m + ab + col + f + dis ]
        rres = merged_data['r_' + m + ab + col + f + dis]
        pred = merged_data['p_' + m + ab + dis]
        resd = merged_data['r_' + m + ab + dis]
        r_std = round(rres.std(ddof=0), 3)
        d_std = round(resd.std(ddof=0), 3)
        ax = axs[i]
        ax.plot(x, y, col_dot[i], label=f'{m+ab} Band | $\sigma$ = {d_std}')
        ax.plot(x, y_cor, 'ro', label=f'{m+ab} Band ({f}, {col}) | $\sigma$ = {r_std}')
        ax.plot(x, rpre, 'r-', label=f'$M_{m}^{f}$ = {ralpha:.3f}(logP - 1) + {rgamma:.3f}')
        ax.plot(x, pred, col_das[i], label=f'$M_{m}$ = {alpha:.3f}(logP - 1) + {gamma:.3f}')
        # Residual lines
        for j in range(len(merged_data)):
            label = rf"$Residue = \delta \mu + R_{{m}} * E_{{BV}}$" if j == 0 else None
            #ax.plot([x[j], x[j]], [y[j], pred[j]], color='red', linestyle='--', alpha=0.5, label=label)
        ax.invert_yaxis()
        for k in range(len(merged_data)):
            ax.annotate('%i'%(k), xy =(x.iloc[k], y.iloc[k]), fontsize = 11) 
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
    title = f'{len(merged_data)}_PL{ab}_{f}{col}{dis}'
    if s == 1:
        imgsave(title, 7, fil='pdf', p=1)
    plt.show()     

print(f'* * {module} module loaded!')
