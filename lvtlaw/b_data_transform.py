### File: ./lvtlaw/b_data_transform.py
'''
This code converts multiband apparent magnitude and reddening of into extinction, absolute magnitude, true absolute magnitude and wesenheit magnitude in all possible color combinations. The reddening law is adopted from Fouque (2007) derived using Galactic reddening ratio, R_v. The value of reddening ratio taken from a_utils.py   

The output will be saved in 'data/{DatasetName_Rv}/1_prepared/*.csv'

Function contained:
	R123(m,c1,c2): Calculate composite reddening ratio using three bands.
	extinction_law(): Prints the Galactic extinction law as of Table 7 of Fouque 2007.
	extinction(data): Converts reddening into extinction of dataset.
	absolute_magnitude(data): Converts apparent magnitude into absolute magnitude.
	true_absolute_magnitude (absolute_magnitude): Impliment extinction correction on absolute magnitude. 
	reddening_free (absolute_magnitude): Calculate composite wesenheit magnitudes
    transformation(data): calls the above functions and save the results as csv files. 
'''

from lvtlaw.a_utils import A, R, mag, data_dir, input_data_file, dis_flag, data_out, dis_list, process_step, colors, k, s

import pandas as pd
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

def R123(m:str,c1:str,c2:str,R=R):
    R123 = R[mag.index(m)] / (R[mag.index(c1)] - R[mag.index(c2)])
    return R123

def extinction_law(mag = mag, A = A, R = R):
    print('Adopting BVIJHK Extinction law and reddening ratio from Fouque (2007): \n')
    print ('Bands \t Extinction \t Reddening ratio \n \t A(x)/A(v) \t R(x) for E(B-V)')
    for i in range(0,len(mag)):
        print(mag[i],'\t', A[i], '\t \t', R[i], '\n')
    return A, R 

def extinction(data, R=R, mag = mag):
    extinction = pd.DataFrame({'name': data['name'], 'logP': data['logP'], 'EBV': data['EBV']})
    for i in range(0,len(mag)):
        extinction['A_'+mag[i]]=data['EBV']*R[i]
    print(extinction.head())
    print('###'*30)
    return extinction

def absolute_magnitude(data, R=R, mag=mag, dis_flag=dis_flag, dis_list=dis_list, k=k):
    absolute = pd.DataFrame({
        'name': data['name'],
        'logP': data['logP'],
        'EBV': data['EBV']})
    for i, d in enumerate(dis_list):
        absolute[d] = data[d]
        for m in mag:
            if k == 0:  # Madore dataset
                absolute[f'M_{m}{dis_flag[i]}'] = data[f'M_{m}'] + data['EBV'] * R[i]
            else:
                absolute[f'M_{m}{dis_flag[i]}'] = data[f'{m}_mag'] - data[dis_list[i]]
    print(absolute.head())
    print('###' * 30)
    return absolute

def true_absolute_magnitude(absolute, R=R, mag=mag, dis_flag=dis_flag, dis_list=dis_list, k=k):
    tabsolute = pd.DataFrame({'name': absolute['name'], 'logP': absolute['logP'], 'EBV': absolute['EBV']})
    for d,dis in enumerate(dis_list):
        tabsolute[dis] = absolute[dis]    
        for i,m in enumerate(mag):
                tabsolute[f'M_{m}0{dis_flag[d]}']=absolute[f'M_{m}{dis_flag[d]}']  - R[i]*absolute['EBV']    
    print(tabsolute.head())
    print('###'*30) 
    return tabsolute

def reddening_free(absolute, R=R, mag=mag, dis_flag=dis_flag, k=k):
    wesen = pd.DataFrame({'name': absolute['name'], 'logP': absolute['logP'], 'EBV': absolute['EBV']})
    for d,dis in enumerate(dis_flag):
        for c,m in enumerate(mag):
            for a,c1 in enumerate(mag):
                for b,c2 in enumerate(mag[a+1:]):
                    wes_str = m+c1+c2+dis
                    Rm12 = R123(m,c1,c2)
                    wesen[wes_str] = absolute[f'M_{m}{dis}'] - Rm12*(absolute[f'M_{c1}{dis}'] - absolute[f'M_{c2}{dis}'])
                    wesen[wes_str+'0'] = (absolute[f'M_{m}{dis}'] - absolute['EBV'] * R[c]) - Rm12*(absolute[f'M_{c1}{dis}'] - absolute['EBV'] * R[a] - absolute[f'M_{c2}{dis}'] - absolute['EBV'] * R[b])
    print(wesen.head())
    print('###'*30)
    return wesen

def transformation(data, R=R, mag=mag, dis_flag=dis_flag, dis_list=dis_list, k=k, s=s):
    print('Absolute magnitude for each band \n')
    abs_data = absolute_magnitude(data, R, mag, dis_flag, dis_list, k)    
    print('Calculated extinction for each band \n')
    ext_data = extinction(data, R, mag)
    print('True absolute magnitude for each band \n')
    tabs_data = true_absolute_magnitude(abs_data, R, mag, dis_flag, dis_list, k)
    print('Wesenheit magnitude for each band \n')
    wes_data = reddening_free(abs_data, R, mag, dis_flag, k)
    merg1= pd.merge(abs_data, tabs_data, on="logP")
    prepared_regression_data = pd.merge(merg1, wes_data, on = 'logP')

    if s==1:
        abs_data.to_csv(data_out+process_step[0]+str(len(abs_data))+ '_abs_data'+'.csv')
        ext_data.to_csv(data_out+process_step[0]+ str(len(ext_data))+ '_ext_data'+'.csv')
        tabs_data.to_csv(data_out+process_step[0]+str(len(tabs_data))+ '_true_abs_data'+'.csv')
        wes_data.to_csv(data_out+process_step[0]+str(len(wes_data))+ '_wes_data'+'.csv')
    #print('\n Number of wesenheit functions: \n', len(wes_data.columns) - 4) # why 4?
    #print('###'*30)
        prepared_regression_data.to_csv(data_out+process_step[0]+str(len(prepared_regression_data))+ '_prepared_PLdata'+'.csv')

    return  abs_data, ext_data, tabs_data, wes_data, prepared_regression_data
        

    
    
    
    
    
    
    
    
    
    
    
    
    
    

