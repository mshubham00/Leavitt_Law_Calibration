### File: ./main.py
import os, sys, pandas as pd ; clear_screen= lambda: os.system('clear'); clear_screen()
from lvtlaw.a_utils import output_directories, load_data, process_step, open_output_dir, data_cols, z, flags, A, R
from lvtlaw.a_utils import data_dir, file_name, data_out, mag, colors, wes_show, dis_list, dis_flag, del_mu, s, k
from lvtlaw.main_modules import intro, data_loaded, trans, star_list, regress, res_analysis, redd_err, correction, load_ex_mu
load = 1
intro(data_out, z)
output_directories(data_out, s)
cleaned_data = load_data(file_name)
df = cleaned_data[data_cols].dropna().reset_index(drop=True); n = len(df)  # total number of cepheids
data_loaded(file_name, R, k, df)
#####################################################################################################
raw, absolute, extinction, tabsolute, wesenheit, prepared_regression_data = trans(mag, A, R, cleaned_data, dis_flag, dis_list, k, s, z)

if load==0:
    stars_ex_red_mu_list = load_ex_mu(n)
else: 
    star_frame_list = star_list(prepared_regression_data, mag, wes_show, z)
    PLW, residue, prediction, star_frame_list = regress(prepared_regression_data, star_frame_list, s, z)
    dres, dpre, dmc, star_frame_list, dSM = res_analysis(residue, dis_flag, wes_show, flags, star_frame_list, s,z)
    red0_df_list, mu_df_list_dict, stars_ex_red_mu_list = redd_err(df, wes_show, dis_flag, dSM, flags, del_mu,s,z)
####################################################################################################
correction(stars_ex_red_mu_list, tabsolute, flags, dis_flag, s, z)
print(f'All the processed data is saved in {data_out} directory.')
####################################################################################################

#star_frame_list = add_dres(star_frame_list, dres_S, dres_M)
#input('Enter to open the output folder!!')
#open_output_dir(data_out)

