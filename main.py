### File: ./main.py
import os, sys, pandas as pd ; clear_screen= lambda: os.system('clear'); clear_screen()

print('Master Thesis Project: Galactic BVIJHK Leavitt Law Calibration \n     Refining systematic errors in luminosity, distance and reddening for individual Cepheid \n     Author: Shubham Mamgain (mshubham00@gmail.com) \n     Supervisor I: Dr. Jesper Storm (AIP Potsdam)\n     Supervisor II: Prof. Dr. Maria Rosa Cioni \n To start the analysis, store the datafile file in ./data/input/ directory. \n Selection of datafile (k) and columns mapping must be done by editing ./lvtlaw/utils.py file. \n Processed data will be saved in ./data/output directory. \n'+'###'*30+'\nPress Enter to proceed')
#####################################################################################################


from lvtlaw.a_utils import output_directories, load_data, process_step, open_output_dir, data_cols, z
from lvtlaw.a_utils import data_dir, input_data_file, data_out, mag, colors, wes_cols, wes_show, dis_list, dis_flag, del_mu, s, k
output_directories(data_out, s)
cleaned_data = load_data(input_data_file)

df = cleaned_data[data_cols].dropna().reset_index(drop=True)
n = len(df)  # total number of cepheids
if z==1:
    input('###'*30+'\n')

print(n,' Galactic Cepheids loaded. (k = %i)\n'%(k), df.head(-1),'\n')
'''
from lvtlaw.visualization import milky_way, plot_corr, cordinate
milky_way(ra,dec, dis_flag[0], '%i_Galactic_Cepheids'%(n))
plot_corr(df, 'logP', title = input_data_file, f=18)
from lvtlaw.star_analysis import ex_rd_error
choice = input('Press spacebar and enter for project visualization.')
if choice == ' ':
    cordinate(name, ra, dec, EBV, dis)
'''
print('\nRaw data transformed into absolute magnitude and weseheit magnitude using the Galactic extinction law, Reddenings (EBV) and Distance modulus (mu).\n M  = m - mu \n M0 = m - mu - R*EBV \n W  = m - mu - R*(m1-m2) \n')
#####################################################################################################


from lvtlaw.b_data_transform import transformation, extinction_law
A, R = extinction_law() # converts Fouque (2007) extinction law into corresponding reddening ration
print(' \n Reddening ratio values will be multiplied with E(B-V) values to calculate extinction in each band for individual Cepheid toward the respective line-of-sight.  \n')
if z==1:
    input('###'*30+'\n')
star_names=df['name']
absolute, extinction, tabsolute, wesenheit = transformation(df, s)
merg1= pd.merge(absolute, tabsolute, on="logP")
prepared_regression_data = pd.merge(merg1, wesenheit, on = 'logP')
#prepared_regression_data['name'] = star_names 
prepared_regression_data.to_csv(data_out+process_step[1]+str(len(prepared_regression_data))+ '_prepared_PLdata'+'.csv')
#####################################################################################################


from lvtlaw.f_star_wise import star_frame, add_res, add_dres, star_ex_red_mu
star_frame_list = star_frame(prepared_regression_data)
print('Following raw PL, true PL and PW relations will be calculated. \n', len(mag),'Photometry bands: \t \t \t ', mag, '\n %i versions of composite weneheits: \t '%(len(wes_show)), wes_show,'\n Total: \t \t \t \t', len(mag), '(PL relations) +',len(mag),'x' ,len(wes_show),' (PW relations) \n \t \t \t \t \t= ',len(mag) + len(mag)*len(wes_show),' versions of Galactic Leavitt Law.' )
if z==1:
    input('Press enter to deduce the raw Leavitt Laws')
#####################################################################################################


from lvtlaw.c_pl_pw import pl_reg     
PLW, residue, prediction= pl_reg(prepared_regression_data, s)
if z==1:
    input('###'*30+'\n')
print('\n Slope, Intercept and respective error for PL and PW relations: \n')
print(PLW.head())
print('\n Dataframe containing residues of PL relations and associated PW relation: \n')
print(residue.head())
print('\n PL residuals are sensitive to modulus and E(B-V) errors.\n PW residuals sensitive to modulus only. \n'+'###'*30)
star_frame_list = add_res(star_frame_list, residue)
print('Start the residual correlation \n')
print('PW residuals correlated with PL residuals with two approaches. \n i) Madore : (m vs. VVI) \n ii) Shubham: (m vs mVI) \n') 
if z==1:
    input('###'*30+'\n')
#####################################################################################################


from lvtlaw.d_del_del import residue_analysis
dres, dpre, dmc = residue_analysis(residue, dis_flag, wes_show, s)
print(dres)
star_frame_list = add_dres(star_frame_list, dres)
print('Slope, Intercept and respective errors.')
print('###'*30)
print(dmc.head())
print('###'*30)
print('\n Delta residue \n', dres.head())
star_frame_list = add_dres(star_frame_list, dres)
print('###'*30)
print(' \n start decoupling distance-reddening errors.')
if z==1:
    input('###'*30+'\n')
dSM = [[dmc],[dres]]
####################################################################################################


from lvtlaw.e_error_estimation import reddening_error#star_by_star, star_dispersion, result
#from visuals.dataload import dSM#, pick_star
red0_SM, ex_rd_mu = reddening_error(wes_show, dis_flag, dSM, s)
print('###'*30+'\n Above represents reddening error without considering modulus error. Modulus error affect reddening using following equation. \n')
print(' \t \t dE(mu) = dE(0) + mu*(1-s)/R \t | where s is the slope from residual correlation.')
print('\n mu implies 100 possibilities of modulus correction in between %f and %f'%(del_mu[0], del_mu[-1]))
print('\n Resolve modulus error for each Cepheid \n')
if z==1:
    input('###'*30+'\n')
stars_ex_red_mu_list =  star_ex_red_mu(n,ex_rd_mu, df)
if z==1:
    input('###'*30+'\n')
'''
print('loading stars')
from visuals.dataload import pick_star
stars_ex_red_mu_list=[]
for i in range(n):
    _,ex_red_mu = pick_star(i)
    stars_ex_red_mu_list.append(ex_red_mu)
print('loaded')
'''
####################################################################################################


from lvtlaw.g_result import correction_rd_mu, correction_apply, corrected_PL, corrected_reg
correction_red_mu_stars = correction_rd_mu(stars_ex_red_mu_list, save=1)
print('\n Modulus-Reddening error pair estimated using different composite wesenheit magnitudes \n' ,correction_red_mu_stars.head())
if z==1:
    input('###'*30+'\n')
corrected = correction_apply(tabsolute, correction_red_mu_stars, save=1)
print(corrected.head(-1))
corrected_reg(tabsolute, corrected, dis_flag, s=1)
'''
from visuals.dataload import tabsolute, correction, wesenheit
import matplotlib.pyplot as plt
correction_red_mu_stars =  correction()
print(tabsolute, correction_red_mu_stars)

flag = '_M'
col = 'JK'
for i in range(6):
    plt.plot(tabsolute['logP'], tabsolute['M_'+mag[i]+'0_g'], 'k--')
    plt.plot(tabsolute['logP'], tabsolute['M_'+mag[i]+'0_g']+correction_red_mu_stars['mu_g'+col+flag]+ correction_red_mu_stars['rd_g'+col+flag]*R[i])
    plt.show()
'''
#star_frame_list = add_dres(star_frame_list, dres_S, dres_M)
print('All the processed data is saved in ./data/output/ directory.')
#input('Enter to open the output folder!!')
#open_output_dir(data_out)

