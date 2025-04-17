### File: ./lvtlaw/a_utils.py
#####################################################################
k = 1; s=1; R_v = 3.23              
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
Ar_v = 0.845 	                                                #          = A_v / A_v
Ai_v = 0.608                                            #          = A_i / A_v
Aj_v = 0.292                                            #          = A_j / A_v
Ah_v = 0.181                                            #          = A_h / A_v
Ak_v = 0.119                                            #          = A_k / A_v
'''
Ratio of total to selective absorption (Sandage 2004)- driving wavelength dependent value of R
'''
#R_v = 3.23                                              #      R_V = A_v / E(B-V)
R_b = Ab_v*R_v                                          #      R_B = (A_b / A_v) * (A_v / E(B-V))
R_r = Ar_v*R_v                                          #      R_B = (A_b / A_v) * (A_v / E(B-V))
R_i = Ai_v*R_v                                          #          = (A_i / A_v) * (A_v / E(B-V))
R_j = Aj_v*R_v                                          #          = (A_j / A_v) * (A_v / E(B-V))
R_h = Ah_v*R_v                                          #          = (A_h / A_v) * (A_v / E(B-V))
R_k = Ak_v*R_v                                          #          = (A_k / A_v) * (A_v / E(B-V))

##########################################################
def select_data_file(k):
    if k==0:
        file_name = '59_madore.csv'
        file_cols = ['name','logP','HST','EBV','M_B','M_V','M_R','M_I','M_J','M_H','M_K'] 
        dis_list = ['HST']
        dis_flag = ['_h']
        A = [Ab_v, Av_v, Ar_v, Ai_v, Aj_v, Ah_v, Ak_v]
        R = [R_b, R_v, R_r, R_i, R_j, R_h, R_k]
        mag = ['B', 'V', 'R', 'I','J','H','K'];
        abs_bands = ['M_B', 'M_V', 'M_R', 'M_I', 'M_J', 'M_H', 'M_K']; 
    elif k ==1:
        file_name = 'cleaned_data.csv'
        file_cols = ['name',"logP", 'IRSB', 'EBV', "B_mag", 'V_mag', 'I_mag', 'J_mag', 'H_mag', 'K_mag']
        dis_list = ['plx', 'IRSB']
        dis_flag = ['_g','_i']
        A = [Ab_v, Av_v, Ai_v, Aj_v, Ah_v, Ak_v]
        R = [R_b, R_v, R_i, R_j, R_h, R_k]
        mag = ['B', 'V', 'I','J','H','K'];
        abs_bands = ['M_B', 'M_V', 'M_I', 'M_J', 'M_H', 'M_K']; 
    elif k == 2:
        file_name = '18_gaia_irsb_cluster.csv'
        file_cols = ['name',"logP", 'IRSB', 'EBV', "B_mag", 'V_mag', 'I_mag', 'J_mag', 'H_mag', 'K_mag']
        dis_list = ['cluster']
        dis_flag = ['_c']
        A = [Ab_v, Av_v, Ai_v, Aj_v, Ah_v, Ak_v]
        R = [R_b, R_v, R_i, R_j, R_h, R_k]
        mag = ['B', 'V', 'I','J','H','K'];
        abs_bands = ['M_B', 'M_V', 'M_I', 'M_J', 'M_H', 'M_K']; 
    return file_name, file_cols, dis_list, dis_flag, A, R, mag, abs_bands
#k = input('Dataset \n')
input_data_file, data_cols, dis_list, dis_flag, A, R, mag, abs_bands = select_data_file(k)
nreg = 5*len(dis_flag)
#####################################################################
data_dir = './data/input/'
data_out='./data/output/'
img_out_path = './data/output/9_plots/'
flags = ['_S', '_M']
process_step = ['1_prepared/','2_PLPW/','3_deldel/', '4_reddening/', '5_dispersion/','6_rms/','7_errorpair/', '8_result/', '9_plots/', '0_stars/']
#####################################################################
ap_bands = ['B_mag', 'V_mag' ,'I_mag', 'J_mag', 'H_mag', 'K_mag']
band = len(mag);
col_dot = ['b.', 'g*', 'y+', 'r*', 'c+', 'g.', 'y+', 'b+'] ;
col_lin = ['b-', 'g-', 'y-', 'r-', 'c-', 'g-', 'y-', 'b-'] ;
col_das = ['b--', 'g--', 'y--', 'r--', 'c--', 'g--', 'y--', 'b--']
col_ = ['b', 'g', 'y', 'r', 'c', 'g', 'y', 'b'] ;
#####################################################################
def output_directories(parent_folder = data_out, s=1,subdirectories = process_step):
    if s==1:
        for subdirectory in subdirectories:
            path = os.path.join(parent_folder, subdirectory)
            if not os.path.exists(path):
                os.makedirs(path)
#####################################################################       
def load_data(data_file = input_data_file, data_dir = data_dir, p=0):
    cleaned_data = pd.read_csv(data_dir+data_file)
    if p==1:
        print(' \n Data Loaded from: \t', data_dir+data_file)
        print( cleaned_data.info())
#    name = cleaned_data.ID
#    ra = cleaned_data.RA_ICRS
#    dec = cleaned_data.DE_ICRS
#    EBV = cleaned_data.EBV
#    dis = cleaned_data.IRSB
    return cleaned_data #, name, ra, dec, EBV, dis
#####################################################################
def save(title, img_path=img_out_path, step=0, fil = 'pdf'):                                   #   2
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
def RA_DEC_DIS_to_Galactocentric(ra, dec, dis):
    ra = Longitude(ra, unit=u.degree)
    dec = Latitude(dec, unit = u.degree)                        #   1
    dis = 10**(1 + dis/5)/1000          # modulus to kpc
    dis = Distance(dis, unit = u.kpc)
    coordinate = SkyCoord(ra=ra, dec=dec, distance=dis, frame='icrs')
    coordinate = coordinate.transform_to(Galactocentric(galcen_distance=8.1*u.kpc))
    return coordinate
#####################################################################

