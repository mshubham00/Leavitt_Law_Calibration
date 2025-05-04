### File: ./lvtlaw/f_star_wise.py
from lvtlaw.a_utils import process_step, colors, mag, ap_bands, abs_bands, data_dir, input_data_file, data_out, dis_flag, dis_list, s, data_out, wes_show, del_mu

import pandas as pd

def star_frame(data):
    # input prepared_regression_data
    stars = []   
    name = data['name_x'] 
    for i in range(0,len(data)):
        star = pd.DataFrame()
        star['%s'%(name[i])] = mag
        for dis in dis_flag:
            star['abs'+dis] = data[['M_%s%s'%(x, dis) for x in mag]].iloc[i].values
            star['abs0'+dis] = data[['M_%s0%s'%(x, dis) for x in mag]].iloc[i].values
            for c in wes_show:
                star[c+dis] = data[['%s%s%s'%(x, c, dis) for x in mag]].iloc[i].values
        #print(star.head(10))
        stars.append(star)
    return stars

def add_res(stars, res):
    for i in range(0, len(stars)):
        for d in dis_flag:
            stars[i]['r%s'%(d)] =  res[['r_%s%s'%(x,d) for x in mag]].iloc[i].values
            stars[i]['r0%s'%(d)] = res[['r_%s%s'%(x,d) for x in mag]].iloc[i].values
            for c in wes_show:
                stars[i]['r_%s%s'%(c,d)] = res[['r_%s%s%s'%(x,c,d) for x in mag]].iloc[i].values
    return stars
    
def add_dres(stars, dresS, dresM):
    for i in range(0, len(stars)):
        for d in dis_flag:
            for c in wes_show:
                stars[i]['S_%s%s'%(c,d)] = dresS[['d_%s%s%s%s'%(x,x,c,d) for x in mag]].iloc[i].values
                stars[i]['M_%s%s'%(c,d)] = dresM[['d_%s%s%s%s'%(x,c[0],c,d) for x in mag]].iloc[i].values
        stars[i].to_csv('%s%i_star.csv'%(data_out+process_step[9],i))
    return stars

#                     dis[].cols_SM{}.mag[].[mu_e_r.star] 
def star_ex_red_mu(n, ex_rd_mu, raw):
    stars = []
    print('Reddenings over mu for each star, each color and respective distance')
    for i in range(0, n):
        df = pd.DataFrame()
        for d in range(len(dis_flag)):
            for c in wes_show:
                rdS = pd.DataFrame()
                rdM = pd.DataFrame()
                for m in range(len(mag)):
                    rdS[mag[m]] = ex_rd_mu[d][c+'_S'][m][['rd_'+str(mu) for mu in del_mu]].iloc[i].values
                    rdM[mag[m]] = ex_rd_mu[d][c+'_M'][m][['rd_'+str(mu) for mu in del_mu]].iloc[i].values
                rdS = rdS.T
                rdS.columns = [[c+dis_flag[d]+'rd_S'+str(mu) for mu in del_mu]]  # Make sure number matches df.shape[1]
                rdM = rdM.T
                rdM.columns = [[c+dis_flag[d]+'rd_M'+str(mu) for mu in del_mu]]  # Make sure number matches df.shape[1]
                df = pd.concat([df, rdM], axis=1)                         
                df = pd.concat([df, rdS], axis=1)   
                df.loc['mean'] = df.mean()
                x=0
                for m in range(len(mag)):
                    x += (df.iloc[m] - df.loc['mean'])**2 
                df.loc['var'] = x                       
            print('#'*30)
        #print(df)
        stars.append(df)
        print('Star Name: ', raw.name.iloc[i])
        print(i, stars[i])                         
        df.to_csv('%s%i_%istars_ex_red_mu.csv'%(data_out+process_step[5],i, n))
    return stars
            

