### File: ./data/datamapping.py
'''
0_datamapping.py tells to main.py which dataset should be used through parameter k = [0 ,1, 2]. A function select_data_file maps the metadata of input with defined variables. Another function provides Fouque extinction law.
'''
module = 'datamapping'
#####################################################################
k=1; 						# k selects dataset [0:Madore, 1:Jesper, 2:Cruz, 3:LMC, 4:SMC]
s=0 ; 						# saves the output
z=0; 						# z switches output to paging mode
plots=0; 					# plots for genrating plots
#####################################################################
flags = ['S'] 				# Madore and Shubham
mode = ['', '0']  			# Absolute mag and True absolute mag for PL and PW
rd_avg_drop = ['H','K'] 	# Not included in estimating reddening variance (f_star_wise)
#####################################################################
wes_show=['BI', 'VI', 'IH', 'JK']
del_mu = [round(i*0.01,2) for i in range(-300,300,2)]
extinction_ratios = {   	# Extinction Law from Fouque 2007
    'B': 1.31,   			# A_b / A_v
    'V': 1.0,    			# A_v / A_v
    'R': 0.845,  			# A_r / A_v
    'I': 0.608,  			# A_i / A_v
    'J': 0.292,  			# A_j / A_v
    'H': 0.181,  			# A_h / A_v
    'K': 0.119 }   			# A_k / A_v 
#####################################################################
col_dot = ['b.', 'g*', 'y+', 'c*', 'g+', 'k.', 'c+', 'r+'] ;
col_lin = ['b-', 'g-', 'y-', 'c-', 'g-', 'k-', 'c-', 'r-'] ;
col_das = ['b--', 'g--', 'y--', 'c--', 'g--', 'k--', 'c--', 'r--']
col_ = ['b', 'g', 'y', 'c', 'g', 'k', 'c', 'r'] ;
#####################################################################
import os, subprocess, sys
#import pandas as pd
#####################################################################
def R_(R_v, mag, extinction_ratios=extinction_ratios):
	# Wavelength dependent value of ratio of total to selective absorption
    r = {}
    for m in mag:
        r[m] = extinction_ratios[m]*R_v
    return r, R_v
##########################################################
def select_data_file(k):
    if k==0:
        filename = '59_madore'
        dis_list = ['HST']
        dis_flag = ['_h']
        mag = ['B', 'V', 'I','J','H','K'];
        R, R_v = R_(R_v = 3.23, mag = mag)
        file_cols = ['name','logP','EBV'] + dis_list + [f'M_{m}' for m in mag]
    elif k ==1:
        filename = '95_jesper'
        dis_list = ['plx']
        dis_flag = ['_g']
        mag = ['B', 'V', 'I','J','H','K'];
        R, R_v = R_(R_v = 3.23, mag = mag)
        file_cols = ['name','logP','EBV'] + dis_list + [f'{m}_mag' for m in mag]
    elif k == 2:
        filename = '20_cluster_cruz'
        dis_list = ['mplx']
        dis_flag = ['_p']
        mag = ['B', 'V', 'I','J','H','K'];
        R, R_v = R_(R_v = 3.23, mag = mag)
        file_cols = ['name','logP','EBV'] + dis_list + [f'{m}_mag' for m in mag]
    elif k == 3:
        filename = '30_LMC'
        dis_list = ['IRSB']
        dis_flag = ['_l']
        mag = ['V', 'I','J', 'K'] 
        R, R_v = R_(R_v = 3.41, mag = mag) #± 0.06
        file_cols = ['name','logP','EBV'] + dis_list + [f'{m}_mag' for m in mag]
    elif k == 4:
        filename = '32_SMC_VIJK'
        dis_list = ['IRSB']
        dis_flag = ['_s']
        mag = ['V', 'I','J', 'K']
        R, R_v = R_(R_v = 2.74, mag = mag) #± 0.13
        file_cols = ['name','logP','EBV'] + dis_list + [f'{m}_mag' for m in mag]
    return filename, file_cols, dis_list, dis_flag, R, mag, R_v
#k = input('Dataset \n')
#####################################################################
file_name, data_cols, dis_list, dis_flag, R, mag, R_v = select_data_file(k)
nreg = 5*len(dis_flag)
data_dir = './data/input/'
data_out=f'./data/{file_name}_{R_v}/'
img_out_path = data_out + '9_plots/'
process_step = ['1_prepared/','2_PLPW/','3_deldel/', '4_reddening/', '5_dispersion/','6_rms/','7_errorpair/', '8_result/', '9_plots/', '0_stars/']
image_step = ['1_datacleaning/','2_PLPW/','3_deldel/', '4_reddening/', '5_dispersion/','6_rms/','7_errorpair/', '8_result/']
#####################################################################
def color_index(mag = mag):
    color_index = []
    for i in range(0,len(mag)):
        for j in range(i+1,len(mag)):
            color_index.append(mag[i]+mag[j])
    return color_index
#wes_show = color_index()
#####################################################################

print(f'* * {module} module loaded!')
