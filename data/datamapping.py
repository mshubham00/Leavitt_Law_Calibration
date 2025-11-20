### File: ./data/datamapping.py
'''
0_datamapping.py tells to main.py which dataset should be used through parameter k = [0 ,1, 2]. A function select_data_file maps the metadata of input with defined variables. Another function provides Fouque extinction law.
'''
module = 'datamapping'
#####################################################################
k=1; 						# k selects dataset [0:Madore, 1:Jesper, 2:Cruz, 3:LMC, 4:SMC]
skip=0
s=1 ; 						# saves the output
z=0; 						# z switches output to paging mode
p=0
plots=0; 					# plots for genrating plots
flags = ['S'] 				# Madore and Shubham
mode = ['0']  			    # Absolute mag and True absolute mag for PL and PW
rd_avg_drop = ['H','K']# Not included in estimating reddening variance (f_star_wise)
del_mu = [round(i*0.01,3) for i in range(-100,100,2)]
plot_every_n_star = 15
#####################################################################
#fouque_extinction_ratios = {'B': 1.31, 'V': 1.0, 'R': 0.845,'I': 0.608,'J': 0.292,'H': 0.181,'K': 0.119 }   			 
fouque_extinction_ratios = {'B': 1.2574, 'V': 1.0, 'R': 0.845,'I': 0.609,'J': 0.2969,'H': 0.1816,'K': 0.1231 }   	
LMC_extinction_ratios = {'B': 1.32,'V': 1.00, 'I': 0.65,'J': 0.30,'H': 0.20,'K': 0.15} #Wang & Chen 2023
SMC_extinction_ratios = {'B': 1.40,'V': 1.00,'R': 0.90,'I': 0.70,'J': 0.38,'H': 0.28,'K': 0.20}

#####################################################################
def R_ratio(R_v, mag, A):
	# Wavelength dependent value of ratio of total to selective absorption
    R = {}
    for m in mag:
        R[m] = A[m]*R_v
    return R, R_v, A

#####################################################################
def colors(mag):
    color_index = []
    for i in range(0,len(mag)):
        for j in range(i+1,len(mag)):
            color_index.append(mag[i]+mag[j])
    return color_index
#####################################################################
def select_data_file(k):
    if k==0:
        filename = '59_madore'
        dis_list = ['HST']
        dis_flag = ['_h']
        mag = ['B','V','R', 'I','J','H','K'];
        wes_show=colors(mag)#['VI']#['BJ', 'BH', 'BK', 'VI', 'VJ', 'VH', 'VK', 'RJ', 'RH' ]
        R, R_v, A = R_ratio(R_v = 3.23, mag = mag, A = fouque_extinction_ratios)
        file_cols = ['name','logP','EBV'] + dis_list + [f'M_{m}' for m in mag] 
    elif k ==1:
        filename = '109_IRSB_plx_IH'
#        filename = '71_IRSB_plx_IK'
        dis_list = ['plx']; dis_flag = ['_p']
#        filename = '76_IRSB_IJ_HK'
#        filename = '109_IRSB_IH_VJ'
#        dis_list = ['IRSB']; dis_flag = ['_j']
        mag = ['B','V','I','J','H','K'];#
        wes_show=colors(mag)#['VI', 'BJ', 'BH', 'BK', 'VJ', 'VH', 'VK', 'IH', 'IK']
        R, R_v, A = R_ratio(R_v = 3.23, mag = mag, A = fouque_extinction_ratios)
        file_cols = ['name','logP','EBV'] + dis_list + [f'{m}_mag' for m in mag]
    elif k == 2:
        filename = '20_cluster_cruz'
        wes_show=['VI']#['BJ', 'BH', 'BK', 'VJ', 'IJ','IH', 'IK', 'JH', 'JK' ]
        dis_list = ['mplx']
        dis_flag = ['_c']
        mag = ['B', 'V', 'I','J','H','K'];
        R, R_v, A = R_ratio(R_v = 3.23, mag = mag, A = fouque_extinction_ratios)
        file_cols = ['name','logP','EBV'] + dis_list + [f'{m}_mag' for m in mag]
    elif k == 3:
        filename = '29_LMC'
        wes_show=['VI','VJ','VK','IJ','IK', 'JK']
        dis_list = ['IRSB']
        dis_flag = ['_l']
        mag = ['V', 'I','J', 'K'] 
        R, R_v, A = R_ratio(R_v = 3.4, mag = mag, A = LMC_extinction_ratios) #± 0.06
        file_cols = ['name','logP','EBV'] + dis_list + [f'{m}_mag' for m in mag]
    elif k == 4:
        filename = '32_SMC_VIJK'
        wes_show=['VI','VJ','VK','IJ','IK', 'JK']
        dis_list = ['IRSB']
        dis_flag = ['_s']
        mag = ['V', 'I','J', 'K']
        R, R_v, A = R_ratio(R_v = 2.53, mag = mag, A = SMC_extinction_ratios) #± 0.13
        file_cols = ['name','logP','EBV'] + dis_list + [f'{m}_mag' for m in mag]
    return filename, file_cols, dis_list, dis_flag, R, A, mag, R_v, wes_show
#####################################################################
file_name, data_cols, dis_list, dis_flag, R, A, mag, R_v, wes_show = select_data_file(k)
#####################################################################
nreg = 5*len(dis_flag)
data_dir = './data/input/'
data_out=f'./data/processed/{file_name}{dis_flag[0]}_{R_v}/'
img_out_path='./docs/reports/plots/'
#img_out_path = data_out + '9_plots/'
process_step = ['1_prepared/','2_PLPW/','3_deldel/', '4_reddening/', '5_dispersion/','6_rms/','7_errorpair/', '8_result/', '9_plots/', '0_stars/']
image_step = ['1_datacleaning/','2_PLPW/','3_deldel/','4_reddening/','5_dispersion/','6_rms/','7_errorpair/', '8_result/', '9_compare/']
#####################################################################
def R123(m:str,c1:str,c2:str,R=R):
    # calculate composite reddening ratio for wesenheit functions
    R123 = round(R[m] / (round(R[c1],3) - round(R[c2],3)),3)
    return R123
#####################################################################    
def R_dic(mag=mag):
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
