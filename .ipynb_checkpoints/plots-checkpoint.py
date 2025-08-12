import numpy as np
import matplotlib.pyplot as plt
import pandas as pd                                             #   0
from lvtlaw.utils import img_out_path, mag, ap_bands, abs_bands
from lvtlaw.visual import milky_way
bands_label = ap_bands


# Data Extraction

data = pd.read_csv('./data/input/cleaned_data.csv')             
data_abs = pd.read_csv('./data/output/95_abs_data.csv')             
data_ = data[['plx', 'IRSB']]
data_E= data[['EBV', 'logP']]
data_m = data[bands_label] #- data['plx']
abss = []
tick_true = []
tick_abs = []
data_M = pd.DataFrame()
for i in range(0,6):
    abss.append(abs_bands[i] + '_i')
    tick_true.append(mag[i]+'0')
    tick_abs.append('M'+mag[i])
    data_M[abs_bands[i]] = data[bands_label[i]] - data['IRSB']
data_M0 = pd.DataFrame()
#data_M0['logP'] = data['logP']
#data_M0['IRSB'] = data['IRSB']
data_M0[mag] = data[bands_label]
data_M0[tick_abs] = data_M[abs_bands]
data_M0[tick_true] = data_abs[abss]
print(data_M0.info())
output_path = './data/output/plots/'
dis = data.IRSB #* u.kpc
ra = data.RA_ICRS                                               #   4
dec = data.DE_ICRS
##################################################################### 
milky_way(ra,dec,dis, title = 'milkyway', img_path=output_path)

#histogram_plot(kind = 1, data = data_, bins=20, title='IRSB vs Parallax Distance', xlabel='Distance Range (in modulus)', ylabel='Number of Cepheid stars')
#histogram_plot(kind = 2, data = data_, bins=20, title='IRSB vs Parallax Distance', xlabel='Distance Range (in modulus)', ylabel='Number of Cepheid stars')
#sea_sub(data_M0)
#histogram_plot(kind = 1, data = data_E, bins=20, title='Period and Reddening Distribution', xlabel='Values', ylabel='Number of Cepheid stars')
#sea_pair(data_M0)
#photometry(data_M, title = 'apparent',xlabel = 'Luminosity in magnitude unit', ylabel = 'Number of Cepheids', img_path=img_out_path)
#cat_photometry(data_M0,  title = 'Comparision',xlabel = 'Luminosity in magnitude unit', ylabel = 'Number of Cepheids', img_path=img_out_path)
#photometry(data_M0,  title = 'true_absolute',xlabel = 'Luminosity in magnitude unit', ylabel = 'Number of Cepheids', img_path=img_out_path)
