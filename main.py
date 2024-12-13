### File: ./main.py

from lvtlaw.utils import colors,data_dir, data_file, data_out
import pandas as pd
from lvtlaw.pl_pw import pl_reg     #pl_reg(data,'_g','_i') -> PLW, residue, prediction
from lvtlaw.data_transform import transformation, extinction_law
from lvtlaw.residue import residue_analysis
#from lvtlaw.error_estimation import decouple_error

import os
clear_screen= lambda: os.system('clear')
clear_screen()

print('Master Thesis Project: Calibration of Galactic Leavitt Law by determining distance and reddening errors of individual Cepheid \n Author: Shubham Mamgain (smamgain@aip.de) \n Supervisor II: Dr. Jesper Storm \n Supervisor I: Prof. Dr. Maria Rosa Cioni \n ')
input(' To start the analysis, store the cleaned_data.csv file in ./data/input/ directory. \n Press enter to continue')
print('###'*30)
#####################################################################################################
cleaned_data = pd.read_csv(data_dir+data_file)
print(' \n Data Loaded from: \t', data_dir+data_file)
print( cleaned_data.info())
input('\n \n Raw data will be transformed into absolute magnitude and weseheit magnitude using the extinction law.')
print('###'*30)
extinction_law()

input(' \n These values will be multiplied with E(B-V) values to calculate extinction in each band for individual Cepheid toward the respective line-of-sight.')
print('###'*30)

#####################################################################################################

name=cleaned_data['ID']
absolute, extinction, true_absolute, wesenheit = transformation(cleaned_data)
absolute.to_csv(data_out+str(len(absolute))+ 'abs_data'+'.csv')
extinction.to_csv(data_out+ str(len(extinction))+ 'ext_data'+'.csv')
true_absolute.to_csv(data_out+str(len(true_absolute))+ 'true_abs_data'+'.csv')
wesenheit.to_csv(data_out+str(len(wesenheit))+ 'wes_data'+'.csv')
print('Calculated absolute magnitude: \n', absolute.head())
print('Calculated true-Absolute magnitude: \n', true_absolute.head())
print('Calculated Wesenheit magnitude: \n', wesenheit.head())
input(' \n Using these results the raw PL, PL_0 and PW relations can be deduced. \n')
print('###'*30)
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
print(prepared_regression_data.head())
input('\n This prepared dataset will be used for deriving PL and PW relations with their respective residues \n')
print('###'*30)
#####################################################################################################

PLW, residue, prediction= pl_reg(prepared_regression_data)
input('\n Press enter to see the PL and PW relation data \n')
print('###'*30)
residue.to_csv('%s%i_residue.csv'%(data_out,len(residue)))
prediction.to_csv('%s%i_prediction.csv'%(data_out,len(prediction)))
PLW.to_csv('./%s%i_regression.csv'%(data_out,len(PLW)))

for i in range(0,17):
    print('\n \t %i \t Relation  Slope, intercept, respective error in Gaia (g) and IRSB (i) cases \n '%(i), PLW[i*6:6*i+6])


input('\n Model Residues: \n')
print('###'*30)
print(residue.head())
#####################################################################################################

input('\n'*3 + 'Following begins the residual analysis'+ '\n')
print('###'*30)

dres , dpre, del_mc, dres_M, dpre_M, del_mc_M = residue_analysis(colors,s=1)
input('See residue')
print('###'*30)
print('My approach \n', dres.head())
print(del_mc.head())


input('see Madore approach')
print('###'*30)
print('Madore Approach \n', dres_M.head())
print(del_mc_M.head())

input(' \n \n Press Enter to decouple distance reddening error')
print('###'*30)

####################################################################################################

input('Enter to exit!!')
