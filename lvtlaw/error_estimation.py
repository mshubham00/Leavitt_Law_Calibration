### File: ./lvtlaw/error_estimation.py

from lvtlaw.utils import colors,data_dir, data_file, data_out, R, mag, disg, disi
import pandas as pd
from lvtlaw.pl_pw import pl_reg     #pl_reg(data,'_g','_i') -> PLW, residue, prediction
from lvtlaw.data_transform import transformation, extinction_law

res = pd.read_csv(data_out+'95_residue.csv')
raw = pd.read_csv(data_out+'95abs_data.csv')
del_slope = pd.read_csv(data_out+'95_del_slope_intercept.csv')
del_slope_M = pd.read_csv(data_out+'95_del_slope_intercept_M.csv')

def calculate_extinction_reddening(name, del_W, del_M, slope, wm_str, R):
    del_mu = [i*0.01 for i in range(-100,100,2)]
    extinction = pd.DataFrame()
    reddening = pd.DataFrame()
    extinction['%s'%(wm_str)]=name
    reddening['%s'%(wm_str)]=name
    for mu in del_mu:
        extinction['%f'%(mu)] = (del_M + mu) - slope*(del_W + mu)
        reddening['%f'%(mu)] = extinction['%f'%(mu)]/R  
    #print(reddening.head())
    return del_mu, extinction, reddening

def all_bands_reddening(data = res, slope_data = del_slope, col = 'VI', mag = mag):
    reddening_bands_g = []
    reddening_bands_i = []
    for i in range(0,6):
        name = data['name']
        wes = mag[i]+col
        wm_str = mag[i]+wes
        #input('%s'%(wm_str))
        dis = disg
        r = R[i]/(R[1]-R[2])
        del_M = data['r0_'+mag[i]+dis]
        del_W = data['r_'+wes+dis]
        slope = slope_data[wm_str].iloc[0]
        del_mu, extinction_g, reddening_g = calculate_extinction_reddening(name, del_W, del_M, slope, wm_str+dis, r)
        reddening_bands_g.append(reddening_g)
        dis = disi
        del_M = data['r0_'+mag[i]+dis]
        del_W = data['r_'+wes+dis]
        slope = slope_data[wm_str].iloc[4]
        del_mu, extinction_i, reddening_i = calculate_extinction_reddening(name, del_W, del_M, slope, wm_str+dis,r)
        reddening_bands_i.append(reddening_i)
    return del_mu, reddening_bands_g, reddening_bands_i


mu,red_g,red_i = all_bands_reddening()
#input('#########################################################')
def find_rms(name, reddening, del_mu):
    rms_df = pd.DataFrame()
    rms_df['rms'] = name
    EBV_df = pd.DataFrame()
    EBV_df['EBV'] = name
    mu = del_mu
    dispersion_list = []
    for k in mu:
        dispersion = pd.DataFrame()
        dispersion['rms'] = name
        summ = 0
        for i in range(0,6):
            dispersion[mag[i]] = reddening[i]['%f'%(k)]
            summ += dispersion[mag[i]]
        dispersion['avg_EBV'] = summ / 6
        EBV_df['%f'%(k)] = dispersion['avg_EBV'] 
        dev = 0
        for i in range(0,6):
            dev += (dispersion[mag[i]] - dispersion['avg_EBV'])**2
            rms = dev**0.5
        dispersion['%f'%(k)] = rms
        dispersion_list.append(dispersion)
        rms_df['%f'%(k)] = rms
    return rms_df, EBV_df

rms_df_g, avg_EBV_g = find_rms(res.name, red_g, mu)
rms_df_i, avg_EBV_i = find_rms(res.name, red_i, mu)
input('#########################################################')

def find_error_pair(rms_df = rms_df_g, avg_EBV = avg_EBV_g):
    error_result = pd.DataFrame()
    error_result['error'] = rms_df.rms
    rms = []
    EBV = []
    mu = []
    for i in range(0,95):
        dispersion_over_mu = rms_df.iloc[i].to_dict()
        y = rms_df.iloc[i].values
        min_rms = min(y[1:])
        rms.append(min_rms)
        min_mu = list(filter(lambda x: dispersion_over_mu[x] == min_rms, dispersion_over_mu))[0]
        mu.append(float(min_mu))
        EBV.append(avg_EBV[min_mu].iloc[i])
    error_result['rms'] = rms
    error_result['mu'] = mu
    error_result['EBV'] = EBV
    for i in range(0,6):
        error_result['A_'+mag[i]] = error_result['EBV']*R[i]
    return error_result
result_g = find_error_pair(rms_df_g, avg_EBV_g)
result_i = find_error_pair(rms_df_i, avg_EBV_i)
print('\n',result_g)
print('\n',result_i)
input('#########################################################')

def error_correction(error_pair = result_g, raw = raw, dis=disg):
    correction=pd.DataFrame()
    if dis == disi:
        rdis = 'IRSB'
    else:
        rdis = 'plx'
    correction['name']=error_pair.error
    correction['new_mod'] = raw[rdis] + error_pair['mu']
    correction['new_EBV'] = raw['EBV'] + error_pair['EBV']
    for i in range(0,6):
        correction['new_M_'+mag[i]] = raw['M_'+mag[i]+dis] + error_pair['mu'] + error_pair['A_'+mag[i]]
    print(correction)
    return correction

result_g = error_correction(result_g, raw, disg)
result_i = error_correction(result_i, raw, disi)


