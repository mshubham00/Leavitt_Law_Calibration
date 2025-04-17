from lvtlaw.a_utils import process_step, colors, mag, ap_bands, abs_bands, data_dir, input_data_file, data_out, dis_flag, dis_list, s, data_out, wes_show, flags, del_mu, regression, R
import pandas as pd
def get_pair(star):
    ls = {}    # 
    for d in dis_flag:
        for col in wes_show: 
            for f in flags:
                x = star[[col+d+'rd'+f+str(mu) for mu in del_mu]].iloc[-1]# # variance list
                x_min = pd.to_numeric(x, errors='coerce').min()   # minimum variance
                mu_name = star[[col+d+'rd'+f+str(mu) for mu in del_mu]].iloc[-1].idxmin()  # collect mu index
                rd = star[mu_name[0]].iloc[-2]  # collect mean reddening 
                mu = float(mu_name[0][8:])  # collect mu
                ls['rms'+d+col+f] = x_min 
                ls['mu'+d+col+f] = mu
                ls['rd'+d+col+f] = rd.iloc[0]#.values 
    return ls

def correction(stars, s=1):
    stars_correction = [] 
    for i in range(len(stars)):
        mu_rd_pair_list = get_pair(stars[i])
        stars_correction.append(mu_rd_pair_list)
    df = pd.DataFrame(stars_correction)
    if s==1:
        df.to_csv('%s%i_error_rms_mu_rd.csv'%(data_out+process_step[6],len(df)))
    return df    

def result(tabsolute, correction_red_mu_stars, col, dis, mag, flag, s=1):
    corrected = pd.DataFrame()
    corrected['logP'] = tabsolute['logP'] 
    print('Method: ', flag[1], '\t Color: ', col, '\t Distance: ', dis[1])
    for i in range(len(mag)):
        x = R[i]*correction_red_mu_stars['rd'+dis+col+flag] + correction_red_mu_stars['mu'+dis+col+flag]
        corrected[i]=tabsolute['M_'+mag[i]+'0'+dis] + x
        regression(tabsolute['logP']-1, tabsolute['M_'+mag[i]+'0'+dis], '(logP - 1)', mag[i]+dis, 1)
        m,c,p,r,em,ec = regression(corrected['logP']-1,corrected[i], '(logP-1)', 'M*_%s'%(mag[i]), p = s)

