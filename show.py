### file: ./show.py

from visuals.dataload import raw, absolute, wesenheit, dmc_S, extinction, tabsolute, PLWregression, PLWresidue
from visuals.dataload import dmc_M, dmc_S, dres_M, dres_S, ext_g, ext_i, stars, pick_extred
from visuals.transformation import get_apparent, get_absolute, plt_wes_plotly
from visuals.plrelation import PLmc, pl6, PLresidue, PWresidue
from visuals.deldel import plotdeldel, dmc, residue, PLPWres
from visuals.reddening import starbystar
from lvtlaw.utils import wes_cols, dis_flag

#from lvtlaw.star_analysis import star_analysis
#for i in range(0,len(raw)):
#    star_analysis(i)

############# transformation ##################
get_apparent(raw, extinction)
get_absolute(tabsolute)
plt_wes_plotly(tabsolute,absolute, wesenheit, '_i', 'wesen_data_i')
plt_wes_plotly(tabsolute,absolute, wesenheit, '_g', 'wesen_data_g')
############### plrelation ####################
PLmc(PLWregression)
pl6(tabsolute,list(PLWregression.mg[6:12]),list(PLWregression.cg[6:12]),list(PLWregression.mg[12:18]),list(PLWregression.cg[12:18]))
PLresidue(PLWresidue)
PWresidue(PLWresidue)
################ deldel ######################
for c in wes_cols:
    plotdeldel(c, '_g', PLWresidue)    
    plotdeldel(c, '_i', PLWresidue)
dmc(dmc_M,dmc_S)
for c in wes_cols:
    residue(dres_M, dres_S,c)

for c in wes_cols:
    PLPWres(dres_M, dres_S, c)

############## reddening #####################

#for i in range(0,20):
#   star_analysis(i)


#stars = star_dispersion(0)
#stars[ind][dis][col][flag] 

#print(stars['_g']['BV']['_S'])
#print(d.info())
#x = pick_extred('red','BBVI','_g')
#print(x['logP'].iloc[3])
