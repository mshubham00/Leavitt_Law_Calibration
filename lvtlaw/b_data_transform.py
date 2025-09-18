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
module = 'b_data_transform'

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
#####################################################################
from data.datamapping import R, mag, data_dir, file_name, dis_flag, data_out, dis_list, process_step, k, s, z, extinction_ratios
from lvtlaw.a_utils import merge_12, imgsave
#####################################################################
def R123(m:str,c1:str,c2:str,R=R):
    # calculate composite reddening ratio for wesenheit functions
    R123 = R[m] / (R[c1] - R[c2])
    return R123
#####################################################################
def extinction_law(mag = mag, A = extinction_ratios, R = R):
    print('Adopting BVIJHK Extinction law and reddening ratio from Fouque (2007): \n')
    print ('Bands \t Extinction \t Reddening ratio \n \t A(x)/A(v) \t R(x) for E(B-V)')
    for i in mag:
        print(i,'\t', extinction_ratios[i], '\t \t', R[i], '\n')
    return A, R 
#####################################################################
def extinction(data, R=R, mag = mag):
    #converts reddening into extinction
    extinction = pd.DataFrame({'name': data['name'], 'logP': data['logP'], 'EBV': data['EBV']})
    for i in mag:
        extinction['A_'+i]=data['EBV']*R[i]
    print(extinction.head())
    print('###'*30)
    return extinction
#####################################################################
def absolute_magnitude(data, R=R, mag=mag, dis_flag=dis_flag, dis_list=dis_list, k=k):
    absolute = pd.DataFrame({
        'name': data['name'],
        'logP': data['logP'],
        'EBV': data['EBV']})
    for d, dis in enumerate(dis_list):
        absolute[dis] = data[dis]
        for i, m in enumerate(mag):
            if k == 0:  # Madore dataset
                absolute[f'M_{m}{dis_flag[d]}'] = data[f'M_{m}'] + R[m]*data['EBV']
            else:
                absolute[f'M_{m}{dis_flag[d]}'] = data[f'{m}_mag'] - data[dis_list[d]]
    print(absolute.head())
    print('###' * 30)
    return absolute
#####################################################################
def true_absolute_magnitude(absolute, extinction, mag=mag, dis_flag=dis_flag, dis_list=dis_list):
    tabsolute = pd.DataFrame({'name': absolute['name'], 'logP': absolute['logP'], 'EBV': absolute['EBV']})
    for d,dis in enumerate(dis_list):
        tabsolute[dis] = absolute[dis]    
        for i,m in enumerate(mag):
                tabsolute[f'M_{m}0{dis_flag[d]}']=absolute[f'M_{m}{dis_flag[d]}'] - extinction['A_'+m]    
    print(tabsolute.head())
    print('###'*30) 
    return tabsolute
#####################################################################
def reddening_free(absolute, R=R, mag=mag, dis_flag=dis_flag):
    wesen = pd.DataFrame({'name': absolute['name'], 'logP': absolute['logP'], 'EBV': absolute['EBV']})
    for d,dis in enumerate(dis_flag):
        wesen[dis_list[d]] = absolute[dis_list[d]]
        for c,m in enumerate(mag):
            for a,c1 in enumerate(mag):
                for b,c2 in enumerate(mag[a+1:]):
                    wes_str = m+c1+c2+dis
                    Rm12 = R123(m,c1,c2)
                    wesen[wes_str] = absolute[f'M_{m}{dis}'] - Rm12*(absolute[f'M_{c1}{dis}'] - absolute[f'M_{c2}{dis}'])
                    #print(f'{m+c1+c2}: {Rm12}')
                    #wesen[wes_str] = absolute[f'M_{m}0{dis}']- Rm12*(absolute[f'M_{c1}0{dis}']- absolute[f'M_{c2}0{dis}'])
    print(wesen.head())
    print('###'*30)
    return wesen
#####################################################################
def transformation(data, R=R, A=extinction_ratios, mag=mag, dis_flag=dis_flag, dis_list=dis_list, s=s, z=z):
    A, R = extinction_law(mag = mag, A = extinction_ratios, R = R) # converts Fouque (2007) extinction law into corresponding reddening ration
    print(' \n Reddening ratio values will be multiplied with E(B-V) values to yield extinction in each band for individual Cepheid along the respective line-of-sight.  \n')
    print('###'*30)
    print('\nApparent magnitude transformed into absolute magnitude and weseheit magnitude using the Galactic extinction law, Reddenings (EBV) and Distance modulus (mu).\n M  = m - mu \n M0 = m - mu - R*EBV \n W  = m - mu - R*(m1-m2) \n')
    if z==1:
        input('\n')
    data = data
    print('###'*30)
    print('Apparent magnitude')
    print(data.head())
    print('###'*30)
    print('Absolute magnitude for each band \n')
    abs_data = absolute_magnitude(data)    
    print('Calculated extinction for each band \n')
    ext_data = extinction(data)
    print('True absolute magnitude for each band \n')
    tabs_data = true_absolute_magnitude(abs_data, ext_data)
    print('Wesenheit magnitude for each band \n')
    wes_data = reddening_free(abs_data)
    merged_data= pd.merge(abs_data, tabs_data, on=['name','logP', 'EBV', f'{dis_list[0]}'])
    merged_data = merge_12(merged_data, wes_data, on = ['name','logP', 'EBV', f'{dis_list[0]}'])
    if s==1:
        abs_data.to_csv(data_out+process_step[0]+str(len(abs_data))+ '_abs_data'+'.csv')
        ext_data.to_csv(data_out+process_step[0]+ str(len(ext_data))+ '_ext_data'+'.csv')
        tabs_data.to_csv(data_out+process_step[0]+str(len(tabs_data))+ '_true_abs_data'+'.csv')
        wes_data.to_csv(data_out+process_step[0]+str(len(wes_data))+ '_wes_data'+'.csv')
        merged_data.to_csv(data_out+process_step[0]+str(len(merged_data))+ '_prepared_PLdata'+'.csv')
        print(f'Above data saved in ./{data_out+process_step[0]}\n')
    if z==1:
        input('\n')
    return data, abs_data, ext_data, tabs_data, wes_data, merged_data
#####################################################################
def plot_corr(df, Y='logP', title ='', f=12, s=s):
    sns.set_context("paper", rc={"axes.labelsize": f})
    g = sns.pairplot(data=df, x_vars=df.columns[::], y_vars=Y, kind='scatter')
    g.fig.suptitle(title, fontsize=f)
    g.fig.tight_layout()
    g.fig.subplots_adjust(top=0.9)  # Adjust top to make room for title
    if s == 1:
        imgsave(title,0)    
    plt.show()
#####################################################################
print(f'* * {module} module loaded!')

    
    
    
    
    
    
    
    
    
    
    
    
    

