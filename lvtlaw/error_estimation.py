### File: ./lvtlaw/error_estimation.py

from lvtlaw.utils import colors,data_dir, data_file, data_out, R, mag, dis, dis_list, process_step
import pandas as pd
from lvtlaw.pl_pw import pl_reg     #pl_reg(data,'_g','_i') -> PLW, residue, prediction
from lvtlaw.data_transform import transformation, extinction_law

#for a star, del-del slope required which varies for different bands. Also residue of PL, PW required. 
def calculate_extinction_reddening(star_name, del_W, del_M, slope, wm_str, R):
    del_mu = [i*0.01 for i in range(-100,100,2)]
    del_mu = [round(x, 2) for x in del_mu]
    extinction = pd.DataFrame()
    reddening = pd.DataFrame()
    extinction['%s'%(wm_str)]=star_name
    reddening['%s'%(wm_str)]=star_name
    for mu in del_mu:
        extinction['%f'%(mu)] = (del_M + mu) - slope*(del_W + mu)
        reddening['%f'%(mu)] = extinction['%f'%(mu)]/R  
    return del_mu, extinction, reddening

def all_dis_reddening(residue, slope_data, diss , col, flag):
    star_names = residue['name']
    reddening_dis_list_df = []  # [distance-based [band-based [reddening-dataframe(star,mu)]]]
    extinction_dis_list_df = []
    for dis in diss:
        reddening_bands = []
        extinction_bands = []
        for i in range(0,6):
            r = R[i]/(R[mag.index(col[0])]-R[mag.index(col[1])])
            if flag == '_S':
                wes = mag[i]+col
            else:
                wes = col[0]+col
            wm_str = mag[i]+wes
            del_M = residue['r0_'+mag[i]+dis]
            del_W = residue['r_'+wes+dis]
            if dis == '_g':
                slope = slope_data[wm_str].iloc[0]
            else:
                slope = slope_data[wm_str].iloc[4]            
            del_mu, extinction, reddening = calculate_extinction_reddening(star_names, del_W, del_M, slope, wm_str+dis, r)
            reddening_bands.append(reddening)
            extinction_bands.append(extinction)
            reddening.to_csv('%s%i_red_%s.csv'%(data_out+process_step[3],len(reddening),wm_str))
            extinction.to_csv('%s%i_ext_%s.csv'%(data_out+process_step[3],len(extinction),wm_str))
        reddening_dis_list_df.append(reddening_bands)
        extinction_dis_list_df.append(extinction_bands)
    # returns list of mu, 2 distance-dependent lists of dfs
    return del_mu, reddening_dis_list_df, extinction_dis_list_df

#input('#########################################################')

def find_rms(star_name, reddening, extinction, del_mu, col, d, flag):
    # input 
    rms_df = pd.DataFrame()
    rms_df['rms'] = star_name
    EBV_df = pd.DataFrame()
    EBV_df['EBV'] = star_name
    dispersion_list = []
    for mu in del_mu:
        dispersion = pd.DataFrame()
        dispersion[str(mu)] = star_name
        summ = 0
        for i in range(0,6):
            dispersion['E0'+mag[i]] = reddening[i]['%f'%(mu)]
            dispersion['A0_'+mag[i]] = extinction[i]['%f'%(mu)]
            summ += dispersion['E0'+mag[i]]
        dispersion['avg_EBV'] = summ / 6
        EBV_df['%f'%(mu)] = dispersion['avg_EBV'] # yielding avg. reddening error for each mod
        dev = 0
        for i in range(0, 6):
            dev += (dispersion['E0'+mag[i]] - dispersion['avg_EBV'])**2
        rms = (dev/6)**0.5
        rms_df['%f'%(mu)] = rms
        dispersion['%f'%(mu)] = rms
        dispersion.to_csv('%s%i_dispersion_%s_%s_%s_%f.csv'%(data_out+process_step[4],len(rms_df), d, col, flag,mu))
        dispersion_list.append(dispersion) # list of dataframes for every mu step
    print(EBV_df)
    rms_df.to_csv('%s%i_rms_%s_%s_%s.csv'%(data_out+process_step[5],len(rms_df),d, col, flag))
    EBV_df.to_csv('%s%i_EBV_%s_%s_%s.csv'%(data_out+process_step[5],len(EBV_df), d, col,flag))
    return rms_df, EBV_df, dispersion_list


def find_error_pair(rms_df, EBV_df, del_mu, dispersion_list, col,d,flag):
    print(rms_df.info(), rms_df.head())    
    error_result = pd.DataFrame()
    error_result['error_pair'] = rms_df.rms #name of star
    rms = []
    EBV = []
    mu = []
    for i in range(0,95):
        dispersion_over_mu = rms_df.iloc[i].to_dict()
        y = rms_df.iloc[i].values
        min_rms = min(y[1:]) # min E-rms among all mu-trails for given color and distance.
        rms.append(min_rms)
        min_mu = list(filter(lambda x: dispersion_over_mu[x] == min_rms, dispersion_over_mu))[0]
        mu.append(float(min_mu))
        EBV.append(EBV_df[min_mu].iloc[i])
        for k in range(0,6):
            error_result['A0_'+mag[k]]= dispersion_list[del_mu.index(float(min_mu))]['A0_'+mag[k]].iloc[i]
    error_result['min_rms'] = rms
    error_result['min_mu'] = mu
    error_result['avg_EBV'] = EBV
    for i in range(0,6):
        error_result['A_'+mag[i]] = error_result['avg_EBV']*R[i]
    print(error_result.head())
    error_result.to_csv('%s%i_error_%s_%s_%s.csv'%(data_out+process_step[6],len(error_result),d,col,flag))
    return error_result

def error_correction(error_result, raw, col, dis, flag):
    correction=pd.DataFrame()
    if dis == '_g':
        rdis = 'plx'
    else:
        rdis = 'IRSB'
    correction['name']=error_result.error_pair
    correction['logP']=raw['logP']
    correction['new_mod'] = raw[rdis] + error_result['min_mu']
    correction['new_EBV'] = raw['EBV'] + error_result['avg_EBV']
    for i in range(0,6):
        correction['new_M_'+mag[i]] = raw['M_'+mag[i]+dis] - error_result['min_mu'] - error_result['A_'+mag[i]]
        correction['new_M0_'+mag[i]] = raw['M_'+mag[i]+dis] - error_result['min_mu'] - error_result['A0_'+mag[i]]
    correction.to_csv('%s%i_result_%s_%s_%s.csv'%(data_out+process_step[7],len(correction), dis, col,flag))
    return correction


def result(raw_data, dresidue, dslope, diss, col, flag):
    col_list=[]
    for c in col: # for four interesting wesenheits BV, VI, VK, JK
        del_mu, red_dis_list, ex_dis_list= all_dis_reddening(dresidue,dslope, diss, c, flag)
        dis_list = []
        k=0
        for red, ext in red_dis_list, ex_dis_list:
            d = diss[k]
            rms_df, EBV_df, dispersion_list = find_rms(dresidue.name, red, ext, del_mu, c, d, flag)
            error_df = find_error_pair(rms_df, EBV_df, del_mu, dispersion_list, c, d, flag)
            result_df = error_correction(error_df, raw_data, c, d, flag)
            #print(result_df)
            dis_list.append(result_df)
            k=k+1
        col_list.append(dis_list)
    return col_list

    



