### File: ./main.py

from lvtlaw.a_utils import output_directories, load_data, process_step, open_output_dir, flags, s, k, data_cols
from lvtlaw.a_utils import colors,data_dir, input_data_file, data_out, dis_list, dis_flag, wes_cols
from lvtlaw.b_data_transform import transformation, extinction_law, distance, star_frame
from lvtlaw.c_pl_pw import pl_reg     
from lvtlaw.d_residue import residue_analysis
from lvtlaw.e_error_estimation import star_by_star, star_dispersion, result

#from lvtlaw.star_analysis import ex_rd_error
#from lvtlaw.visualization import milky_way, plot_corr

import os
import pandas as pd
clear_screen= lambda: os.system('clear')
clear_screen()

print('Master Thesis Project: Galactic BVIJHK Leavitt Law Calibration \n     Tracing systematic errors in luminosity, distance and reddening for individual Cepheid \n     Author: Shubham Mamgain (mshubham00@gmail.com) \n     Supervisor I: Dr. Jesper Storm (AIP Potsdam)\n     Supervisor II: Prof. Dr. Maria Rosa Cioni \n ')

print(' To start the analysis, store the cleaned_data.csv file in ./data/input/ directory. \n Columns mapping must be done by editing ./lvtlaw/utils.py file. \n') ; print('###'*30)
input('\n The processed data will be saved in ./data/output directory.')
#####################################################################################################
output_directories(data_out, s)
cleaned_data = load_data(input_data_file)
#####################################################################################################
#milky_way(ra,dec, dis_i, '95_Galactic_Cepheids')
df = cleaned_data[data_cols]
#plot_corr(df, 'logP', title = '103_raw_data_IRSB', f=18)
'''
choice = input('Press spacebar and enter for project visualization.')
if choice == ' ':
    cordinate(name, ra, dec, EBV, dis)
'''
print('\n \n Raw data will be transformed into absolute magnitude and weseheit magnitude using the extinction law.')
print('###'*30)
extinction_law()
print(' \n These values will be multiplied with E(B-V) values to calculate extinction in each band for individual Cepheid toward the respective line-of-sight.')
print('###'*30)

#####################################################################################################
star_names=cleaned_data['name']
n = len(star_names)
absolute, extinction, true_absolute, wesenheit = transformation(cleaned_data, s)
print(' \nUsing these results the raw PL, PL_0 and PW relations can be calibrated. \n There are 2 distance methods - IRSB and plx, 2 different approaches - Madore and mine, 4 versions of composite weneheits - BV, VI, VK and JK and 6 photometry bands - BVIJHK. \n \n6 x PL relation x 4 x 2 x 2 = 16 versions of BVIJHK Galactic Leavitt Law.')
#input('Press enter to start the process')
print('###'*30)
#####################################################################################################
merg1= pd.merge(absolute, true_absolute, on="logP")
prepared_regression_data = pd.merge(merg1, wesenheit, on = 'logP')
prepared_regression_data['name'] = star_names 
if s==1:
    prepared_regression_data.to_csv(data_out+process_step[1]+str(len(prepared_regression_data))+ '_prepared_PLdata'+'.csv')
print(prepared_regression_data.head())
print('\n This prepared dataset will be used for deriving PL and PW relations with their respective residues \n')
print('###'*30)

star_frame_list = star_frame(prepared_regression_data)

#####################################################################################################

PLW, residue, prediction= pl_reg(prepared_regression_data, s)
print('\n Press enter to see the PL and PW relation data \n'); print('###'*30)
'''
for i in range(0,17):
    print('\n \t %i \t Relation  Slope, intercept, respective error in Gaia (g) and IRSB (i) cases \n '%(i), PLW[i*6:6*i+6])

print('\n Residues PL and PW relation: \n')
print(residue.head())
print('###'*30)
print('\n PL and PW relation: \n')
print(PLW.head())
print('###'*30)

#####################################################################################################

print('\n'*3 + 'Following begins the residual analysis'+ '\n')
print('###'*30)

dres_S, dpre_S, del_mc_S, dres_M, dpre_M, del_mc_M = residue_analysis(residue, dis_flag, wes_cols, s)
print('Now PW residual correlated with PL residuals - two approaches. \n i) Madore : (m vs. VVI) \n ii) Shubham: (m vs mVI)') 
print('see slope data')
print('###'*30)
print(del_mc_M.head())
print(del_mc_S.head())
print('###'*30)
print('See Madore residue \n', dres_M.head())
print('See Shubham residue \n', dres_S.head())

print(' \n \n Now Decouple distance reddening error')
print('###'*30)

####################################################################################################

slope_data=[del_mc_S, del_mc_M]

#ex,rd =  ex_rd_error(residue, slope_data, dis_flag = dis_flag, cols = col, flags=flags, s=1)

#


star_by_star(residue, slope_data, dis_flag , wes_cols, flags, s=1)

method = []
for flag in flags:
    if flag == '_S':
        dresidue = dres_S
        dslope = del_mc_S
    elif flag == '_M':
        dresidue = dres_M
        dslope = del_mc_M
    lists = result(absolute, residue, dslope, dis_flag, wes_cols, flag, s)
    method.append(lists)

for meth in range(0,2):
    for coll in range(0,4):
        for dist in range(0,2):
            print(method[meth][coll][dist].head())
'''
print('All the processed data is saved in ./data/output/ directory.')
#input('Enter to open the output folder!!')
#open_output_dir(data_out)

