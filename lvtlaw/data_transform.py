### File: ./lvtlaw/data_transform.py
import os
import pandas as pd
import numpy as np
from scipy import stats
from functools import reduce
from lvtlaw.utils import A, R, mag, ap_bands, abs_bands, data_dir, input_data_file, dis_flag, data_out, dis_list, process_step
from lvtlaw.plot import vertical_7_colomn_plot as v_plt
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
#clean_data = pd.read_csv(data_dir+data_file)
    
def extinction_law(mag = mag, A = A, R = R):
    print('Adopting BVIJHK Extinction law and reddening ratio from Fouque (2007): \n')
    print ('Bands \t Extinction \t Reddening')
    for i in range(0,len(mag)):
        print(mag[i],'\t', A[i], '\t \t', R[i], '\n')
    return A, R 


def distance(data, dis_list):
    dis_data = pd.DataFrame(dis_list)
    dis_data['logP'] = data['logP']
    for i in dis_list:
        dis_data[i] = data[i]
    return dis_data


def extinction(data, R=R, bands = abs_bands):
    extinction = pd.DataFrame()
    extinction['name'] = data['ID'] 
    extinction['logP'] = data['logP'] 
    extinction['IRSB'] = data['IRSB']
    extinction['plx'] = data['plx']
    extinction['EBV'] = data['EBV']
    for i in range(0,len(mag)):
        extinction['A_'+mag[i]]=data['EBV']*R[i]
    print(extinction.head())
    print('###'*30)
    return extinction


def absolute_magnitude(data, ap_bands=ap_bands, bands = abs_bands, disg = '_g', disi = '_i'):
    absolute = pd.DataFrame()
    absolute['name'] = data['ID'] 
    absolute['logP'] = data['logP'] 
    absolute['IRSB'] = data['IRSB']
    absolute['plx'] = data['plx']
    absolute['EBV'] = data['EBV']
    for i in range(0,len(mag)):
        absolute[bands[i]+disg]=data[ap_bands[i]] - data['plx']
        absolute[bands[i]+disi]=data[ap_bands[i]] - data['IRSB']
    print(absolute.head())
    print('###'*30)
    return absolute



def true_absolute_magnitude(data, R=R, mag=mag, bands=abs_bands, disg = '_g', disi = '_i'):
    tabsolute = pd.DataFrame()
    tabsolute['logP'] = data['logP']
    tabsolute['IRSB'] = data['IRSB']
    tabsolute['plx'] = data['plx']
    tabsolute['EBV'] = data['EBV']
    for d in range(0,len(dis_list)):
        for i in range(0,len(mag)):
            tabsolute[bands[i]+'0'+dis_flag[d]]=data[mag[i]+'_mag'] - data[dis_list[d]] - R[i]*data['EBV']
    print(tabsolute.head())
    print('###'*30)
    return tabsolute



def reddening_free(data, R=R, mag=mag, ap_bands=ap_bands, disg = '_g', disi = '_i'):
    wesen = pd.DataFrame()
    wesen['logP'] = data['logP']
    wesen['IRSB'] = data['IRSB']
    wesen['plx'] = data['plx']
    wesen['EBV'] = data['EBV']
    for a in range(0,len(mag)):
        for b in range(a+1,len(mag)):
            for c in range(0,len(mag)):
                for d in range(0,len(dis_list)):
                    wesen[mag[c]+mag[a]+mag[b]+dis_flag[d]] = data[ap_bands[c]] - (R[c]/(R[a]-R[b]))*(data[ap_bands[a]] - data[ap_bands[b]]) - data[dis_list[d]]
    print(wesen.head())
    print('###'*30)
    return wesen


def transformation(data,  s = 1, R=R, A=A):
    print('Absolute magnitude for each band \n')
    abs_data = absolute_magnitude(data)    
    print('Calculated extinction for each band \n')
    ext_data = extinction(data)
    print('True absolute magnitude for each band \n')
    tabs_data = true_absolute_magnitude(data)
    print('Wesenheit magnitude for each band \n')
    wes_data = reddening_free(data)
    if s==1:
        abs_data.to_csv(data_out+process_step[0]+str(len(abs_data))+ '_abs_data'+'.csv')
        ext_data.to_csv(data_out+process_step[0]+ str(len(ext_data))+ '_ext_data'+'.csv')
        tabs_data.to_csv(data_out+process_step[0]+str(len(tabs_data))+ '_true_abs_data'+'.csv')
        wes_data.to_csv(data_out+process_step[0]+str(len(wes_data))+ '_wes_data'+'.csv')
    print('\n Number of wesenheit functions: \n', len(wes_data.columns) - 4)
    print('###'*30)
    return  abs_data, ext_data, tabs_data, wes_data
