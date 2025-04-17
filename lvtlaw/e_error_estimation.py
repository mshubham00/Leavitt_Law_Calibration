### File: ./lvtlaw/e_error_estimation.py
from lvtlaw.a_utils import colors,data_dir, input_data_file, data_out, R, mag, dis_flag, dis_list, process_step, del_mu
import pandas as pd
from lvtlaw.b_data_transform import transformation, extinction_law
from lvtlaw.c_pl_pw import pl_reg     #pl_reg(data,'_g','_i') -> PLW, residue, prediction

def reddening_error(wes_cols, dis_flags, dSM, s = 1):
    ext0S = pd.DataFrame()
    ext0M = pd.DataFrame()
    red0S = pd.DataFrame()
    red0M = pd.DataFrame()
    ex_rd_mu = []    # dis.cols_SM.mag.mu_e_r.star
    for dis in dis_flags:
        if dis == '_i':
            m_S = dSM[0][0].iloc[4].T
            c_S = dSM[0][0].iloc[5].T
            m_M = dSM[0][1].iloc[4].T
            c_M = dSM[0][1].iloc[5].T
        else:
            m_S = dSM[0][0].iloc[0].T
            c_S = dSM[0][0].iloc[1].T
            m_M = dSM[0][1].iloc[0].T
            c_M = dSM[0][1].iloc[1].T
        dis_mu = {}
        print('\n Distance is: ' + dis+ '\n Wesenheit color: ')
        for col in wes_cols:        
            print(' Processing \t' + col)
            wes_mu_S = [] 
            wes_mu_M = []
            for i in range(len(mag)):
                Mwm_str = mag[i] + col[0] + col
                ext0, red0, ex_rd_m = error_over_mu(i, col , dis , '_M', Mwm_str, m_M, c_M, dSM[1][1], s)    
                ext0M[Mwm_str+dis] = ext0 
                red0M[Mwm_str+dis] = red0 
                wes_mu_M.append(ex_rd_m) 
            for i in range(len(mag)):
                Swm_str = mag[i] + mag[i] + col
                ext0, red0, ex_rd_m = error_over_mu(i, col , dis , '_S', Swm_str, m_S, c_S, dSM[1][0], s)    
                ext0S[Swm_str+dis] = ext0 
                red0S[Swm_str+dis] = red0 
                wes_mu_S.append(ex_rd_m) 
            dis_mu[col+'_M'] = wes_mu_M
            dis_mu[col+'_S'] = wes_mu_S
        ex_rd_mu.append(dis_mu)
    print('\n Reddening error (mu-0) from Madore approach: \n ',red0M.head(10))
    print('\n Reddening error (mu-0) from Shubham approach: \n ',red0S.head(10))
    red_SM = [red0S, red0M]
    if s == 1:
        ext0S.to_csv('%s%i_ext_err0_S.csv' % (data_out + process_step[3], len(ext0S)))
        ext0M.to_csv('%s%i_ext_err0_M.csv' % (data_out + process_step[3], len(ext0M)))    
        red0S.to_csv('%s%i_red_err0_S.csv' % (data_out + process_step[3], len(red0S)))
        red0M.to_csv('%s%i_red_err0_M.csv' % (data_out + process_step[3], len(red0M)))    
    return red_SM, ex_rd_mu

def error_over_mu(i, col , dis , flag, wm_str, slope, intercept, dres, s):
    r = R[i] / (R[0] - R[1])   # reddening ratio B-V
    slope = slope['%s'%(wm_str)]
    intercept = intercept['%s'%(wm_str)]
    ext0 = dres['d_%s%s'%(wm_str,dis)]
    red0 = ext0/r #  to convert extinction into redenning E(B-V)
    mu_run_ext_red = run_mu_for_reddening(ext0, r, slope, intercept)
    if s == 1:
        #print(mu_run_ext_red)
        mu_run_ext_red.to_csv('%s%i%s%s%s.csv' % (data_out + process_step[4], len(mu_run_ext_red), dis, wm_str, flag))
    return ext0, red0, mu_run_ext_red

def run_mu_for_reddening(ex, r, slope, intercept):
    mu_run = pd.DataFrame()
    for mu in del_mu:
        mu_run['ex_'+str(mu)] = ex + mu*(1-slope) - intercept
        mu_run['rd_'+str(mu)] = mu_run['ex_'+str(mu)] / r
    return mu_run



