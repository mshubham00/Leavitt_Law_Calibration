import pandas as pd
from scipy import stats

mag = ['B', 'V', 'I','J','H','K']; 
bands = ['M_B', 'M_V', 'M_I', 'M_J', 'M_H', 'M_K']; band = len(bands);
ap_bands = ['B_mag', 'V_mag' ,'I_mag', 'J_mag', 'H_mag', 'K_mag']
col_dot = ['k.', 'r*', 'g+', 'c*', 'k+', 'gx', 'y+', 'b+', 'c.'] ; 
col_lin = ['k-', 'r-', 'g-', 'c-', 'k-', 'g-', 'y-', 'b-', 'c-'] ; 
col_das = ['k--', 'r--', 'g--', 'c--', 'k--', 'g--', 'y--', 'b--', 'c--']
col_ = ['k', 'r', 'g', 'c', 'k', 'g', 'y', 'b', 'c'] ; 
mu = [round(i*0.01,2) for i in range(-100,100,2)]

def save(title, img_path = '../../Latex/figures/clean/'):
    plt.savefig('%s%s.pdf'%(img_path,title))

def data_select(dataset_number, R_value_index):
    input_file = ['59_madore','95_jesper','18_cluster', '36_LMC', '32_SMC', '10_cluster_cruz']
    R_value = ['1', '2', '3', '3.15', '3.23', '3.3', '3.5', '4']
    print(f'Dataset Loaded: {input_file[dataset_number]} and R_V = {R_value[R_value_index]}')
    raw = pd.read_csv(f'../data/input/{input_file[dataset_number]}.csv', index_col=0); cepheid = len(raw)
    data_load = f'../data/{input_file[dataset_number]}_{R_value[R_value_index]}/'
    cepheid=len(raw)
    data, w, PLW, prediction, residue, del_mc, dres, dpre, err, correction = dataset(data_load, cepheid)
    return raw, data_load, data, w, PLW, prediction, residue, del_mc, dres, dpre, err, correction



def color_index(mag = mag):
    color_index = []
    for i in range(0,len(mag)):
        for j in range(i+1,len(mag)):
            color_index.append(mag[i]+mag[j])
    #print('Possible %i combinations of color indexes (str): \n'%(len(color_index)), color_index)
    return color_index

cols = color_index

def regression(x, y, x_str, y_str, p = 0):
    regression_line = stats.linregress(x, y); 
    m = regression_line.slope; 
    c = regression_line.intercept
    prediction = [m * xw + c for xw in x]; 
    residue = y #-prediction 
    m_error = regression_line.stderr; 
    c_error = regression_line.intercept_stderr
    if p == 1:
        print('%s = %f %s ( %f) + %f ( %f)'%(y_str, m, x_str, m_error, c, c_error))
    return m, c, prediction, residue, m_error, c_error

def pick_star(n, data_load, cepheid):
    star = pd.read_csv('%s%i_star.csv'%(data_load+'0_stars/',n), index_col=0)
    erm = pd.read_csv('%s%i_%istars_ex_red_mu.csv'%(data_load+'6_rms/',cepheid,n), index_col=0)    
    return star, erm

def dataset(data_load, cepheid):
    data = pd.read_csv(data_load + f'1_prepared/{cepheid}_true_abs_data.csv', index_col=0)#%(data_path,cepheid,mode))
    w = pd.read_csv(data_load + f'1_prepared/{cepheid}_wes_data.csv', index_col=0)#%(data_path,cepheid,mode))

    PLW = pd.read_csv('%s%s_5_regression.csv'%(data_load+'2_PLPW/',cepheid), index_col=0)
    prediction = pd.read_csv('%s%s_prediction.csv'%(data_load+'2_PLPW/',cepheid), index_col=0)
    residue = pd.read_csv('%s%s_residue.csv'%(data_load+'2_PLPW/',cepheid), index_col=0)

    del_mc = pd.read_csv('%s%i_del_slope_intercept.csv'%(data_load+'3_deldel/',cepheid), index_col=0)
    dres = pd.read_csv('%s%i_del_res.csv'%(data_load+'3_deldel/',cepheid), index_col=0)
    dpre = pd.read_csv('%s%i_del_pre.csv'%(data_load+'3_deldel/',cepheid), index_col=0) 
    
    err = pd.read_csv('%s%i_error_rms_mu_rd.csv'%(data_load+'7_errorpair/',cepheid), index_col=0)
    correction = pd.read_csv('%s%i_corrected.csv'%(data_load+'8_result/',cepheid), index_col=0)

    return data, w, PLW, prediction, residue, del_mc, dres, dpre, err, correction
