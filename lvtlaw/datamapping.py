### File: ./data/datamapping.py
'''
0_datamapping.py tells to main.py which dataset should be used through parameter k = [0 ,1, 2]. A function select_data_file maps the metadata of input with defined variables. Another function provides Fouque extinction law.
'''
module = 'datamapping'
#####################################################################
k=5; 						# k selects dataset [0:Madore, 1:Jesper, 2:Cruz, 3:LMC, 4:SMC], see line 69
ex_law = '_s'               # S means Shubham's version, see line 24 onwards
standard_PL = 0             # 1 means PL imported, 0 means estimate PL from data, see line 37 onwards.
pivot = 1                   # pivot value chosen for PL relation.
del_fit = 0                 # 1 means del_del slopes are priory known. see line 46 onwards
del_mask = (-1, 1)      # Mask range for delta-delta plots. 
flags = ['S'] 			# Madore and Shubham method for distance-reddening correction
del_mu = [round(i*0.01,3) for i in range(-100,100,2)]
rd_avg_drop = ['Y', 'J', 'K']            # Not included in estimating reddening variance (f_star_wise)
mode = ['0']  			    # Absolute mag '' and True absolute mag '0' based PL and PW
#####################################################################
skip=0;                     # for code development purpose. see main.py
s=1; 						# 1 saves the output in data/processed/
z=0; 						# 1 switches output to paging mode in terminal
p=0;                        # print numerical data while processing
plots=0; 					# 1 genrates plots
plot_every_n_star = 15
#####################################################################
if ex_law == '_F': # Fouque
    extinction_ratios = {'B': 1.31, 'V': 1.0, 'R': 0.845,'I': 0.608,'J': 0.292,'H': 0.181,'K': 0.119 }   	
    Rv = 3.23		 
elif ex_law == '_S': # Shubham
    extinction_ratios = {'B': 1.31, 'V': 1.0, 'R': 0.845,'I': 0.608,'J': 0.2969,'H': 0.1805,'K': 0.1231 }   
    Rv = 3.19	
elif ex_law == '_l': # LMC
    extinction_ratios = {'B': 1.32,'V': 1.00, 'I': 0.65,'J': 0.30,'H': 0.20,'K': 0.15}   
    Rv = 3.4	
elif ex_law == '_s': # SMC #Wang & Chen 2023 
    extinction_ratios = {'B': 1.40,'V': 1.00, 'G': 0.95,'R': 0.90,'I': 0.70, 'Y': 0.6, 'J': 0.38,'H': 0.28,'K': 0.20}   
    Rv = 2.53	 
#####################################################################
def PL_madore17():
    slpMW = {'B': -2.277, 'V': -2.670,'R': -2.874,'I': -2.983,'J': -3.198,'H': -3.333,'K': -3.377}
    slperr = {'B': 0.121, 'V': 0.095,'R': 0.075,'I': 0.064,'J': 0.054,'H': 0.055,'K': 0.055}
    incMW = {'B': -3.214, 'V': -3.944,'R': -4.396,'I': -4.706,'J': -5.258,'H': -5.558,'K': -5.659}
    incerr = {'B': 0.036, 'V': 0.028,'R': 0.022,'I': 0.019,'J': 0.016,'H': 0.017,'K': 0.016}
    rmsMW = {'B': 0.27, 'V': 0.21,'R': 0.17,'I': 0.14,'J': 0.12,'H': 0.12,'K': 0.12}
    return slpMW, slperr, incMW, incerr, rmsMW
#####################################################################
def del_del():
    rho = {'B': 0.7, 'V': 0.8,'R': 0.86,'I': 0.91,'J': 0.94,'H': 0.97,'K': 0.99}
    return rho
#####################################################################
def R_ratio(R_v, mag, A):
    R = {}
    for m in mag:
        R[m] = round(A[m]*R_v, 4)
    R_dic = {}
    for m in mag:
        for c1 in range(0,len(mag)):
            for c2 in range(c1+1,len(mag)):
                R_dic[m+mag[c1]+mag[c2]] = round(R[m] / (round(R[mag[c1]],4) - round(R[mag[c2]],4)),4)
    return R, R_v, A, R_dic
#####################################################################
def R123(m:str,c1:str,c2:str,R):
    # calculate composite reddening ratio for wesenheit functions
    R123 = round(R[m] / (round(R[c1],4) - round(R[c2],4)),4)
    return R123
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
        dis_list = ['HST']; dis_flag = ['_h']
        mag = ['B','V','R','I','J','H','K'];
        wes_show=colors(mag)
        R, R_v, A, R_dic = R_ratio(R_v = Rv, mag = mag, A = extinction_ratios)
        file_cols = ['name','logP','EBV'] + dis_list + [f'M_{m}' for m in mag] 
    elif k ==1:
        filename = '121_Cepheids'
        dis_list = ['mMplx']; dis_flag = ['_g']; dis_label = ['Gaia']
        mag = ['B','V','I', 'J', 'H','K'];#
        wes_show=colors(mag)#['VI', 'BJ', 'BH', 'BK', 'VJ', 'VH', 'VK', 'IH', 'IK']
        R, R_v, A, R_dic = R_ratio(R_v = Rv, mag = mag, A = extinction_ratios)
        file_cols = ['name','logP','EBV'] + dis_list + [f'{m}_mag' for m in mag]
    elif k == 2:
        filename = '20_cluster_cruz'
        wes_show=['VK']#['BJ', 'BH', 'BK', 'VJ', 'IJ','IH', 'IK', 'JH', 'JK' ]
        dis_list = ['cplx']
        dis_flag = ['_c']; dis_label = ['Cruz']
        mag = ['B', 'V', 'I','J','H','K'];
        R, R_v, A, R_dic = R_ratio(R_v = Rv, mag = mag, A = extinction_ratios)
        file_cols = ['name','logP','EBV'] + dis_list + [f'{m}_mag' for m in mag]
    elif k == 3:
        filename = '29_LMC'
        wes_show=['VI','VJ','VK','IJ','IK', 'JK']
        dis_list = ['IRSB']
        dis_flag = ['_l']
        mag = ['V', 'I','J', 'K'] 
        R, R_v, A, R_dic = R_ratio(R_v = Rv, mag = mag, A = extinction_ratios) #± 0.06
        file_cols = ['name','logP','EBV'] + dis_list + [f'{m}_mag' for m in mag]
    elif k ==4:
        filename = '2486_SMC'
        dis_list = ['mMecb']; dis_flag = ['_g']; dis_label = ['SMC']
        mag = ['V','I', 'J', 'K'];#
        wes_show=colors(mag)#['VI', 'VJ', 'VK', 'IK']
        R, R_v, A, R_dic = R_ratio(R_v = Rv, mag = mag, A = extinction_ratios)
        file_cols = ['name','logP','EBV', 'RA', 'DEC'] + dis_list + [f'{m}_mag' for m in mag]
    elif k ==5:
        filename = '2574_SMC'
        dis_list = ['mMecb']; dis_flag = ['_g']; dis_label = ['SMC']
        mag = ['B','V','G','R','I','Y','J','K'];#
        wes_show=colors(mag)#['VI', 'VJ', 'VK', 'IK']
        R, R_v, A, R_dic = R_ratio(R_v = Rv, mag = mag, A = extinction_ratios)
        file_cols = ['name','logP','EBV', 'RA', 'DEC'] + dis_list + [f'{m}_mag' for m in mag]
    return filename, file_cols, dis_list, dis_flag, dis_label, R, A, R_dic, mag, R_v, wes_show
#####################################################################
file_name, data_cols, dis_list, dis_flag, dis_label, R, A, R_dic, mag, R_v, wes_show = select_data_file(k)
#####################################################################
nreg = 5*len(dis_flag)
data_dir = './data/input/'                     # save data.csv file in this directory
disfl = ''.join(dis_flag)
data_out=f'./data/processed/{file_name}{disfl}_{R_v}{ex_law}/'
img_out_path=f'./docs/processed/{file_name}{disfl}_{R_v}{ex_law}/9_plots/'
table_out_path='./docs/reports/thesis_version/chapters/content/'
process_step = ['1_prepared/','2_PLPW/','3_deldel/', '4_reddening/', '5_dispersion/','6_rms/','7_errorpair/', '8_result/', '9_plots/', '0_stars/']
image_step = ['1_datacleaning/','2_PLPW/','3_deldel/','4_reddening/','5_dispersion/','6_rms/','7_errorpair/', '8_result/', '9_compare/']
#####################################################################
col_dot = ['b.', 'm*', 'y+', 'c*', 'g+', 'k.', 'c+', 'r+'] ;
col_lin = ['b-', 'm-', 'y-', 'c-', 'g-', 'k-', 'c-', 'r-'] ;
col_das = ['b--', 'm--', 'y--', 'c--', 'g--', 'k--', 'c--', 'r--']
col_ = ['b', 'm', 'y', 'c', 'g', 'k', 'c', 'r'] ;
#####################################################################
print(f'* * {module} module loaded!')
