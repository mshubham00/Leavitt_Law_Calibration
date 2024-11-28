### File: ./lvtlaw/data_transform.py
import os
import pandas as pd
import numpy as np
from scipy import stats
from functools import reduce
from lvtlaw.utils import A, R, mag, bands, ap_bands, data_dir, data_file, data_out
from lvtlaw.plot import vertical_7_colomn_plot as v_plt
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

clean_data = pd.read_csv(data_dir+data_file)
    
def extinction_law(mag = mag, A = A, R = R):
    print('Adopting BVIJHK Extinction law and reddening ratio from Fouque (2007): \n')
    print ('Bands \t Extinction \t Reddening')
    for i in range(0,len(mag)):
        print(mag[i],'\t', A[i], '\t \t', R[i], '\n')
    return A, R 

def absolute_magnitude(data = clean_data, ap_bands=ap_bands, bands = bands, disg = '_g', disi = '_i'):
    absolute = pd.DataFrame()
    absolute['logP'] = data['logP'] 
    absolute['IRSB'] = data['IRSB']
    absolute['plx'] = data['plx']
    absolute['EBV'] = data['EBV']
    for i in range(0,len(mag)):
        absolute[bands[i]+disg]=data[ap_bands[i]] - data['plx']
        absolute[bands[i]+disi]=data[ap_bands[i]] - data['IRSB']
    return absolute



def extinction(data = clean_data, R=R, bands = bands):
    extinction = pd.DataFrame()
    extinction['logP'] = data['logP'] 
    extinction['IRSB'] = data['IRSB']
    extinction['plx'] = data['plx']
    extinction['EBV'] = data['EBV']
    for i in range(0,len(mag)):
        extinction[bands[i]]=data['EBV']*R[i]
    return extinction


def true_absolute_magnitude(data = clean_data, R=R, mag=mag, bands=bands, disg = '_g', disi = '_i'):
    tabsolute = pd.DataFrame()
    tabsolute['logP'] = data['logP']
    tabsolute['IRSB'] = data['IRSB']
    tabsolute['plx'] = data['plx']
    tabsolute['EBV'] = data['EBV']
    for i in range(0,len(mag)):
        tabsolute[bands[i]+'0'+disg]=data[mag[i]+'_mag'] - data['plx'] - R[i]*data['EBV']
        tabsolute[bands[i]+'0'+disi]=data[mag[i]+'_mag'] - data['IRSB'] - R[i]*data['EBV']
    return tabsolute



def reddening_free(data = clean_data, R=R, mag=mag, ap_bands=ap_bands, disg = '_g', disi = '_i'):
    wesen = pd.DataFrame()
    wesen['logP'] = data['logP']
    wesen['IRSB'] = data['IRSB']
    wesen['plx'] = data['plx']
    wesen['EBV'] = data['EBV']
    for a in range(0,len(mag)):
        for b in range(a+1,len(mag)):
            for c in range(0,len(mag)):
                wesen[mag[c]+mag[a]+mag[b]+disg] = data[ap_bands[c]] - (R[c]/(R[a]-R[b]))*(data[ap_bands[a]] - data[ap_bands[b]]) - data['plx']
                wesen[mag[c]+mag[a]+mag[b]+disi] = data[ap_bands[c]] - (R[c]/(R[a]-R[b]))*(data[ap_bands[a]] - data[ap_bands[b]]) - data['IRSB']
    return wesen


def transformation(data, R=R, A=A):
    abs_data = absolute_magnitude(data)
    print('\n Absolute data \n', abs_data.info())
    input('--')
    ext_data = extinction(data)
    print('\n Extinction data: \n', ext_data.info())
    input('--')
    tabs_data = true_absolute_magnitude(data)
    print('\n True Absolute Magnitude: \n',tabs_data.info())
    wes_data = reddening_free(data)
    input('press Enter to see wesenheit data')
    print(wes_data.info())
    print('\n List of columns name: \n', wes_data.columns[0:20], wes_data.columns[21:40])
    input('--')
    print(wes_data.head())
    return abs_data, ext_data, tabs_data, wes_data
