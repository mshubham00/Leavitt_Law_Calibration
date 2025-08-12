### file: ./show.py

from visuals.dataload import raw, transformation, PLWcorrection, del_del
from visuals.dataload import ext_red, pick_extred
#from visuals.transformation import get_apparent, get_absolute, plt_wes_plotly
from visuals.plrelation import PLmc, pl6, PLresidue, PWresidue
from visuals.deldel import plotdeldel, dmc, residue, PLPWres
#from visuals.reddening import starbystar
from lvtlaw.a_utils import wes_cols, dis_flag, wes_show, output_directories, img_out_path, process_step


output_directories(parent_folder = img_out_path, s=1,subdirectories = process_step)

#from lvtlaw.star_analysis import star_analysis
#for i in range(0,len(raw)):
#    star_analysis(i)
############# transformation ##################
absolute, extinction, tabsolute, wesenheit = transformation()
#get_apparent(raw, extinction)
#get_absolute(tabsolute)
#plt_wes_plotly(tabsolute,absolute, wesenheit, '_i', 'wesen_data_i')
#plt_wes_plotly(tabsolute,absolute, wesenheit, '_g', 'wesen_data_g')
############### plrelation ####################
PLWdata, PLWresidue, PLWregression, PLWregression, PLWprediction = PLWcorrection()
#PLmc(PLWregression)
#pl6(tabsolute,list(PLWregression.mg[6:12]),list(PLWregression.cg[6:12]),list(PLWregression.mg[12:18]),list(PLWregression.cg[12:18]))
PLresidue(PLWresidue)
PWresidue(PLWresidue)
for c in wes_show:
    plotdeldel(c, '_g', PLWresidue)    
    plotdeldel(c, '_i', PLWresidue)
################ deldel ######################
dpre_M, dres_M, dmc_M, dpre_S, dres_S, dmc_S, dSM = del_del()
dmc(dmc_M,dmc_S)
for c in wes_show:
    residue(dres_M, dres_S,c)
for c in wes_show:
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
