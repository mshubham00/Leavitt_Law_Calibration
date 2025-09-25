### File: ./data/datamapping.py
'''
0_datamapping.py tells to main.py which dataset should be used through parameter k = [0 ,1, 2]. A function select_data_file maps the metadata of input with defined variables. Another function provides Fouque extinction law.
'''
module = 'datamapping'
#####################################################################
k=3; 						# k selects dataset [0:Madore, 1:Jesper, 2:Cruz, 3:LMC, 4:SMC]
skip=0
s=1 ; 						# saves the output
z=0; 						# z switches output to paging mode
plots=0; 					# plots for genrating plots
flags = ['S'] 				# Madore and Shubham
mode = ['0']  			# Absolute mag and True absolute mag for PL and PW
rd_avg_drop = [] 	# Not included in estimating reddening variance (f_star_wise)
del_mu = [round(i*0.01,2) for i in range(-300,300,2)]
plot_every_n_star = 10

#####################################################################
extinction_ratios = {'B': 1.31, 'V': 1.0, 'R': 0.845,'I': 0.608,'J': 0.292,'H': 0.181,'K': 0.119 }   			 
#####################################################################
def select_data_file(k):
    if k==0:
        filename = '59_madore'
        dis_list = ['HST']
        dis_flag = ['_h']
        mag = ['B','V','R', 'I','J','H','K'];
        wes_show=['BJ', 'BH', 'BK', 'VI', 'VJ', 'VH', 'VK', 'RJ', 'RH' ]
        R, R_v = R_(R_v = 3.23, mag = mag)
        file_cols = ['name','logP','EBV'] + dis_list + [f'M_{m}' for m in mag]
    elif k ==1:
        filename = '95_jesper'
        wes_show=['BJ', 'BH', 'BK', 'VJ', 'VH', 'VK', 'IH', 'IK']
        dis_list = ['plx']
        dis_flag = ['_g']
        mag = ['B', 'V', 'I','J','H','K'];
        R, R_v = R_(R_v = 3.23, mag = mag)
        file_cols = ['name','logP','EBV'] + dis_list + [f'{m}_mag' for m in mag]
    elif k == 2:
        filename = '20_cluster_cruz'
        wes_show=['BJ', 'BH', 'BK', 'VJ', 'IJ','IH', 'IK', 'JH', 'JK' ]
        dis_list = ['mplx']
        dis_flag = ['_p']
        mag = ['B', 'V', 'I','J','H','K'];
        R, R_v = R_(R_v = 3.23, mag = mag)
        file_cols = ['name','logP','EBV'] + dis_list + [f'{m}_mag' for m in mag]
    elif k == 3:
        filename = '29_LMC'
        wes_show=['VI','VJ','VK','IJ','IK', 'JK']
        dis_list = ['IRSB']
        dis_flag = ['_l']
        mag = ['V', 'I','J', 'K'] 
        R, R_v = R_(R_v = 3.41, mag = mag) #± 0.06
        file_cols = ['name','logP','EBV'] + dis_list + [f'{m}_mag' for m in mag]
    elif k == 4:
        filename = '32_SMC_VIJK'
        wes_show=['VI', 'VJ','IJ','IK']
        dis_list = ['IRSB']
        dis_flag = ['_s']
        mag = ['V', 'I','J', 'K']
        R, R_v = R_(R_v = 2.74, mag = mag) #± 0.13
        file_cols = ['name','logP','EBV'] + dis_list + [f'{m}_mag' for m in mag]
    return filename, file_cols, dis_list, dis_flag, R, mag, R_v, wes_show
#####################################################################
def R_(R_v, mag, extinction_ratios=extinction_ratios):
	# Wavelength dependent value of ratio of total to selective absorption
    r = {}
    for m in mag:
        r[m] = extinction_ratios[m]*R_v
    return r, R_v
#####################################################################
def colors(mag):
    color_index = []
    for i in range(0,len(mag)):
        for j in range(i+1,len(mag)):
            color_index.append(mag[i]+mag[j])
    return color_index
#####################################################################
file_name, data_cols, dis_list, dis_flag, R, mag, R_v, wes_show = select_data_file(k)
#wes_show = colors(mag)
#####################################################################
nreg = 5*len(dis_flag)
data_dir = './data/input/'
data_out=f'./data/{file_name}_{R_v}/'
img_out_path = data_out + '9_plots/'
process_step = ['1_prepared/','2_PLPW/','3_deldel/', '4_reddening/', '5_dispersion/','6_rms/','7_errorpair/', '8_result/', '9_plots/', '0_stars/']
image_step = ['1_datacleaning/','2_PLPW/','3_deldel/', '4_reddening/', '5_dispersion/','6_rms/','7_errorpair/', '8_result/']

#####################################################################
def R123(m:str,c1:str,c2:str,R=R):
    # calculate composite reddening ratio for wesenheit functions
    R123 = R[m] / (R[c1] - R[c2])
    return R123
#####################################################################    
def R_(mag=mag):
    R_ = {}
    for c,m in enumerate(mag):
        for a,c1 in enumerate(mag):
            for b,c2 in enumerate(mag[a+1:]):
                R_[m+c1+c2] = R123(m,c1,c2)
    return R_
#####################################################################
col_dot = ['b.', 'g*', 'y+', 'c*', 'g+', 'k.', 'c+', 'r+'] ;
col_lin = ['b-', 'g-', 'y-', 'c-', 'g-', 'k-', 'c-', 'r-'] ;
col_das = ['b--', 'g--', 'y--', 'c--', 'g--', 'k--', 'c--', 'r--']
col_ = ['b', 'g', 'y', 'c', 'g', 'k', 'c', 'r'] ;
#####################################################################
print(f'* * {module} module loaded!')
