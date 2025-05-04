from lvtlaw.a_utils import process_step, colors, mag, ap_bands, abs_bands, data_dir, input_data_file, data_out, dis_flag, dis_list, s, data_out, wes_show, flags, del_mu, regression, R
import pandas as pd

def get_error_pair(star):
    ls = {}    # 
    for d in dis_flag:
        for col in wes_show: 
            for f in flags:
                x = star[[col+d+'rd'+f+str(mu) for mu in del_mu]].iloc[-1]# # variance list
                x_min = pd.to_numeric(x, errors='coerce').min()   # minimum variance
                mu_name = star[[col+d+'rd'+f+str(mu) for mu in del_mu]].iloc[-1].idxmin()  # collect mu index
                mu = float(mu_name[0][8:])  # collect mu
                rd = star[mu_name[0]].iloc[-2].values  # collect mean reddening 
                print('\n redd:', rd[0], x_min)
                print('mu:', mu_name[0][8:]) 
                #print(star)
                ls['rms'+d+col+f] = x_min 
                ls['mu'+d+col+f] = mu
                ls['rd'+d+col+f] = rd[0]#.values 
    return ls

def correction_rd_mu(stars, save=1):
    stars_correction = [] 
    for i in range(len(stars)):
        mu_rd_pair_list = get_error_pair(stars[i])
        stars_correction.append(mu_rd_pair_list)
    correction_red_mu_stars = pd.DataFrame(stars_correction)
    if save==1:
        correction_red_mu_stars.to_csv('%s%i_error_rms_mu_rd.csv'%(data_out+process_step[6],len(stars)))
    return correction_red_mu_stars    

def correction_apply(tabsolute, correction, save=1):
    corrected = pd.DataFrame()
    correct = pd.DataFrame()
    corrected['logP'] = tabsolute['logP'] 
    for d in dis_flag:
        for col in wes_show:
            for f in flags:
                correct['mu'+d+col+f] = correction['mu'+d+col+f]
                for i in range(len(mag)):
                    correct['ex'+mag[i]+d+col+f] = R[i]*correction['rd'+d+col+f]
                    corrected[mag[i]+d+col+f]=tabsolute['M_'+mag[i]+'0'+d] + correct['ex'+mag[i]+d+col+f]+correction['mu'+d+col+f]
    print('Correction for each band \n', correct)
    if save==1:
        corrected.to_csv('%s%i_corrected_%s%s%s.csv'%(data_out+process_step[7],len(corrected), d, col, f))
    return corrected
    
def corrected_PL(tabsolute, corrected, s=1):
    for dis in dis_flag:
        for col in wes_show:
            for flag in flags:
                print('Method: ', flag[1], '\t Color: ', col, '\t Distance: ', dis[1])
                for i in range(len(mag)):
                    regression(tabsolute['logP']-1, tabsolute['M_'+mag[i]+'0'+dis], '(logP - 1)', 'M__'+mag[i], 1)
                    m,c,p,r,em,ec = regression(corrected['logP']-1,corrected[mag[i]+dis+col+flag], '(logP - 1)', 'M*_%s'%(mag[i]), p = s)
    #if save==1:
        #corrected.to_csv('%s%i_corrected_%s%s%s.csv'%(data_out+process_step[6],len(corrected),col, dis, flag))
        
        
        
'''
    if s==2:
        res.to_csv('%s%i_residue.csv'%(data_out+process_step[7],len(res)))
        pre.to_csv('%s%i_prediction.csv'%(data_out+process_step[7],len(pre)))
        reg.to_csv('./%s%i_regression.csv'%(data_out+process_step[7],len(reg)))    

'''
