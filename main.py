### File: ./main.py

from lvtlaw.utils import data_dir, data_file, data_out
import pandas as pd
from lvtlaw.pl_pw import pl_reg     #pl_reg(data,'_g','_i') -> PLW, residue, prediction
from lvtlaw.data_transform import transformation, extinction_law
#from lvtlaw.residue import residue_correlation


import os
clear_screen= lambda: os.system('clear')
clear_screen()

print('Master Thesis Project: Calibration of Galactic Leavitt Law by determining distance and reddening errors of individual Cepheid \n Author: Shubham Mamgain (smamgain@aip.de) \n Supervisor II: Dr. Jesper Storm \n Supervisor I: Prof. Dr. Maria Rosa Cioni \n ')
input(' To start the analysis, store the cleaned_data.csv file in ./data/input/ directory. \n Press enter to continue')

#####################################################################################################
extinction_law()        # Extinction Law from Fouque 2007
input(' \n These values will be embedded with E(B-V) values to calculate extinction in each band for individual Cepheid toward the respective line-of-sight. Please enter to load the data')

#####################################################################################################
cleaned_data = pd.read_csv(data_dir+data_file)
print(' \n Data Loaded from: \t', data_dir+data_file)
print('\n Here is the raw data: \n', cleaned_data.info())
input('--')
print(cleaned_data.head())
input('\n Raw data will be transformed into absolute magnitude and weseheit magnitude.')
name=cleaned_data['ID']
absolute, extinction, true_absolute, wesenheit = transformation(cleaned_data)
absolute.to_csv(data_out+str(len(absolute))+ 'abs_data'+'.csv')
extinction.to_csv(data_out+ str(len(extinction))+ 'ext_data'+'.csv')
true_absolute.to_csv(data_out+str(len(true_absolute))+ 'true_abs_data'+'.csv')
wesenheit.to_csv(data_out+str(len(wesenheit))+ 'wes_data'+'.csv')
print('Calculated absolute, true-Absolute and Wesenheit magnitude: \n', wesenheit.head(), true_absolute.head(), absolute.head())
input(' \n Using these results, raw PL, PL_0 and PW relation can be deduced. \n')
#####################################################################################################
    #v_plt('Raw_data', data,ap_bands, 1, disg='', disi='') 
    #v_plt('absolute_data', abs_data, bands, 1) 
    #v_plt('extinction_data', ext_data, bands, 1, disg='', disi='') 
    #v_plt('true_absolute_data', tabs_data, bands, 1, disg = '0_g', disi='0_i') 
#####################################################################################################
merg1= pd.merge(absolute, true_absolute, on="logP")
prepared_regression_data = pd.merge(merg1, wesenheit, on = 'logP')
prepared_regression_data['name'] = name 
prepared_regression_data.to_csv(data_out+str(len(prepared_regression_data))+ 'prepared_PLdata'+'.csv')
print(prepared_regression_data.info())
input('--')
print(prepared_regression_data.head())
input('\n This dataset will be used for deriving PL and PW relations with their respective residues \n')
#####################################################################################################

PLW, residue, prediction= pl_reg(prepared_regression_data)
input('--')
residue.to_csv('%s%i_residue.csv'%(data_out,len(residue)))
prediction.to_csv('%s%i_prediction.csv'%(data_out,len(prediction)))
PLW.to_csv('./%s%i_regression.csv'%(data_out,len(PLW)))

for i in range(0,17):
    print('\n \t %i \t Relation  Slope, intercept, respective error in Gaia (g) and IRSB (i) cases \n '%(i), PLW[i*6:6*i+6])


input('\n Model Residues: \n')
print(residue.head())
input('\n Model Prediction below \n ')
print('\n',prediction.head())
#####################################################################################################
residue_correlation(PLW)



input('Enter to exit!!')
