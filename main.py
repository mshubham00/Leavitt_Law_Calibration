### File: ./main.py
import os, sys, pandas as pd ; clear_screen= lambda: os.system('clear'); clear_screen()
from data.datamapping import file_name, data_cols, skip, R
from lvtlaw.a_utils import open_output_dir
from lvtlaw.main_modules import * 
from lvtlaw.h_loadoutput import starwise_analysis_ # to load processed data
#####################################################################################################
# Display project related details
#skip=1
def skip_to(skip = skip):
    if skip == 0:
        #Generate directories for saving output

        intro()
            
        # Load data and select relevant coloumns
        input_data, raw, mag, dis = load_data(file_name) # a_utils

        # Transform data into wesenheit magnitude
        raw, absolute, extinction, tabsolute, wesenheit, merged_data = mag_transformation(raw) #b_data_transform

        # Deduce PL and PW relations
        PLW_mc, residue, prediction, merged_data = PLWcorrection(merged_data) # c_pl_pw

        # Correlate residues of PL and PW relations
        dmc, dres, dpre, merged_data = residual_correlation(merged_data,plots=0) # d_del_del

        # Trace reddening error for varying modulus
        ex0_df, rd0_df, mu_df_list_dict, merged_data = rd_mu_error_matrix(merged_data, dmc) # e_error_estimation

        # Decoupling reddening-modulus error star by star
        stars, rdmu_list, rd_mu_rms, merged_data = starwise_analysis(merged_data, mu_df_list_dict) # f_star_wise
        
        # Implimenting the corrections in raw data 
        calibrated_result(merged_data, rd_mu_rms, plots=0) # g_result

    else:
#        ex0_df, rd0_df, mu_df_list_dict, merged_data = rd_mu_error_matrix_() # e_error_estimation
        stars, rdmu_list, rd_mu_rms, merged_data = starwise_analysis_()

        # Implimenting the corrections in raw data
        calibrated_result(merged_data, rd_mu_rms, plots=1) # g_result

skip_to()
print(f'All the processed data is saved in {data_out} directory.')
#open_output_dir(data_out)

