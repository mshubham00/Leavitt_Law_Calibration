### File: ./main.py
import os, sys, pandas as pd ; clear_screen= lambda: os.system('clear'); clear_screen()
from data.datamapping import file_name, data_cols
from lvtlaw.a_utils import output_directories, image_directories, load_data, open_output_dir
from lvtlaw.main_modules import * 
#from lvtlaw.h_loadoutput import starwise_analysis # to load processed data
#####################################################################################################

#Generate directories for saving output
output_directories(); 
image_directories(); 

# Display project related details
intro()

# Load data and select relevant coloumns
input_data, raw, mag, dis = load_data(file_name) # a_utils

# Transform data into wesenheit magnitude
raw, absolute, extinction, tabsolute, wesenheit, merged_data = mag_transformation(raw) # b_data_transform

# Deduce PL and PW relations
PLW_mc, residue, prediction, merged_data = PLWcorrection(merged_data) # c_pl_pw

# Correlate residues of PL and PW relations
dmc, dres, dpre, merged_data = residual_correlation(merged_data) # d_del_del

# Trace reddening error for varying modulus
ex0_df, red0_df, mu_df_list_dict, merged_data = rd_mu_error_matrix(merged_data, dmc) # e_error_estimation

# Decoupling reddening-modulus error star by star
star_list, ex_red_mu_list, correction_rd_mu, merged_data = starwise_analysis(merged_data, mu_df_list_dict) # f_star_wise
#print('loaded!')

# Implimenting the corrections in raw data
calibrated_result(merged_data, correction_rd_mu, plots=1) # g_result

print(f'All the processed data is saved in {data_out} directory.')
#input('Enter to open the output folder!!')
#input('* * Success!')
open_output_dir(data_out)

