 # File: ./leavitt_law/main_modules.py
####################################################################
def intro(data_out, z):
    print('Master Thesis Project: Galactic BVIJHK Leavitt Law Calibration \n     Refining systematic errors in luminosity, distance and reddening for individual Cepheid \n     Author: Shubham Mamgain (mshubham00@gmail.com) \n     Supervisor I: Dr. Jesper Storm (AIP Potsdam)\n     Supervisor II: Prof. Dr. Maria Rosa Cioni \n To start the analysis, store the datafile file in ./data/input/ directory. \n Selection of datafile (k) and columns mapping must be done by editing ./lvtlaw/utils.py file.')
    print(f'Processed data will be saved in {data_out} directory. \n'+'###'*30)
    if z==1:
        print('\nPress Enter to proceed \n \n')
#####################################################################################################
def data_loaded(file_name, R, k, df):
    print(file_name,' Galactic Cepheids loaded with R_v = %f. (k = %i)\n'%(R[1], k), df.head(-1),'\n')
#####################################################################################################
'''
from lvtlaw.visualization import milky_way, plot_corr, cordinate
milky_way(ra,dec, dis_flag[0], '%i_Galactic_Cepheids'%(n))
plot_corr(df, 'logP', title = input_data_file, f=18)
from lvtlaw.star_analysis import ex_rd_error
choice = input('Press spacebar and enter for project visualization.')
if choice == ' ':
    cordinate(name, ra, dec, EBV, dis)
'''
#####################################################################################################
from lvtlaw.b_data_transform import transformation, extinction_law
def trans(mag, A, R, cleaned_data, dis_flag, dis_list, k, s, z):
    print('\nRaw data transformed into absolute magnitude and weseheit magnitude using the Galactic extinction law, Reddenings (EBV) and Distance modulus (mu).\n M  = m - mu \n M0 = m - mu - R*EBV \n W  = m - mu - R*(m1-m2) \n')
    A, R = extinction_law(mag = mag, A = A, R = R) # converts Fouque (2007) extinction law into corresponding reddening ration
    print(' \n Reddening ratio values will be multiplied with E(B-V) values to calculate extinction in each band for individual Cepheid toward the respective line-of-sight.  \n')
    print(R, '\n',A)
    if z==1:
        input('###'*30+'\n')
    raw, absolute, extinction, tabsolute, wesenheit, prepared_regression_data = transformation(data=cleaned_data, R=R, mag=mag, dis_flag=dis_flag, dis_list=dis_list, k=k, s=s)
    return raw, absolute, extinction, tabsolute, wesenheit, prepared_regression_data
#####################################################################################################
from lvtlaw.f_star_wise import star_frame
def star_list(prepared_regression_data, mag, wes_show, z):
    star_frame_list = star_frame(prepared_regression_data)
    print('Following raw PL, true PL and PW relations will be calculated. \n', len(mag),'Photometry bands: \t \t \t ', mag, '\n %i versions of composite weneheits: \t '%(len(wes_show)), wes_show,'\n Total: \t \t \t \t', len(mag), '(PL relations) +',len(mag),'x' ,len(wes_show),' (PW relations) \n \t \t \t \t \t= ',len(mag) + len(mag)*len(wes_show),' versions of Galactic Leavitt Law.' )
    if z==1:
        input('Press enter to deduce the raw Leavitt Laws')
    return star_frame_list
#####################################################################################################
from lvtlaw.c_pl_pw import pl_reg     
from lvtlaw.f_star_wise import add_res
def regress(prepared_regression_data, star_frame_list, s, z):
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
    return PLW, residue, prediction, star_frame_list
####################################################################################################
from lvtlaw.d_del_del import residue_analysis
from lvtlaw.f_star_wise import add_dres
def res_analysis(residue, dis_flag, wes_show, flags, star_frame_list, s,z):
    dres, dpre, dmc = residue_analysis(residue, dis_flag, wes_show, flags, s)
    print(dres)
    print('Slope, Intercept and respective errors.')
    print('###'*30)
    print(dmc.head())
    print('###'*30)
    print('\n Delta residue \n', dres.head())
    star_frame_list = add_dres(star_frame_list, dres, flags, dis_flag[0])
    print('###'*30)
    print(' \n Start decoupling distance-reddening errors.')
    if z==1:
        input('###'*30+'\n')
    dSM = [dmc,dres, dpre]
    return dres, dpre, dmc, star_frame_list, dSM
####################################################################################################
from lvtlaw.e_error_estimation import reddening_error #star_by_star, star_dispersion, result
from lvtlaw.f_star_wise import star_ex_red_mu
def redd_err(df, wes_show, dis_flag, dSM, flags, del_mu,s,z):
    n = len(df)
    red0_df_list, mu_df_list_dict = reddening_error(wes_show, dis_flag, dSM, flags, s)
    print('###'*30+'\n Above represents reddening error without considering modulus error. Modulus error affect reddening using following equation. \n')
    print(' \t \t dE(mu) = dE(0) + mu*(1-s)/R \t | where s is the slope from residual correlation.')
    print('\n mu implies 100 possibilities of modulus correction in between %f and %f'%(del_mu[0], del_mu[-1]))
    print('\n Resolve modulus error for each Cepheid \n')
    if z==1:
        input('###'*30+'\n')
    stars_ex_red_mu_list =  star_ex_red_mu(n,mu_df_list_dict, df, flags, dis_flag)
    if z==1:
        input('###'*30+'\n')
    return red0_df_list, mu_df_list_dict, stars_ex_red_mu_list
####################################################################################################
from lvtlaw.g_result import correction_rd_mu, correction_apply, corrected_PL, corrected_reg
def correction(stars_ex_red_mu_list, tabsolute, flags, dis_flag, s, z):
    correction_red_mu_stars = correction_rd_mu(stars_ex_red_mu_list, tabsolute, s=1)
    print('\n Modulus-Reddening error pair estimated using different composite wesenheit magnitudes \n' ,correction_red_mu_stars.head())
    if z==1:
        input('###'*30+'\n')
    corrected = correction_apply(tabsolute, correction_red_mu_stars, flags, s=1)
    print(corrected.head(-1))
    corrected_reg(tabsolute, corrected, dis_flag[0], flags, s=1)
    return correction_red_mu_stars, corrected
####################################################################################################
from visuals.dataload import pick_star
def load_ex_mu(n):
    print('loading stars')
    stars_ex_red_mu_list=[]
    for i in range(n):
        _,ex_red_mu = pick_star(i)
        stars_ex_red_mu_list.append(ex_red_mu)
    print('loaded')
    return stars_ex_red_mu_list
