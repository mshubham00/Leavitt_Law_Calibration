### File: ./lvtlaw/a_utils.py
'''
a_utils.py tells to main.py which dataset should be used through parameter k = [0 ,1, 2] = [Madore, Jesper, Reiss]. A function select_data_file maps the metadata of input with defined variables. Another function provides Fouque extinction law. File also contains more generic function like regression, save_data, etc. and input/output variables.
'''
#####################################################################
k = 1; s=1; z=0; 
# k changes dataset, s saves the output, z switches intracting output, flag for Madore/Shubham
flags = ['M']

R_v = 3.23; # for milky way Sandage (2004)
#R_v = 3.41# ± 0.06 in the LMC and 
#R_v = 2.74 #± 0.13 in the SMC. (2023)
#####################################################################
import os, subprocess, sys
import matplotlib.pyplot as plt
from scipy import stats

import pandas as pd
#####################################################################
"""
Extinction Law from Fouque 2007

""" 
Ab_v = 1.31                                             #          = A_b / A_v
Av_v = 1                                                #          = A_v / A_v
Ar_v = 0.845 	                                        #          = A_v / A_v
Ai_v = 0.608                                            #          = A_i / A_v
Aj_v = 0.292                                            #          = A_j / A_v
Ah_v = 0.181                                            #          = A_h / A_v
Ak_v = 0.119                                            #          = A_k / A_v
'''
Ratio of total to selective absorption (Sandage 2004)- driving wavelength dependent value of R
'''
#R_v = 3.23                                             #      R_v = A_v / E(B-V)
R_b = Ab_v*R_v                                          #      R_b = (A_b / A_v) * (A_v / E(B-V))
R_r = Ar_v*R_v                                          #      R_r = (A_r / A_v) * (A_v / E(B-V))
R_i = Ai_v*R_v                                          #          = (A_i / A_v) * (A_v / E(B-V))
R_j = Aj_v*R_v                                          #          = (A_j / A_v) * (A_v / E(B-V))
R_h = Ah_v*R_v                                          #          = (A_h / A_v) * (A_v / E(B-V))
R_k = Ak_v*R_v                                          #          = (A_k / A_v) * (A_v / E(B-V))

##########################################################
def select_data_file(k):
    if k==0:
        file_name = '59_madore'
        file_cols = ['name','logP','HST','EBV','M_B','M_V','M_I','M_J','M_H','M_K'] 
        dis_list = ['HST']
        dis_flag = ['_h']
        A = [Ab_v, Av_v, Ai_v, Aj_v, Ah_v, Ak_v]
        R = [R_b, R_v, R_i, R_j, R_h, R_k]
        mag = ['B', 'V', 'I','J','H','K'];
        abs_bands = ['M_B', 'M_V', 'M_I', 'M_J', 'M_H', 'M_K']; 
        ap_bands = ['B_mag', 'V_mag', 'I_mag', 'J_mag', 'H_mag', 'K_mag']
    elif k ==1:
        file_name = '95_jesper'
        file_cols = ['name',"logP", 'plx', 'EBV', "B_mag", 'V_mag', 'I_mag', 'J_mag', 'H_mag', 'K_mag']
        dis_list = ['plx']
        dis_flag = ['_g']
        A = [Ab_v, Av_v, Ai_v, Aj_v, Ah_v, Ak_v]
        R = [R_b, R_v, R_i, R_j, R_h, R_k]
        mag = ['B', 'V', 'I','J','H','K'];
        abs_bands = ['M_B', 'M_V', 'M_I', 'M_J', 'M_H', 'M_K']; 
        ap_bands = ['B_mag', 'V_mag' ,'I_mag', 'J_mag', 'H_mag', 'K_mag']
    elif k == 2:
        file_name = '18_cluster'
        file_cols = ['name',"logP", 'cluster', 'EBV', "B_mag", 'V_mag', 'I_mag', 'J_mag', 'H_mag', 'K_mag']
        dis_list = ['cluster']
        dis_flag = ['_c']
        A = [Ab_v, Av_v, Ai_v, Aj_v, Ah_v, Ak_v]
        R = [R_b, R_v, R_i, R_j, R_h, R_k]
        mag = ['B', 'V', 'I','J','H','K'];
        abs_bands = ['M_B', 'M_V', 'M_I', 'M_J', 'M_H', 'M_K']; 
        ap_bands = ['B_mag', 'V_mag' ,'I_mag', 'J_mag', 'H_mag', 'K_mag']
    elif k == 3:
        file_name = '36_LMC'
        file_cols = ['name',"logP", 'IRSB', 'EBV', 'V_mag', 'I_mag', 'J_mag', 'K_mag']
        dis_list = ['IRSB']
        dis_flag = ['_l']
        A = [Av_v, Ai_v, Aj_v,  Ak_v]
        R = [R_v, R_i, R_j, R_k]
        mag = ['V', 'I','J','K']
        abs_bands = ['M_V', 'M_I', 'M_J', 'M_K']; 
        ap_bands = ['V_mag' ,'I_mag', 'J_mag', 'K_mag']
    elif k == 4:
        file_name = '20_cluster_cruz'
        file_cols = ['name',"logP", 'mplx', 'IRSB', 'EBV','B_mag', 'V_mag', 'I_mag', 'J_mag', 'H_mag','K_mag']
        dis_list = ['IRSB']
        dis_flag = ['_c']
        A = [Ab_v, Av_v, Ai_v, Aj_v, Ah_v, Ak_v]
        R = [R_b, R_v, R_i, R_j, R_h, R_k]
        mag = ['B', 'V', 'I','J','H','K'];
        abs_bands = ['M_B', 'M_V', 'M_I', 'M_J', 'M_H', 'M_K']; 
        ap_bands = ['B_mag', 'V_mag' ,'I_mag', 'J_mag', 'H_mag', 'K_mag']
    return file_name, file_cols, dis_list, dis_flag, A, R, mag, abs_bands, ap_bands
#k = input('Dataset \n')
input_data_file, data_cols, dis_list, dis_flag, A, R, mag, abs_bands, ap_bands = select_data_file(k)
nreg = 5*len(dis_flag)
#####################################################################
data_dir = './data/input/'
data_out=f'./data/{input_data_file}_{R_v}/'
img_out_path = './data/output/9_plots/'
process_step = ['1_prepared/','2_PLPW/','3_deldel/', '4_reddening/', '5_dispersion/','6_rms/','7_errorpair/', '8_result/', '9_plots/', '0_stars/']
image_step = ['1_datacleaning/','2_PLPW/','3_deldel/', '4_reddening/', '5_dispersion/','6_rms/','7_errorpair/', '8_result/']
#####################################################################
del_mu = [round(i*0.01,2) for i in range(-100,100,2)]
band = len(mag);
col_dot = ['b.', 'g*', 'y+', 'c*', 'g+', 'k.', 'c+', 'r+'] ;
col_lin = ['b-', 'g-', 'y-', 'c-', 'g-', 'k-', 'c-', 'r-'] ;
col_das = ['b--', 'g--', 'y--', 'c--', 'g--', 'k--', 'c--', 'r--']
col_ = ['b', 'g', 'y', 'c', 'g', 'k', 'c', 'r'] ;
#####################################################################
def output_directories(parent_folder = data_out, s=1,subdirectories = process_step):
    if s==1:
        for subdirectory in subdirectories:
            path = os.path.join(parent_folder, subdirectory)
            if not os.path.exists(path):
                os.makedirs(path)
#####################################################################       
def image_directories(parent_folder = img_out_path, s=1,subdirectories = image_step):
    if s==1:
        for subdirectory in subdirectories:
            path = os.path.join(parent_folder, subdirectory)
            if not os.path.exists(path):
                os.makedirs(path)
#####################################################################       
def load_data(data_file = input_data_file, data_dir = data_dir, p=0):
    cleaned_data = pd.read_csv(data_dir+data_file+'.csv')
    if p==1:
        print(' \n Data Loaded from: \t', data_dir+data_file)
        print( cleaned_data.info())
    return cleaned_data #, name, ra, dec, EBV, dis
#####################################################################
def save(title, step=0, img_path=img_out_path, fil = 'pdf', p=0):                                   #   2
    if p == 1:
        print(img_path+process_step[step]+title+'.'+fil)
    plt.savefig('%s%s.%s'%(img_path+process_step[step],title, fil))
#####################################################################
def open_output_dir(path):  
    # Open the output folder after process completion
    subprocess.run(['xdg-open', path])
#####################################################################
def color_index(mag = mag):
    color_index = []
    for i in range(0,len(mag)):
        for j in range(i+1,len(mag)):
            color_index.append(mag[i]+mag[j])
    #print('Possible %i combinations of color indexes (str): \n'%(len(color_index)), color_index)
    return color_index
colors = color_index()
wes_show = color_index()#['BV','VI','VK','JK']; 
wes_cols = colors
#####################################################################
def regression(x: list, y: list, x_str: str, y_str: str, p = 0):
    regression_line = stats.linregress(x, y); 
    m = regression_line.slope; 
    c = regression_line.intercept
    prediction = m * x + c; 
    residue = y-prediction 
    m_error = regression_line.stderr; 
    c_error = regression_line.intercept_stderr
    if p == 1:
        print('%s = %f %s ( %f) + %f ( %f)'%(y_str, m, x_str, m_error, c, c_error))
    return m, c, prediction, residue, m_error, c_error
#####################################################################
def pr_value(x,y,p=0):
    p,r = stats.pearsonr(x,y)
    if p==1:
        print('Pearson R:', r)
        print('P-value:', p)
    return p,r
#####################################################################
def RA_DEC_DIS_to_Galactocentric(ra, dec, dis):
    ra = Longitude(ra, unit=u.degree)
    dec = Latitude(dec, unit = u.degree)                        #   1
    dis = 10**(1 + dis/5)/1000          # modulus to kpc
    dis = Distance(dis, unit = u.kpc)
    coordinate = SkyCoord(ra=ra, dec=dec, distance=dis, frame='icrs')
    coordinate = coordinate.transform_to(Galactocentric(galcen_distance=8.1*u.kpc))
    return coordinate
#####################################################################
