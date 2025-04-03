### File: ./lvtlaw/error_estimation.py

from lvtlaw.a_utils import colors,data_dir, input_data_file, data_out, R, mag, dis_flag, dis_list, process_step
import pandas as pd
from lvtlaw.b_data_transform import transformation, extinction_law
from lvtlaw.c_pl_pw import pl_reg     #pl_reg(data,'_g','_i') -> PLW, residue, prediction


def all_star(residue, slope_data, dis_flag, cols, flags, s=1):
    ex_ = pd.DataFrame()
    rd_ = pd.DataFrame()
    for flag in flags:
        for dis in dis_flag:
            for col in cols:
                for i in range(0, len(mag)):
                    r = R[i] / (R[mag.index(col[0])] - R[mag.index(col[1])])                
                    if flag == '_S':
                        wes = mag[i] + col
                        slope = slope_data[0]
                    else:
                        wes = col[0] + col
                        slope = slope_data[1]
                    wm_str = mag[i] + wes
                    del_M = residue['r0_' + mag[i] + dis]
                    del_W = residue['r_' + wes + dis]
                    if dis == dis_flag[0]:
                        m = slope[wm_str].iloc[0]
                        c = slope[wm_str].iloc[2]
                    elif dis == dis_flag[1]:
                        m = slope[wm_str].iloc[4]            
                        c = slope[wm_str].iloc[6]
                    ex_[wm_str + dis+flag] = del_M - m * del_W - c
                    rd_[wm_str + dis+flag] = ex_[wm_str + dis+flag] / r
    if s == 1:
        ex_.to_csv('%s%i_ex.csv' % (data_out + process_step[2], len(ex_)))
        rd_.to_csv('%s%i_rd.csv' % (data_out + process_step[2], len(rd_)))    
    return ex_, rd_

def star_by_star(residue, slope_data, dis_flag , cols, flags, s=1):
    e,r = all_star(residue, slope_data, dis_flag , cols, flags, s=1)
    star_list =[]
    for index in range(len(residue)):
        star_data = pd.DataFrame()
        for flag in flags:
            for dis in range(len(dis_flag)):
                for col in cols:
                    ex=[]
                    rd=[]
                    for i in range(6):
                        if flag == '_S':
                            wes = mag[i]+col
                        elif flag == '_M':
                            wes = col[0]+col
                        wm_str = mag[i]+wes
                        ex.append(e[wm_str+dis_flag[dis]+flag].iloc[index])
                        rd.append(r[wm_str+dis_flag[dis]+flag].iloc[index])
                    star_data['A0'+col+dis_flag[dis]+flag] = ex
                    star_data['E0'+col+dis_flag[dis]+flag] = rd
        star_data.to_csv('%s%i_%i_star.csv'%(data_out+process_step[2],len(star_data),index))
        star_list.append(star_data)
    return star_list
     
#for a star, del-del slope required which varies for different bands. Also residue of PL, PW required. 
def calculate_extinction_reddening(star_names, period, del_W, del_M, slope, intrc, wm_str, R, dis, s =1):
    # del_W : list containing residue of specific PW relation
    # del_M : list containing resdiue of specific PL relation
    # slope, intrc : m and c of linear fit between del_W and del_M
    del_mu = [i*0.01 for i in range(-100,100,2)]
    del_mu = [round(x, 2) for x in del_mu]
    extinction = pd.DataFrame()
    reddening = pd.DataFrame()
    extinction['logP'] = reddening['logP'] = period
    extinction['%s'%(wm_str)]=star_names
    reddening['%s'%(wm_str)]=star_names
#    ex_ = del_M - slope*del_W - intrc
#    rd_ = ex_/R
    for mu in del_mu:
        extinction[str(mu)] = (del_M - mu) - slope*(del_W - mu) - intrc
             #                  = (del_M - slope*del_W - intrc) + mu (slope - 1)
        reddening[str(mu)] = extinction[str(mu)]/R  
    if s==1:
        reddening.to_csv('%s%i_red_%s%s.csv'%(data_out+process_step[3],len(reddening),wm_str,dis))
        extinction.to_csv('%s%i_ext_%s%s.csv'%(data_out+process_step[3],len(extinction),wm_str,dis))
    return del_mu, extinction, reddening#, ex_, rd_

def all_dis_reddening(residue, slope_data, dis_flag , col, flag, s=1):
    # residue : dataframe containing PL and PW residues
    # slope_data : dataframe containing all the slope and intercept of del-del plots
    star_names = residue['name']
    period = residue['logP']
    reddening_dis_list_df = []  # [distance-based [band-based [reddening-dataframe(star,mu)]]]
    extinction_dis_list_df = []
    for dis in dis_flag:
        reddening_bands = []
        extinction_bands = []
        for i in range(0,len(mag)):
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
                intrc = slope_data[wm_str].iloc[2]
            else:
                slope = slope_data[wm_str].iloc[4]            
                intrc = slope_data[wm_str].iloc[6]
            del_mu, extinction, reddening = calculate_extinction_reddening(star_names, period, del_W, del_M, slope, intrc, wm_str, r, dis)
            reddening_bands.append(reddening)
            extinction_bands.append(extinction)
        reddening_dis_list_df.append(reddening_bands)
        extinction_dis_list_df.append(extinction_bands)
    # returns list of mu, 2 distance-dependent lists of dfs
    return del_mu, reddening_dis_list_df, extinction_dis_list_df

#input('#########################################################')

def find_rms(star_names, reddening, extinction, del_mu, col, d, flag, s=1, number_of_bands = 4):
    # input 
    del_mu = [round(x, 2) for x in del_mu]
    rms_df = pd.DataFrame()
    rms_df['rms'] = star_names
    EBV_df = pd.DataFrame()
    EBV_df['EBV'] = star_names
    dispersion_list = []
    for mu in del_mu:
        dispersion = pd.DataFrame()
        dispersion[str(mu)] = star_names
        summ = 0
        for i in range(0,len(mag)):
            dispersion['E0'+mag[i]] = reddening[i][str(mu)]
            dispersion['A0_'+mag[i]] = extinction[i][str(mu)]
            summ += dispersion['E0'+mag[i]]
        dispersion['avg_EBV'] = summ / 6
        EBV_df[str(mu)] = dispersion['avg_EBV'] # yielding avg. reddening error for each mod
        dev = 0
        for i in range(0, number_of_bands):
            dev += (dispersion['E0'+mag[i]] - dispersion['avg_EBV'])**2
        rms = (dev/number_of_bands )**0.5
        rms_df[str(mu)] = rms
        dispersion['rms'] = rms
        if s==1:
            dispersion.to_csv('%s%i_dispersion%s_%s%s_%s.csv'%(data_out+process_step[4],len(rms_df), d, col, flag,str(mu)))
        dispersion_list.append(dispersion) # list of dataframes for every mu step
    print(EBV_df)
    if s==1:
        rms_df.to_csv('%s%i_rms_%s_%s_%s.csv'%(data_out+process_step[5],len(rms_df),d, col, flag))
        EBV_df.to_csv('%s%i_EBV_%s_%s_%s.csv'%(data_out+process_step[5],len(EBV_df), d, col,flag))
    return rms_df, EBV_df, dispersion_list



def find_error_pair(rms_df, EBV_df, del_mu, dispersion_list, col,d,flag, s=1):
    print(rms_df.info(), rms_df.head())    
    error_result = pd.DataFrame()
    error_result['error_pair'] = rms_df.rms #name of star
    rms = []
    EBV = []
    mu = []
    for i in range(0,len(rms_df)): # star by star
        dispersion_over_mu = rms_df.iloc[i].to_dict() # list of str
        rms_over_mu = rms_df.iloc[i].values # list of numbers
        min_rms = min(rms_over_mu[1:]) # min E-rms among all mu-trails for given color and distance.
        rms.append(min_rms)
        min_mu = list(filter(lambda x: dispersion_over_mu[x] == min_rms, dispersion_over_mu))[0]
        mu.append(float(min_mu))
        EBV.append(EBV_df[min_mu].iloc[i])
        for k in range(0,len(mag)):
            error_result['A0_'+mag[k]]= dispersion_list[del_mu.index(float(min_mu))]['A0_'+mag[k]].iloc[i]
    error_result['min_rms'] = rms
    error_result['min_mu'] = mu
    error_result['avg_EBV'] = EBV
    for i in range(0,len(mag)):
        error_result['A_'+mag[i]] = error_result['avg_EBV']*R[i]
    print(error_result.head())
    if s==1:
        error_result.to_csv('%s%i_error_%s_%s_%s.csv'%(data_out+process_step[6],len(error_result),d,col,flag))
    return error_result

def error_correction(error_result, raw, col, dis, flag, s=1):
    correction=pd.DataFrame()
    if dis == '_g':
        rdis = 'plx'
    else:
        rdis = 'IRSB'
    correction['name']=error_result.error_pair
    correction['logP']=raw['logP']
    correction['new_mod'] = raw[rdis] + error_result['min_mu']
    correction['new_EBV'] = raw['EBV'] + error_result['avg_EBV']
    for i in range(0,len(mag)):
        correction['new_M_'+mag[i]] = raw['M_'+mag[i]+dis] + error_result['min_mu'] - error_result['A_'+mag[i]]
        correction['new_M0_'+mag[i]] = raw['M_'+mag[i]+dis] + error_result['min_mu'] - error_result['A0_'+mag[i]]
    if s==1:
        correction.to_csv('%s%i_result_%s_%s_%s.csv'%(data_out+process_step[7],len(correction), dis, col,flag))
    return correction


def star_dispersion(index, dis_list, red, ext, col):
    star = pd.DataFrame()
#    star['ex_g'] = red[].iloc[index]
#    star['ex_i'] = 



def result(raw_data, residue, dslope, dis_flag, col, flag, s=1):
    col_list=[]
    for c in col: # for four interesting wesenheits BV, VI, VK, JK
        del_mu, red_dis_list, ex_dis_list= all_dis_reddening(residue,dslope, dis_flag, c, flag, s)
        dis_list = []
        k=0
        for red, ext in red_dis_list, ex_dis_list:
            d = dis_flag[k]
            rms_df, EBV_df, dispersion_list = find_rms(residue.name, red, ext, del_mu, c, d, flag, s)
            error_df = find_error_pair(rms_df, EBV_df, del_mu, dispersion_list, c, d, flag, s)
            result_df = error_correction(error_df, raw_data, c, d, flag, s)
            #print(result_df)
            dis_list.append(result_df)
            k=k+1
        col_list.append(dis_list)
    return col_list

    

