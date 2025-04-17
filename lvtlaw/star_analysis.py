### File: ./lvtlaw/star_analysis.py

from lvtlaw.utils import colors,data_dir, input_data_file, data_out, R, mag, dis_flag, dis_list, wes_cols, process_step, flags, n
import pandas as pd
from lvtlaw.pl_pw import pl_reg     #pl_reg(data,'_g','_i') -> PLW, residue, prediction
from lvtlaw.data_transform import transformation, extinction_law

def ex_rd_error(residue, slope_data, dis_flag = dis_flag, cols = wes_cols, flags=flags, s=1):
    # Input PLW relations slope, intr, residue for all different distances, 
    ex_ = pd.DataFrame()
    rd_ = pd.DataFrame()
    for flag in flags:
        for dis in dis_flag:
            for col in cols:
                for i in range(0, len(mag)):
                    if flag == '_S':
                        wes = mag[i] + col
                        slope = slope_data[0]
                    else:
                        wes = col[0] + col
                        slope = slope_data[1]
                    wm_str = mag[i] + wes
                    if dis == dis_flag[0]:      # gaia
                        m = slope[wm_str].iloc[0]
                        c = slope[wm_str].iloc[2]
                    elif dis == dis_flag[1]:      # i
                        m = slope[wm_str].iloc[4]            
                        c = slope[wm_str].iloc[6]
                        
                    
                    extinction, reddening = ex_rd_0(residue,m,c,i,col, wes, dis)
                    ex_[wm_str + dis+flag] = extinction
                    rd_[wm_str + dis+flag] = reddening
    if s == 1:
        ex_.to_csv('%s%i_ex0.csv' % (data_out + process_step[3], n))
        rd_.to_csv('%s%i_rd0.csv' % (data_out + process_step[3], n))    
    return ex_, rd_










def ex_rd_0(residue, m, c, i, col, wes, dis):
    # calculates extinction and reddening error for fixed distance error.
    del_M = residue['r0_' + mag[i] + dis]
    del_W = residue['r_' + wes + dis]
    r = R[i] / (R[mag.index(col[0])] - R[mag.index(col[1])])
    ex_ = (del_M) - m * (del_W) - c 
    rd_ = ex_ / r
    return ex_, rd_    # lists

def ex_rd_error(residue, slope_data, dis_flag = dis_flag, cols = wes_cols, flags=flags, s=1):
    # Input PLW relations slope, intr, residue for all different distances, 
    ex_ = pd.DataFrame()
    rd_ = pd.DataFrame()
    for flag in flags:
        for dis in dis_flag:
            for col in cols:
                for i in range(0, len(mag)):
                    if flag == '_S':
                        wes = mag[i] + col
                        slope = slope_data[0]
                    else:
                        wes = col[0] + col
                        slope = slope_data[1]
                    wm_str = mag[i] + wes
                    if dis == dis_flag[0]:      # gaia
                        m = slope[wm_str].iloc[0]
                        c = slope[wm_str].iloc[2]
                    elif dis == dis_flag[1]:      # i
                        m = slope[wm_str].iloc[4]            
                        c = slope[wm_str].iloc[6]
                    extinction, reddening = ex_rd_0(residue,m,c,i,col, wes, dis)
                    ex_[wm_str + dis+flag] = extinction
                    rd_[wm_str + dis+flag] = reddening
    if s == 1:
        ex_.to_csv('%s%i_ex0.csv' % (data_out + process_step[3], n))
        rd_.to_csv('%s%i_rd0.csv' % (data_out + process_step[3], n))    
    return ex_, rd_

#####################################################################################

def star_data(star_num, data, PLWresidue, dres_M, dres_S, ex_, rd_): 
    name = data.name.iloc[[star_num]].to_string()    #  Getting star name
    period = data.logP.iloc[star_num]                #  period of the star
    exc = data.EBV.iloc[star_num]                 #  color excess of the star
    mod_g = data['plx'].iloc[star_num]                 #  modulus of the star
    mod_i = data['IRSB'].iloc[star_num]
    cep = [name, period, exc, mod_g, mod_i] 
                         #  getting residue from PL relation
    res = [PLWresidue.columns.tolist(), PLWresidue.iloc[star_num]]
    
    dmc_SM_cols = [dmc_S.columns.tolist(), dmc_M.columns.tolist()]
    dmc_SM = [dmc_S, dmc_M]
    dmc = [dmc_SM_cols, dmc_SM]
    
    dres_SM_cols = [dres_S.columns.tolist(), dres_M.columns.tolist()]
    dres_SM = [dres_S.iloc[star_num], dres_M.iloc[star_num]]    #  residue from Del_M-Del_W plot (residue =
    dres = [dres_SM_cols, dres_SM]

   # ex_err, rd_err = ex_rd_error(PLWresidue, dmc_SM, s=0)
    err_cols = [ex_err.columns.tolist(), rd_err.columns.tolist()]
    err = [ex_err.iloc[star_num], rd_err.iloc[star_num]]
    er = [err_cols, err]

    return cep, res, dmc, dres, er   


def star_analysis(k):
    s = star_data(k)
    extinction = pd.DataFrame()
    reddening = pd. DataFrame()
    mu = [round(i*0.01,2) for i in range(-100,100,2)]
#    mu = [round(x, 2) for x in mu]
    extinction['mu'] = mu    
    reddening['mu'] = mu

    # list - PLW residue [res_col_name_list, residue_data]    
    res_cols = s[1][0][5:] # list of coloumns names of PLW residue      

    # list - slope from del-del correlation, [col_name [S-type, M-type], values[S-type, M-type]]
    dmc_cols_S = s[2][0][0][1:]
    dmc_cols_M = s[2][0][1][1:]

    # list - residues from del-del correlation [col_names[S-type, M-type], values[S-type, M-type]]
    dres_cols_S = s[3][0][0][3:] 
    dres_cols_M = s[3][0][1][3:]

    # list - residues from del-del correlation [col_names[S-type, M-type], values[S-type, M-type]]
    e_cols = s[4][0][0]
    r_cols = s[4][0][1]    
    dmc = {}
    dres = {}
    res = s[1][1][5:]
    dmc['_S'] = s[2][1][0]
    dmc['_M'] = s[2][1][1]
    dres['_S'] = s[3][1][0][3:]
    dres['_M'] = s[3][1][1][3:]
    e = s[4][1][0]
    r = s[4][1][1] 
#    print(dres_S['r_KKJK_i'], dmc_S['KKJK'].iloc[4])    
    for i in dis_flag:
        for col in wes_cols:
            for m in mag:
                for flag in flags:
                    r = R[mag.index(m)] / (R[mag.index(col[0])] - R[mag.index(col[1])])                
                    if i == '_g':
                        x = 0
                    else:
                        x=4
                    if flag == '_S':
                        wes = m + m + col
                    else:
                        wes = m + col[0] + col
                    extinction[wes+i+flag] = [dmc[flag][wes].iloc[x] + dres[flag]['r_'+wes+i] + y*(1-dmc[flag][wes][x]) for y in mu]
                    reddening[wes+i+flag] = extinction[wes+i+flag]/r 
    reddening.to_csv('%s%i_%i_star_r.csv'%(data_out+process_step[3],len(reddening),k))
    extinction.to_csv('%s%i_%i_star_e.csv'%(data_out+process_step[3],len(extinction),k))
    return reddening, extinction




def star_dispersion(ind):
    del_mu = [i*0.01 for i in range(-100,100,2)]
    del_mu = [round(x, 2) for x in del_mu]
    del_mu_str = [str(round(x, 2)) for x in del_mu]
    stars = {}
    x = 0
    if x == 0:
        for dis in dis_flag:
            stars[dis] = {}
            for col in wes_cols:
                stars[dis][col] = {}
                for flag in flags:
                    stars[dis][col][flag] = {}
                    data = pd.DataFrame(columns = del_mu_str)
                    for mu in del_mu_str:
                        data[mu] = pick_disper(dis,col,flag,mu).iloc[ind]
                    data.index.name = col+flag+dis+str(ind)
                    stars[dis][col][flag] = data
    return stars

