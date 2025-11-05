### File: ./lvtlaw/f_star_wise.py
'''
This file resturcture the processed dataset in star by star sequence.

Function contained:
    star_frame(data, dis_flag): Creates DataFrames for each star containing abs0 and wesenheit.
        Output: stars (list of DataFrames: star)
    add_res(): Add residual of PL and PW relations for dis_flag
        Output: stars (updated list of DataFrames)
    add_dres(): Add del-del residue for wes_show and methods
        Output: stars (updated list of DataFrames)    
    star_ex_red_mu(mu_df_list_dict): for colors, methods, dis_flags, and mag - estimates reddening and variance for stepped mu
        Output: stars_ex_red_mu (list of DataFrames: star_df)
'''
module = 'f_star_wise'
#####################################################################
from data.datamapping import dis_flag, flags, wes_show, del_mu, s, plots, mag, data_out, process_step, col_lin, col_dot, col_das, rd_avg_drop, mode, plot_every_n_star, file_name
from lvtlaw.a_utils import imgsave
import pandas as pd
import matplotlib.pyplot as plt
#####################################################################
def star_frame(data, dis_flag=dis_flag, flags=flags, wes_show=wes_show):
    #  to extract features of individual Cepheids
    stars_list = []   
    name = data['name'] 
    for i in range(0,len(data)):
        star = pd.DataFrame()
        star['%s'%(name[i])] = mag
        for dis in dis_flag:
#            star['abs'+dis] = data[['M_%s%s'%(x, dis) for x in mag]].iloc[i].values
            star['abs0'+dis] = data[['M_%s0%s'%(x,dis) for x in mag]].iloc[i].values
            star['r_0%s'%(dis)] = data[['r_%s0%s'%(x,dis) for x in mag]].iloc[i].values
            for c in wes_show:
                star['w_'+c+dis] = data[['%s%s%s'%(x, c, dis) for x in mag]].iloc[i].values
                star['r_%s%s'%(c,dis)] = data[['r_%s%s%s'%(x,c,dis) for x in mag]].iloc[i].values
                for f in flags:
                    for ab in mode:
                        star['d_%s%s%s'%(f,c,dis)] = data[['d_%s%s%s%s%s'%(x,ab,x if f=='S' else c[0],c,dis) for x in mag]].iloc[i].values
        star.to_csv('%s%i_star.csv'%(data_out+process_step[9],i))
        stars_list.append(star)
    return stars_list
#####################################################################
def star_ex_rd_mu(mu_df_list_dict, data, flags=flags, dis_flag=dis_flag, p=1):
    n = len(data)
    stars_rd_mu_list = []
    print('Reddenings over mu for each star, each color and respective distance \n')
    print(f'Data output as {data_out}{process_step[5]}{n}_i_stars_ex_red_mu.csv')
    for i in range(0, n):
        star_df = pd.DataFrame()
        for col in wes_show:
            for dis in dis_flag:
                for ab in mode:
                    colms = [f'rd_{ab}{col}{mu}{dis}' for mu in del_mu]
                    for f in flags:
                        star_rd_mu_mag = pd.DataFrame()
                        for m in range(len(mag)):
                            star_rd_mu_mag[mag[m]] = mu_df_list_dict[f'{col}_{f}{dis}'][m][colms].iloc[i].values
                        star_rd_mu_mag = star_rd_mu_mag.T
                        star_rd_mu_mag.columns = [f'{f}{ab}{col}{dis}rd_{mu}' for mu in del_mu]
                        star_df = pd.concat([star_df, star_rd_mu_mag], axis = 1)
        star_df = star_df.astype('float64')
        star_df.loc['mean'] = star_df.drop(index=rd_avg_drop).mean()
        star_df.loc['var'] = star_df.drop(index=['mean']+rd_avg_drop).std(ddof=0)
        if p == 1:
            print('###' * 30)
            print(f'Star: {i} | Name: {data.name.iloc[i]} \n', i, star_df)
        star_df.to_csv(f'{data_out}{process_step[5]}{n}_{i}stars_ex_red_mu.csv')
        stars_rd_mu_list.append(star_df)
    return stars_rd_mu_list
#####################################################################
def get_error_pair(star_rd_mu, flags = flags, wes_show = wes_show, del_mu = del_mu):
    # star: dataframe containing star                 
    mu_rd_dict = {}    # 
    for d in dis_flag:   
        for f in flags: 
            for col in wes_show: 
                for ab in mode:
                    cols_name = [f'{f}{ab}{col}{d}rd_{mu}' for mu in del_mu] # column names
                    variance_over_mu = pd.to_numeric(star_rd_mu.loc['var', cols_name], errors='coerce') # collect all variation
                    min_var_indx = variance_over_mu.idxmin() # find minimum variance index name
                    mu_rd_dict[f'rd{f}{ab}{col}{d}'] = float(star_rd_mu.loc['mean', min_var_indx]) 
                    if ab == '':
                        solution_mu = float(min_var_indx[8:])  # collect mu of minimum vairance
                    else:
                        solution_mu = float(min_var_indx[9:])
                    mu_rd_dict[f'mu{f}{ab}{col}{d}'] = solution_mu
                    mu_rd_dict[f'vr{f}{ab}{col}{d}'] = min_var_indx
    return mu_rd_dict
#####################################################################
def correction_rd_mu(stars_rd_mu_list, raw, plots=plots, s=s ):
    stars_correction = []
    for i in range(len(stars_rd_mu_list)):
        mu_rd_dict = get_error_pair(stars_rd_mu_list[i])
        stars_correction.append(mu_rd_dict)
    correction_rd_mu_stars_df = pd.DataFrame(stars_correction)
    correction_rd_mu_stars_df['name'] = raw.name
    correction_rd_mu_stars_df['logP'] = raw['logP']
    if s==1:
        correction_rd_mu_stars_df.to_csv('%s%i_error_rms_mu_rd.csv'%(data_out+process_step[6],len(raw)))
    if plots == 1:
        for i in range(0, len(raw),plot_every_n_star):
            for f in flags:
                for d in dis_flag:
                    for ab in mode:
                        print(i,f,d,ab)
                        plot_star_rd_mu(i, stars_rd_mu_list, correction_rd_mu_stars_df, f, ab, d)
    return correction_rd_mu_stars_df    
#####################################################################
def plot_star_rd_mu(i, stars_rd_mu_list, correction, flag, ab, dis, wes_show = wes_show, s=s):
    a = stars_rd_mu_list[i]
    fig, axs = plt.subplots(2, 2, figsize=(13, 5), sharex='col')
    axs = axs.flatten()  # Flatten for easy indexing
    for k, col in enumerate(wes_show[:4]):
        del_E = a[[f'{flag}{ab}{col}{dis}rd_{mu}' for mu in del_mu]]
        mu_c = correction[f'mu{flag}{ab}{col}{dis}'].iloc[i]
        EBV_c = correction[f'rd{flag}{ab}{col}{dis}'].iloc[i]
# === Plotting ===
        ax = axs[k]
        #ax.invert_yaxis()
        for j in range(len(mag)):
            ax.plot(del_mu, del_E.iloc[j].values, col_lin[j], label='%s'%(mag[j]+ab))
        ax.plot(del_mu, del_E.iloc[-1].values, col_das[0], label=f'rms')
        ax.plot(mu_c, EBV_c, 'ko') 
        ax.axhline(y=EBV_c, color='gray', linestyle='--')
        ax.axvline(x=mu_c, color='gray', linestyle='--')
        ax.annotate(f'{mu_c:.2f}', xy=(mu_c, axs[1].get_ylim()[-1]), xytext=(0, 5), textcoords='offset points', va='top', ha='left', fontsize=10, color='black')
        ax.annotate(f'{EBV_c:.2f}', xy=(del_mu[-1], EBV_c), xytext=(5, 0), textcoords='offset points', va='bottom', ha='right', fontsize=10, color='black')
        ax.set_xlabel(f'$\Delta \mu  $  ({col}  :  {mu_c:.3f})')
        ax.set_ylabel(f'$\Delta E  $  ({col}  :  {EBV_c:.3f})')
#        ax.set_ylim(-1, 1)
    for ax in axs:
#        ax.legend()
        for spine in ax.spines.values():
            spine.set_visible(False)
    axs[0].legend()
    plt.tight_layout()
    title = '%s_%i_star_%s%s%s'%(file_name, i, flag, wes_show[0], dis)
    plt.suptitle(f'{i} {correction.name.iloc[i]} ({flag})')
    print(title)
    if s==1:
        imgsave(title,5,fil='pdf', p=1)
    plt.show()
#####################################################################
def plot_star_rd_muM(index, stars_rd_mu_list, correction, flag, ab, dis, col = 'VI', s=s):
    fig, axs = plt.subplots(2, 2, figsize=(13, 5), sharex='col')
    axs = axs.flatten()  # Flatten for easy indexing
    for k, i in enumerate(index): 
        a = stars_rd_mu_list[i]
        del_E = a[[f'{flag}{ab}{col}{dis}rd_{mu}' for mu in del_mu]]
        mu_c = correction[f'mu{flag}{ab}{col}{dis}'].iloc[i]
        EBV_c = correction[f'rd{flag}{ab}{col}{dis}'].iloc[i]
# === Plotting ===
        ax = axs[k]
        #ax.invert_yaxis()
        for j in range(len(mag)):
            ax.plot(del_mu, del_E.iloc[j].values, col_lin[j], label='%s'%(mag[j]+ab))
        ax.plot(del_mu, del_E.iloc[-1].values, col_das[0], label='rms')
        ax.plot(mu_c, EBV_c, 'ko') 
        ax.axhline(y=EBV_c, color='gray', linestyle='--')
        ax.annotate(f'{EBV_c:.2f}', xy=(del_mu[-1], EBV_c), xytext=(5, 0), textcoords='offset points', va='bottom', ha='right', fontsize=10, color='black')
        ax.axvline(x=mu_c, color='gray', linestyle='--')
        ax.annotate(f'{mu_c:.2f}', xy=(mu_c, axs[1].get_ylim()[-1]), xytext=(0, 5), textcoords='offset points', va='top', ha='left', fontsize=10, color='black')
        ax.set_xlabel(f'{correction.name.iloc[i]} $\Delta \mu ({col} : {mu_c:.2f}, {EBV_c:.2f})$')
        ax.set_ylabel(r'$\Delta E_{BV}$')
#        ax.set_ylim(-1, 1)
    for ax in axs:
#        ax.legend()
        for spine in ax.spines.values():
            spine.set_visible(False)
    axs[0].legend()
    plt.tight_layout()
    title = '%i_%i_star_%s%s%s'%(len(correction), i, flag, col, dis)
    #plt.suptitle(f'M_ {correction.name.iloc[i]} ({flag})')
    print(title)
    if s==1:
        imgsave(title,5,fil='pdf', p=1)
    plt.show()
#####################################################################
print(f'* * {module} module loaded!')
