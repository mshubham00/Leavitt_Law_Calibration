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

from lvtlaw.a_utils import process_step, colors, mag, ap_bands, abs_bands, data_dir, data_out, dis_flag, dis_list, s, data_out, wes_show, del_mu

import pandas as pd

def star_frame(data, dis_flag=dis_flag):
    # input prepared_regression_data
    stars = []   
    name = data['name'] 
    for i in range(0,len(data)):
        star = pd.DataFrame()
        star['%s'%(name[i])] = mag
        for dis in dis_flag:
#            star['abs'+dis] = data[['M_%s%s'%(x, dis) for x in mag]].iloc[i].values
            star['abs0'+dis] = data[['M_%s0%s'%(x,dis) for x in mag]].iloc[i].values
            for c in wes_show:
                star[c+dis] = data[['%s%s%s'%(x, c, dis) for x in mag]].iloc[i].values
        #print(star.head(10))
        stars.append(star)
    return stars

def add_res(stars, res, dis_flag=dis_flag):
    for i in range(0, len(stars)):
        for d in dis_flag:
#            stars[i]['r%s'%(d)] =  res[['r_%s%s'%(x,d) for x in mag]].iloc[i].values
            stars[i]['r_0%s'%(d)] = res[['r_%s0%s'%(x,d) for x in mag]].iloc[i].values
            for c in wes_show:
                stars[i]['r_%s%s'%(c,d)] = res[['r_%s%s%s'%(x,c,d) for x in mag]].iloc[i].values
    return stars
    
def add_dres(stars, dres, flags, dis):
    for i in range(0, len(stars)):
        for c in wes_show:
            for f in flags:
                stars[i]['%s%s'%(c,dis)] = dres[['d_%s%s%s%s'%(x,x if f=='S' else c[0],c,dis) for x in mag]].iloc[i].values
        stars[i].to_csv('%s%i_star.csv'%(data_out+process_step[9],i))
    return stars

def star_ex_red_mu(n, mu_df_list_dict, raw, flags, dis_flag=dis_flag):
    stars_ex_red_mu = []
    print('Reddenings over mu for each star, each color and respective distance \n')
    print(f'Data output as {data_out}{process_step[5]}{n}_i_stars_ex_red_mu.csv')
    for i in range(0, n):
        star_df = pd.DataFrame()
        for c in wes_show:
            for dis in dis_flag:
                colms = [f'rd_{mu}{dis}' for mu in del_mu]
                for f in flags:
                    rdMS = pd.DataFrame()
                    for m in range(len(mag)):
                        rdMS[mag[m]] = mu_df_list_dict[f'{c}_{f}{dis}'][m][colms].iloc[i].values
                    rdMS = rdMS.T
                    rdMS.columns = [f'{f}{c}{dis}rd_{mu}' for mu in del_mu]
                    star_df = pd.concat([star_df, rdMS], axis = 1)
        star_df = star_df.astype('float64')
        star_df.loc['mean'] = star_df.drop(index=['H', 'K']).mean()
        star_df.loc['var'] = star_df.drop(index=['mean', 'H', 'K']).std(ddof=0)
        print('###' * 30)
        print(f'Star: {i} | Name: {raw.name.iloc[i]} \n', i, star_df)
        star_df.to_csv(f'{data_out}{process_step[5]}{n}_{i}stars_ex_red_mu.csv')
        stars_ex_red_mu.append(star_df)
    return stars_ex_red_mu
