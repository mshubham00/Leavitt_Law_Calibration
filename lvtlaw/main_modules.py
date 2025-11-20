 # File: ./leavitt_law/main_modules.py
module = 'main_modules'
####################################################################
import pandas as pd
from data.datamapping import plots,s,file_name,mag,z, wes_show, data_out, k, del_mu, flags, dis_flag, R_v, R,fouque_extinction_ratios
from lvtlaw.a_utils import output_directories, image_directories, load_data 
from lvtlaw.b_data_transform import transformation, plot_corr
from lvtlaw.c_pl_pw import pl_reg, plotPL6, plotPW6     
from lvtlaw.d_del_del import residue_analysis
from lvtlaw.e_error_estimation import error_reddening #star_by_star, star_dispersion, result
from lvtlaw.f_star_wise import star_ex_rd_mu, star_frame, correction_rd_mu, plot_star_rd_mu
from lvtlaw.g_result import correction_apply, corrected_PL, corrected_reg
####################################################################
def intro(data_out=data_out, k=k, s=s, z=z):
    output_directories(); 
    image_directories(); 
    bar = '_'
    star = '* '
    Rv = R_v
    print(f"{star*20}\n{star*20}\n\n\nMaster Thesis Project: \tGalactic BVIJHK Leavitt Law Calibration for R_v = {Rv} \n\n  \t\t\tTo Refine systematic errors in luminosity, distance and reddening of individual Cepheid. \n\t\t\t{bar*54}\n\n     \t\t\tAuthor: Shubham Mamgain (mshubham00@gmail.com) \n     \t\t\tSupervisor I: Dr. Jesper Storm (AIP Potsdam)\n     \t\t\tSupervisor II: Prof. Dr. Maria Rosa Cioni")    
    print('\n\n\n\n\t\t\tTo begin the calibration process, store cleaned data at ./data/input/<file_name>.csv \n\n\t\t\tFor datafile selection (k) and columns mapping, edit ./data/datamapping.py file.')
    print(f'\n\t\t\tAutosave (s = {s}) | Paging (z = {z}) | Generate Plots (plots = {plots})\n\n\t\t\tk : {k}\n\t\t\tdata : {file_name}\n\t\t\tR_v : {Rv}\n\n\t\t\tProcessed data will be saved in {data_out} directory. \n\n'+'###'*30)
    if z==1:
        input('\nPress Enter to proceed \n')

# Load data and select relevant coloumns
input_data, raw, mag, dis = load_data(file_name) # a_utils

#####################################################################################################
# b_data_transform -> [0] output folder
def mag_transformation(cleaned_data = raw, A = fouque_extinction_ratios, R = R, plots=plots,s=s,file_name=file_name):
    if plots == 1:
        df = cleaned_data.drop(columns = ['name'])
        print(file_name)
        plot_corr(df , Y = 'logP', title = file_name, f=12)
    print(A)
    print(cleaned_data.head())
    data, abs_data, ext_data, tabs_data, wes_data, merged_data = transformation(cleaned_data,A, R)
    print('mag_transformation module ended!')
    return data, abs_data, ext_data, tabs_data, wes_data, merged_data
#####################################################################################################
# c_pl_pw -> [1]
def PLWcorrection(merged_data, plots=plots, s=s, z=z):
    PLW, residue, prediction, merged_data = pl_reg(merged_data)
    if z==1:
        input('###'*30+'\n')
    print('\n Slope, Intercept and respective error for PL and PW relations: \n')
    print(PLW.head())
    print('\n Dataframe containing residues of PL relations and associated PW relation: \n')
    print(residue.head())
    print('Raw PL and PW relations derived. \n', len(mag),'Photometry bands: \t \t \t ', mag, '\n %i versions of composite wesenheits: \t '%(len(wes_show)), wes_show,'\n \nTotal: \t \t \t \t \t', len(mag), '(PL relations) +',len(mag),'x' ,len(wes_show),' (PW relations) \n \t \t \t \t \t = ',len(mag) + len(mag)*len(wes_show),' versions of Galactic Leavitt Law.' )
    if plots == 1:
        plotPL6(merged_data, PLW, '0')
        for col in wes_show:
            plotPW6(merged_data, PLW, col)
    if z==1:
        input('###'*30+'\n')
    print('PLWcorrection module ended!')
    return PLW, residue, prediction, merged_data
#####################################################################################################
# d_del_del  -> [2]
def residual_correlation(merged_data, plots=plots, s=s, z=z):
    print('Starting residual correlation \n')
    print('PW residuals correlated with PL residuals with two approaches. \n i) Madore : (m vs. VVI) \n ii) Shubham: (m vs mVI) \n') 
    dres, dpre, dmc, merged_data = residue_analysis(merged_data, plots)
    print('Slope, Intercept and respective errors.')
    print('###'*30)
    print(dmc.head())
    print('###'*30)
    print('\n Delta residue \n', dres.head())
    print('###'*30)
    if z==1:
        input('###'*30+'\n')    
    print('residual_correlation module ended!')
    return dmc, dres, dpre, merged_data
####################################################################################################
# e_error_estimation  -> [3,4]
def rd_mu_error_matrix(merged_data, dmc, del_mu=del_mu, z=z,plots=plots,):
    print(' \n Begin to decouple distance-reddening errors.')
    print('###'*30+'\nModulus error affect reddening as following. \n')
    print(' \t \t dE(mu) = dE(0) + mu*(1-rho)/R \n\twhere rho is the slope from residual correlation, \n\t dE(0) represents reddening error from above matrix, \n\tReddening ratio, R = Rx/(Rb - Rv)')
    print('\n \tmu contains 100 possibilities of modulus correction in between %f and %f'%(del_mu[0], del_mu[-1]))
    ex0_df, rd0_df, mu_df_list_dict = error_reddening(merged_data, dmc, plots=plots)
    print('Reddening error without considering distance modulus error. \n',rd0_df)
    if z==1:
        input('###'*30+'\n')
    print('rd_mu_error_matrix module ended!')
    return ex0_df, rd0_df, mu_df_list_dict, merged_data
####################################################################################################
# f_star_wise  -> [5, 9]
def starwise_analysis(merged_data, mu_df_list_dict, plots=plots, s=s, z=z):
    star_frame_list = star_frame(merged_data)
    print('\n Reddening error for introduced modulus error \n')
    stars_rd_mu_list =  star_ex_rd_mu(mu_df_list_dict, merged_data)
    correction_rd_mu_stars = correction_rd_mu(stars_rd_mu_list, merged_data, plots)
    print('starwise_analysis module ended!')
    return star_frame_list, stars_rd_mu_list, correction_rd_mu_stars, merged_data
####################################################################################################
#g_result -> [7]
def calibrated_result(merged_data,correction_rd_mu_stars, plots = plots, flags=flags, dis_flag=dis_flag, s=s, z=z):
#    print('\n Variance-Modulus-Reddening estimated for different composite wesenheits. \n' ,correction_rd_mu_stars.head())
    if z==1:
        input('###'*30+'\n')
    corrected = correction_apply(merged_data, correction_rd_mu_stars)
#    print('Calibrated data: \n', corrected.head(-1))
    reg, res, pre, merged_data = corrected_reg(merged_data, corrected, dis_flag[0], plots)
    print('calibrated_result module ended!')   
    return corrected, merged_data
'''
from lvtlaw.visualization import milky_way, plot_corr, cordinate
milky_way(ra,dec, dis_flag[0], '%i_Galactic_Cepheids'%(n))
plot_corr(df, 'logP', title = input_data_file, f=18)
from lvtlaw.star_analysis import ex_rd_error
choice = input('Press spacebar and enter for project visualization.')
if choice == ' ':
    cordinate(name, ra, dec, EBV, dis)
'''
print(f'* * {module} module loaded!')
