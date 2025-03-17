### file: ./visuals/reddening.py

#from visuals.dataload import raw, absolute, wesenheit, dmc_S, extinction, tabsolute, PLWregression, PLWresidue
from visuals.dataload import ext_g, ext_i, red_g, red_i



def reddening(wes_S):


    e_g = ext_g[1][wes_MS]
    e_g = ext_i[1][wes_MS]
    r_g = red_g[1][wes_MS]
    r_g = red_i[1][wes_MS]
